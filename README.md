<h1 align="center">Computer Vision</h1>
<h2 align="center">Options for the use of computer vision in the framework of the Cup of the Governor of the region in computer vision</h2>

<h2 align="center">Tasks</h2>

### Nut defect detection (product quality control)
The video shows the movement of nuts along the conveyor. The nuts move from the lower border of the frame to the upper one. Among the nuts there are defective ones, they are deformed and have distorted contours. For each nut captured on video, it is necessary to determine compliance with quality standards.

The 97% accuracy solution is presented in folder [task1](task1).
### Logo detection

The image shows the logo. Your task is to write a function that determines in which part of the image the logo is located, and what it is called. Each image shows one of the five logos.

Your function should return the name of the logo and the coordinates of the border bounding the logo. Correctly detected and recognized are those logos for which the name is correctly indicated and the IoU is greater than 0.5.

The 98% accuracy solution is presented in folder [task2](task2).

### Classification of road signs

The images show traffic signs. There is exactly one sign on each image. Your task is to write a function that determines which of the eight characters in the image.

The 100% accuracy solution is presented in folder [task3](task3).

### Traffic light detection

The images show traffic lights. Your task is to write a function that determines in which part of the image the traffic light is located. There is only one traffic light in each image. The function should return the coordinates of the frame bounding the traffic light. Traffic lights for which IoU is greater than 0.5 are considered to be correctly detected.

The 100% accuracy solution is presented in folder [task4](task4).


### Hand detection

Your task is to write a program for gesture recognition and integrate it into aikar. Possible gestures: the thumb up indicates forward movement, the thumb down indicates backward movement, the index finger to the left and to the right indicate turns to the left and to the right, respectively, and the clenched fist indicates a stop.

### Eyes detection
