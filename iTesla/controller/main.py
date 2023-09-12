import os
import time
import logging
import warnings
import cv2
import numpy as np

from typing import Any, Union

from traffic_lights import TrafficLightDetector

connect_pigpio = True

try:
    import pigpio as pigpio
except ImportError:
    pigpio: Any
    connect_pigpio = False


class Controller(object):
    P = 0.38
    D = 0.17
    ESC = 17
    STEER = 18
    ESCAPE = 27
    STOP_AT_THE_TRAFFIC_LINE = 19_000_000
    THE_TRAFFIC_LINE_WITH_PEDESTRIAN_PIXELS_COUNT = 17_500_000
    STOP_LINE_PIXELS_COUNT = 7_000_000
    ROAD_PIXELS_COUNT = 2_300_000
    SIZE = (533, 300)
    RECT = np.float32([[0, SIZE[1]], [SIZE[0], SIZE[1]], [SIZE[0], 0], [0, 0]])
    TRAP = np.float32([[10, 299], [523, 299], [440, 200], [93, 200]])
    SRC_DRAW = np.array(TRAP, dtype=np.int32)

    def __init__(
            self, detector_cfg_path: str, detector_weights_path: str,
            camera: Union[str, int] = 0, speed: int = 1550,
            show_results: bool = False, control_car: bool = True,
            show_angel: bool = False, ignore_warnings: bool = False,
            stop_before_stop_line: bool = False, stop_at_traffic_light: bool = True,
            roads: list = None, do_count: bool = False, to_left: bool = False,
            stop_in_front_of_pedestrians: bool = False, stop_line_stop_time: int = 5
    ) -> None:
        self.pi: Any = object()
        self.crossroads_count = 0
        self.model = TrafficLightDetector(detector_weights_path, detector_cfg_path)
        self.speed = speed
        self.do_count = do_count
        self.to_left = to_left
        self.show_angel = show_angel
        self.show_results = show_results
        self.stop_line_stop_time = stop_line_stop_time
        self.stop_before_stop_line = stop_before_stop_line
        self.stop_at_traffic_light = stop_at_traffic_light
        self.stop_in_front_of_pedestrians = stop_in_front_of_pedestrians
        self.control_car = control_car and connect_pigpio
        self.roads = [] if roads is None else roads
        self.crossroads_count = 0

        if roads:
            for road in enumerate(roads):
                try:
                    print(f"road: {road[0]} - {self.moves_count(cv2.imread(road[1]))}")
                except AttributeError:
                    print(f"road: {road[0]} - image not found")
        if do_count:
            index = int(input("Enter index: "))
            self.max_count = self.moves_count(cv2.imread(roads[index]))
        else:
            self.max_count = float("inf")

        if connect_pigpio:
            self.pi = self.setup_gpio()
            self.control(90, 1500)

        self._angle = 90
        self._ignore_warnings: bool = False
        self.ignore_warnings = ignore_warnings

        self._camera = cv2.VideoCapture(camera)

        self._in_crossroads = False
        self._stop = False

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

            if self._in_crossroads:
                for i in range(5):  # ping fix
                    status, frame = self._camera.read()
            else:
                status, frame = self._camera.read()

            if not status:
                print("Video stream not available")
                time.sleep(1)
                continue

            if self._in_crossroads:
                # remove this "if" if the pedestrian stop doesn't work
                if self.STOP_LINE_PIXELS_COUNT > \
                        self._read_frame(frame, return_only_pixels_count=True) > self.ROAD_PIXELS_COUNT:
                    self._in_crossroads = False

                    self.crossroads_count += 1
                    if self.crossroads_count == self.max_count:
                        self.control(90, 1500)
                    continue

                if not self._stop:
                    self.control(90)
                continue

            previous_error = total_error

            hist, mid, left, right, total_error, stop_line = self._read_frame(frame)

            if stop_line:
                self._in_crossroads = True

                time.sleep(0.15)

                if self.stop_in_front_of_pedestrians:
                    pixels = self._read_frame(frame, return_only_pixels_count=True)

                    if self.THE_TRAFFIC_LINE_WITH_PEDESTRIAN_PIXELS_COUNT < pixels < self.STOP_AT_THE_TRAFFIC_LINE:
                        self.control(90)
                        time.sleep(0.3)
                        self._traffic_controller()
                        self.control(90)
                        time.sleep(0.2)
                        self._stop = False
                        self._in_crossroads = False
                        continue

                if self.stop_before_stop_line:
                    self.control(90, 1500)

                    if not self.stop_at_traffic_light:
                        #  bad implementation...
                        if self.to_left:
                            self.control(90)
                            time.sleep(0.3)
                            self.control(110)
                            time.sleep(2)
                            continue

                        time.sleep(self.stop_line_stop_time)

                        continue

                    # ping fix
                    for i in range(5):
                        status, frame = self._camera.read()

                    self._traffic_lights_controller()
                continue

            self.angel = self._calculate_angel(self.angel, total_error, previous_error)

            if self.control_car and not self._in_crossroads:
                self.control(self.angel)

            if self.show_results:
                key = cv2.waitKey(50)

            if self.show_angel:
                print(self.angel)

            if self.crossroads_count == self.max_count:
                self.control(90)

                time.sleep(0.2)

                self.control(90, 1500)
                break

            self.crossroads_count += 1

    def _traffic_lights_controller(self):
        total_light = False

        while not total_light:
            status, frame = self._camera.read()

            if not status:
                print("Video stream not available")
                time.sleep(0.3)
                continue
            try:
                total_light = self.model.check_traffic_color(frame)
            except Exception as ex:
                print(ex)

    def _traffic_controller(self):
        self._stop = True

        self.control(90, 1500)

        total_light = False

        while not total_light:
            status, frame = self._camera.read()

            if not status:
                print("Video stream not available")
                time.sleep(0.3)
                continue
            try:
                pixels = self._read_frame(frame, return_only_pixels_count=True)

                if pixels < self.STOP_LINE_PIXELS_COUNT / 2:
                    total_light = True
                if self.STOP_AT_THE_TRAFFIC_LINE > pixels > self.STOP_AT_THE_TRAFFIC_LINE:
                    total_light = True
            except Exception as ex:
                print(ex)

    def _calculate_angel(self, angel, total_error, previous_error) -> int:
        return angel - int(self.P * (total_error + (total_error - previous_error) * self.D))

    def _read_frame(
            self, frame: np.ndarray, return_only_error: bool = False,
            return_only_pixels_count: bool = False
    ) -> Any:
        stop_line = False
        img = cv2.resize(frame, self.SIZE)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary = cv2.inRange(gray, 220, 255)

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

        if np.sum(perspective) > self.STOP_LINE_PIXELS_COUNT:
            stop_line = True

        return hist, mid, left, right, total_error, stop_line

    @staticmethod
    def moves_count(img: np.ndarray) -> int:
        img = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))
        first_image, second_image = img[:, :img.shape[1] // 2], img[:, img.shape[1] // 2:]
        bin_data = [[(0, 17, 47), (59, 38, 255)], [(87, 17, 62), (255, 73, 64)]]

        result = []

        for i in bin_data:
            lower, high = i
            first_bin = cv2.inRange(first_image, lower, high)
            second_bin = cv2.inRange(second_image, lower, high)

            result.append([np.sum(first_bin), np.sum(second_bin)])

        result = [i.index(max(i)) for i in result]

        return 1 if result[0] != result[1] else 2

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
        if self.control_car and not self.ignore_warnings:
            logging.warning("connect_pigpio == False but control_car = True")
        try:
            self._run()
        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            self._camera.release()
            self.control(90, 1500)


if __name__ == "__main__":
    controller = Controller(
        detector_cfg_path="./yolov4-tiny-obj.cfg",
        detector_weights_path="./yolov4-tiny-obj_best.weights"
    )

    controller.stop_at_traffic_light = False  # FIXME
    controller.stop_before_stop_line = True
    controller.stop_in_front_of_pedestrians = True
    controller.speed = 1550
    controller.show_results = False
    controller.show_angel = True
    controller.to_left = False
    # controller.control_car = True
    controller()
