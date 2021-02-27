# Highway Lane Detection 

![Project Image](https://user-images.githubusercontent.com/79725511/109364795-94487400-785d-11eb-93ce-119b0c352cb4.png)

> A quick snap of the lane detection output.

---

### Table of Contents

- [Description](#description)
- [Technologies](#technologies)
- [License](#license)
- [Author Info](#author-info)

---

## Description

Implemented a real-time computer vision algorithm to detect the lanes from the recorded video of Greenville - Atlanta highway. The basic pipeline of the algorithm would be image processing such as color conversion and gaussian blur, canny edge detection for detecting the edges of the image, region-masking for isolating the lane region from the background, hough transform to find the lane lines in the image, and polyline fit to map the detected lines into left lane and right lane. In addition to that I have also designed a Stanley controller for smooth tracking of the detected lane lines. 

The final output video will include four different views: 

1) Original highway view 
2) Canny edge detection view
3) Region-masked view
4) Detected left and right lane view

Here is the [video_link](https://www.linkedin.com/posts/venkat-balachandran_opencv-python-computervision-activity-6694674707540705280-X_Tg) of the final output.


#### Technologies

- Python
- OpenCV
- Visual studio code

[Back To The Top](#Highway-Lane-Detection)

---

## License

MIT License

Copyright (c) [2020] [Venkat Narayanan Balachandran]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[Back To The Top](#Highway-Lane-Detection)

---

## Author Info

- LinkedIn - [Venkat_Narayanan_Balachandran](https://www.linkedin.com/in/venkat-balachandran)

[Back To The Top](#Highway-Lane-Detection)


