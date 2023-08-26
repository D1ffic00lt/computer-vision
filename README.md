<h1 align="center">Computer Vision</h1>
<h2 align="center">Options for the use of computer vision in the framework of the Cup of the Governor of the region in computer vision</h2>

<h2 align="center">Tasks</h2>

### Nut defect detection (product quality control)
> The video shows the movement of nuts along the conveyor. The nuts move from the lower border of the frame to the upper one. Among the nuts there are defective ones, they are deformed and have distorted contours. For each nut captured on video, it is necessary to determine compliance with quality standards.

![image](https://github.com/D1ffic00lt/computer-vision/assets/69642892/929e99b8-ec18-4d43-8519-d873d24eaaf1)

The 97% accuracy solution is presented in folder [folder](nut-defect-detection) .
### Logo detection

> The image shows the logo. Your task is to write a function that determines in which part of the image the logo is located, and what it is called. Each image shows one of the five logos.

> Your function should return the name of the logo and the coordinates of the border bounding the logo. Correctly detected and recognized are those logos for which the name is correctly indicated and the IoU is greater than 0.5.

![image](https://github.com/D1ffic00lt/computer-vision/assets/69642892/b9b194c3-671a-4301-ba72-4e4275cd3076)

The 98% accuracy solution is presented in [folder](logo-detection).

### Classification of road signs

> The images show traffic signs. There is exactly one sign on each image. Your task is to write a function that determines which of the eight characters in the image.

![image](https://github.com/D1ffic00lt/computer-vision/assets/69642892/1b3e597d-35ff-4104-9acb-b0c2f2c2bdae)

The 100% accuracy solution is presented in folder [folder](classification-of-road-signs).

### Traffic light detection

> The images show traffic lights. Your task is to write a function that determines in which part of the image the traffic light is located. There is only one traffic light in each image. The function should return the coordinates of the frame bounding the traffic light. Traffic lights for which IoU is greater than 0.5 are considered to be correctly detected.

![image](https://github.com/D1ffic00lt/computer-vision/assets/69642892/483060df-dff2-4b77-b008-046f82d23e17)


The 100% accuracy solution is presented in folder [folder](traffic-light-detection).


### Hand detection

> Your task is to write a program for gesture recognition and integrate it into aikar. Possible gestures: the thumb up indicates forward movement, the thumb down indicates backward movement, the index finger to the left and to the right indicate turns to the left and to the right, respectively, and the clenched fist indicates a stop.

The solution is presented in folder [folder](hand-detection).

### Eyes detection

> Your task is to write a program for blinking recognition and integrate it into aikar. A single blink indicates a turn of the wheels by 70, 90 and 110 degrees, a double blink indicates a stop and start of movement.

The solution is presented in folder [folder](eyes-detection).

### Aikar on the road (the task of the cup final)

> You need to "teach" akar to drive along the highway in a figure of eight, drive through intersections, stop at traffic lights, turn left and let pedestrians pass.

The solution that took the first place is presented in the [folder](iTesla).
