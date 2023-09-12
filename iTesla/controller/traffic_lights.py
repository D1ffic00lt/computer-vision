import cv2
import numpy as np

from typing import Tuple


class TrafficLightDetector(object):
    def __init__(self, weights_path: str, cfg_path: str):
        self.model = self._load_models(weights_path, cfg_path)

    @staticmethod
    def _load_models(weights_path: str, cfg_path: str):
        net = cv2.dnn.readNet(weights_path, cfg_path)

        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)

        return model

    def detect(self, image) -> Tuple:
        classes, scores, boxes = self.model.detect(image, 0.5, 0.4)
        if len(boxes):
            bbox = boxes[0]
            x, y, w, h = [i for i in bbox]

            return int(x), int(y), int(w), int(h)

        bbox = (0, 0, 0, 0)
        return bbox

    def check_traffic_color(self, frame):
        box = self.detect(frame)

        x, y, w, h = box
        new_img = frame[y:y + h, x:x + w]
        bin_frame = cv2.inRange(new_img, (113, 203, 173), (255, 255, 255))

        green = bin_frame[(new_img.shape[0] // 3) * 2:, :]
        yellow = bin_frame[new_img.shape[0] // 3:(new_img.shape[0] // 3) * 2, :]
        red = bin_frame[:new_img.shape[0] // 3, :]

        if np.sum(green) > np.sum(red) and np.sum(green) > np.sum(yellow):
            return True
        return False
