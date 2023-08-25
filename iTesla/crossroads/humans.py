import cv2
import numpy as np


class HumansDetector(object):
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog = cv2.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect_pedestrian(self, img: np.ndarray) -> list:
        rects, weights = self.hog.detectMultiScale(img, winStride=(4, 4))
        return rects

    def check_people_exists(self, img: np.ndarray) -> bool:
        rects, weights = self.hog.detectMultiScale(img, winStride=(4, 4))
        return len(rects) > 0
