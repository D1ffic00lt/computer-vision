import os
import time
import logging
import warnings

import cv2
import numpy as np

from typing import Any, Union, Tuple

connect_pigpio = True

try:
    import pigpio as pigpio
except ImportError:
    pigpio: Any
    connect_pigpio = False


class Controller(object):
    P = 0.35
    D = 0.1
    ESC = 17
    STEER = 18
    ESCAPE = 27
    STOP_LINE_PIXELS_COUNT = 10000000
    ROAD_PIXELS_COUNT = 1600000
    SIZE = (533, 300)
    RECT = np.float32([[0, SIZE[1]], [SIZE[0], SIZE[1]], [SIZE[0], 0], [0, 0]])
    TRAP = np.float32([[10, 299], [523, 299], [440, 200], [93, 200]])
    SRC_DRAW = np.array(TRAP, dtype=np.int32)

    def __init__(
            self, speed: int = 1560, camera: Union[str, int] = 0,
            show_results: bool = False, control_car: bool = True,
            show_angel: bool = False, ignore_warnings: bool = True,
            stop_before_stop_line: bool = False
    ) -> None:
        self.pi: Any
        self.speed = speed
        if connect_pigpio:
            if not control_car and not ignore_warnings:
                logging.warning("connect_pigpio == True but control_car = False")
            self.pi = self.setup_gpio()
            self.control(90, 1500)
        else:
            if control_car and not ignore_warnings:
                logging.warning("connect_pigpio == False but control_car = True")
        self.control_car = control_car and connect_pigpio
        self.show_angel = show_angel
        self.show_results = show_results
        self.stop_before_stop_line = stop_before_stop_line

        self._angle = 90
        self._ignore_warnings: bool
        self.ignore_warnings = ignore_warnings

        self._camera = cv2.VideoCapture(camera)

        self._in_crossroads = False

    def setup_gpio(self) -> Any:
        os.system("sudo pigpiod")
        time.sleep(1)
        pi = pigpio.pi()
        pi.set_servo_pulsewidth(self.ESC, 0)
        pi.set_servo_pulsewidth(self.STEER, 0)
        time.sleep(1)
        return pi

    def control(self, angle: int, speed: int = None) -> None:
        if self.control_car:
            self.pi.set_servo_pulsewidth(self.ESC, self.speed if speed is None else speed)
            self.pi.set_servo_pulsewidth(self.STEER, int(11.1 * angle + 500))

    def _run(self) -> None:
        status, frame = self._camera.read()
        total_error = self._read_frame(frame, return_only_error=True) if status else 0
        key = 1
        while key != self.ESCAPE:
            self.angel = 90
            status, frame = self._camera.read()
            if not status:
                print("No video")
                time.sleep(1)
                continue

            if self._in_crossroads:
                if self._read_frame(frame, return_only_pixels_count=True) > self.ROAD_PIXELS_COUNT:
                    self._in_crossroads = False
                    continue
                self.control(90)

            previous_error = total_error

            hist, mid, left, right, total_error, stop_line = self._read_frame(frame)

            if stop_line and self.control_car:
                self._in_crossroads = True
                if self.stop_before_stop_line:
                    self.control(90, 1500)
                    time.sleep(5)
                continue

            self.angel = self._calculate_angel(self.angel, total_error, previous_error)

            if self.control_car:
                self.control(self.angel)

            if self.show_results:
                key = cv2.waitKey(50)

            if self.show_angel:
                print(self.angel)

    def _calculate_angel(self, angel, total_error, previous_error) -> int:
        return angel - int(self.P * (total_error + (total_error - previous_error) * self.D))

    def _read_frame(
            self, frame: np.ndarray, return_only_error: bool = False,
            return_only_pixels_count: bool = False
    ) -> Tuple[np.ndarray, int, int, int, Union[int, float], bool]:
        stop_line = False
        img = cv2.resize(frame, self.SIZE)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary = cv2.inRange(gray, 180, 255)

        matrix_trans = cv2.getPerspectiveTransform(self.TRAP, self.RECT)
        perspective = cv2.warpPerspective(binary, matrix_trans, self.SIZE, flags=cv2.INTER_LINEAR)
        trap_visual = cv2.drawContours(binary.copy(), [self.SRC_DRAW], -1, 150, thickness=3)

        hist = np.sum(perspective, axis=0)
        mid = hist.shape[0] // 2
        left = np.argmax(hist[:mid])
        right = np.argmax(hist[mid:]) + mid

        total_error = (left + right) // 2 - mid

        if return_only_error:
            return total_error

        if self.show_results:
            cv2.imshow("frame", frame)
            cv2.imshow("binary", binary)
            cv2.imshow("trap_vis", trap_visual)
            cv2.imshow("perspective", perspective)

            cv2.line(perspective, (left, 0), (left, self.SIZE[1]), 50, 2)
            cv2.line(perspective, (right, 0), (right, self.SIZE[1]), 50, 2)

            cv2.imshow('lines', perspective)

        if return_only_pixels_count:
            return np.sum(perspective)
        print(np.sum(perspective))
        if np.sum(perspective) > 10000000:
            stop_line = True

        return hist, mid, left, right, total_error, stop_line

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, value: Union[int, str]):
        self._camera = cv2.VideoCapture(value)

    @property
    def angel(self) -> int:
        return self._angle

    @angel.setter
    def angel(self, value: int) -> None:
        if value > 110:
            self._angle = 110
        elif value < 70:
            self._angle = 70
        else:
            self._angle = int(value)

    @property
    def ignore_warnings(self):
        return self._ignore_warnings

    @ignore_warnings.setter
    def ignore_warnings(self, value):
        self._ignore_warnings = value
        if value:
            warnings.filterwarnings("ignore")
        else:
            warnings.filterwarnings("default")

    def __call__(self) -> None:
        try:
            self._run()
        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            self._camera.release()
            self.control(90, 1500)


if __name__ == "__main__":
    controller = Controller()
    controller.camera = "../output1280.avi"
    controller.show_results = True
    controller.show_angel = True
    controller()
