import numpy as np
import cv2

# Image processing and edge detection
cap = cv2.VideoCapture("Highway video.mp4")
clip = 0
while cap.isOpened():
    _, frame = cap.read()
    original = frame.copy()
    gray_image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    def adjust_gamma(image, gamma=1):
        invGamma = 1 / gamma
        table = np.array([((i / 255) ** invGamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
        return cv2.LUT(image, table)

    darkened_image = adjust_gamma(gray_image, 0.5)
    # mask_white = cv2.inRange(gray_image, 200, 255)
    # mask_white_image = cv2.bitwise_and(darkened_image, mask_white)
    blur = cv2.GaussianBlur(darkened_image, (5, 5), 0)
    canny = cv2.Canny(blur, 100, 200)

# Region masking
    height = frame.shape[0]
    width = frame.shape[1]
    polygon = np.array(
        [[(300, height), (610, 400), (700, 400), (1100, height)]])
    mask = np.zeros_like(canny)
    cv2.fillPoly(mask, polygon, 255)
    masked_image = cv2.bitwise_and(canny, mask)

# Lane lines detection using Hough Transform
    lines = cv2.HoughLinesP(masked_image, 2, np.pi/180, 100,
                            minLineLength=50, maxLineGap=500000)
    left_fit = []
    right_fit = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    print(left_fit_average, 'leftavg')
    print(right_fit_average, 'rightavg')

    def create_coordinates(image, line_parameters):
        try:
            slope, intercept = line_parameters
        except TypeError:
            slope, intercept = 0.1, 0.1
        y1 = int(height)
        y2 = int(y1 * (0.7))
        x1 = int((y1 - intercept)/slope)
        x2 = int((y2 - intercept)/slope)
        return np.array([x1, y1, x2, y2])

    left_line = create_coordinates(frame, left_fit_average)
    right_line = create_coordinates(frame, right_fit_average)
    print(left_line, 'leftline')
    print(right_line, 'rightline')

# draw the lines on the image
    lane_lines = np.array([left_line, right_line])
    for x1, y1, x2, y2 in lane_lines:
        line_image = cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 10)
    combo_image = cv2.addWeighted(frame, 0.2, line_image, 0.9, 1)

# Camera Calibration outputs (calculated)
    focal_length_u = 733.4111
    focal_length_v = 734.7829
    pixel_u = 630.2279
    pixel_v = 477.9256

# Finding the real world coordinates for the lane
    camera_height_Yc = 210
    Zc_left_far_end = (focal_length_v * camera_height_Yc) / \
        (left_line[3] - pixel_v)
    Xc_left_far_end = (Zc_left_far_end *
                       (left_line[2] - pixel_u)) / (focal_length_u)
    Zc_left_near_end = (focal_length_v * camera_height_Yc) / \
        (left_line[1] - pixel_v)
    Xc_left_near_end = (
        Zc_left_far_end * (left_line[0] - pixel_u)) / (focal_length_u)

    Zc_right_far_end = (focal_length_v * camera_height_Yc) / \
        (right_line[3] - pixel_v)
    Xc_right_far_end = (
        Zc_left_far_end * (right_line[2] - pixel_u)) / (focal_length_u)
    Zc_right_near_end = (focal_length_v * camera_height_Yc) / \
        (right_line[1] - pixel_v)
    Xc_right_near_end = (
        Zc_left_far_end * (right_line[0] - pixel_u)) / (focal_length_u)


# Stanley controller design to track the lane center line
    Xc_center_far = (Xc_left_far_end + Xc_right_far_end) / 2
    Xc_center_near = (Xc_left_near_end + Xc_right_near_end) / 2
    Zc_center_far = (Zc_left_far_end + Zc_right_far_end) / 2
    Zc_center_near = (Zc_left_near_end + Zc_right_near_end) / 2

    camera_position = 60   # calculated

    slope_center_line = (Zc_center_far - Zc_center_near) / \
        (Xc_center_far - Xc_center_near)
    departure_angle = -(np.arctan(slope_center_line)) - 90
    departure_distance = Xc_center_near + (1/slope_center_line) * \
        (Zc_center_near - camera_position)

    gain_k1 = 1  # Control gain for stanley controller
    gain_k2 = 0.01
    steering_angle = abs((-gain_k1 * departure_angle) -
                         (gain_k2 * departure_distance))
    print('steering angle', steering_angle)
    clip += 1
    print('frame No.', clip)
    cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Original', 680, 360)
    cv2.imshow('Original', original)

    cv2.namedWindow('Canny Edge Detection', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Canny Edge Detection', 680, 360)
    cv2.imshow('Canny Edge Detection', canny)

    cv2.namedWindow('Lane Masking', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Lane Masking', 680, 360)
    cv2.imshow('Lane Masking', masked_image)

    cv2.namedWindow('Final Output', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Final Output', 680, 360)
    cv2.imshow('Final Output', combo_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
