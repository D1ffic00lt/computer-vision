#!/usr/bin/env python3

import cv2
import numpy as np
import os
import time
import pigpio


def setup_gpio():
    os.system("sudo pigpiod")
    time.sleep(1)
    ESC = 17
    STEER = 18
    pi = pigpio.pi()
    pi.set_servo_pulsewidth(ESC, 0)
    pi.set_servo_pulsewidth(STEER, 0)
    time.sleep(1)
    return pi, ESC, STEER


def control(pi, ESC, speed, STEER, angle):
    pi.set_servo_pulsewidth(ESC, speed)
    pi.set_servo_pulsewidth(STEER, int(11.1 * angle + 500))


pi, ESC, STEER = setup_gpio()
control(pi, ESC, 1500, STEER, 90)
print("Start")
time.sleep(2)

# control(pi, ESC, 1560, STEER, 90)
# time.sleep(1)
# control(pi, ESC, 1400, STEER, 90)
# time.sleep(1)
# control(pi, ESC, 1500, STEER, 90)

SIZE = (533, 300)

RECT = np.float32([[0, SIZE[1]],
                   [SIZE[0], SIZE[1]],
                   [SIZE[0], 0],
                   [0, 0]])

TRAP = np.float32([[10, 299],
                   [523, 299],
                   [440, 200],
                   [93, 200]])

src_draw = np.array(TRAP, dtype=np.int32)

SIZE = (533, 300)

cap = cv2.VideoCapture(0)
key = 1
ESCAPE = 27
angle = 90
# control(pi, ESC, 1500, STEER, 90)

while key != ESCAPE:
    status, frame = cap.read()
    if status:
        # cv2.imshow("Frame", frame),

        img = cv2.resize(frame, SIZE)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary = cv2.inRange(gray, 120, 255)  # 130
        # cv2.imshow("binary", binary)
        matrix_trans = cv2.getPerspectiveTransform(TRAP, RECT)
        perspective = cv2.warpPerspective(binary, matrix_trans, SIZE, flags=cv2.INTER_LINEAR)
        # trap_visual = cv2.drawContours(binary.copy(), [src_draw], -1, 150, thickness=3)
        # cv2.imshow("trap_vis", trap_visual)
        # cv2.imshow("perspective", perspective)

        hist = np.sum(perspective, axis=0)
        mid = hist.shape[0] // 2
        left = np.argmax(hist[:mid])
        right = np.argmax(hist[mid:]) + mid

        # cv2.line(perspective, (left, 0), (left, SIZE[1]), 50, 2)
        # cv2.line(perspective, (right, 0), (right, SIZE[1]), 50, 2)
        # cv2.line(perspective, (200, 0), (200, SIZE[1]), (255, 0, 0), 2)
        if (left + right) // 2 < 160:
            angle = 70
        elif (left + right) // 2 > 250:
            angle = 110
        else:
            angle = 90
        # cv2.line(perspective, (300, 0), (300, SIZE[1]), (255, 0, 0), 2)
        # cv2.line(perspective, ((left + right) // 2, 0), ((left + right) // 2, SIZE[1]), 110, 3)
        # cv2.imshow('lines', perspective)
        control(pi, ESC, 1570, STEER, angle)
    else:
        print("End of Video")
        # cap.release()
        # cap = cv2.VideoCapture("output1280.avi")

    # key = cv2.waitKey(50)

cv2.destroyAllWindows()
cap.release()
