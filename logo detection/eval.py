# -*- coding: utf-8 -*-
from typing import Tuple
import cv2
import dlib
import numpy as np
# TODO: Импортируйте библиотеки, которые собираетесь использовать


def detect_logo(image) -> Tuple[str, Tuple]:
    """
        Функция для детектирования логотипов

        Входные данные: изображение (bgr), прочитано cv2.imread
        Выходные данные: кортеж (Tuple) с названием логотипа и координатами ограничивающей рамки
            (label, (x, y, w, h)),
                где label - строка с названием логотипа;
                x, y - целочисленные координаты левого верхнего угла рамки, ограничивающей логотип;
                w, h - целочисленные ширина и высота рамки, ограничивающей логотип.

        Примечание: Логотип на изображение всегда ровно один!

        Возможные название логотипов:
            cpp, avt, python, altair, kruzhok.

        Примеры вывода:
            ('cpp', (12, 23, 20, 20))

            ('avt', (403, 233, 45, 60))
    """

    # TODO: Отредактируйте эту функцию по своему усмотрению.
    # Для удобства можно создать собственные функции в этом файле.
    # Алгоритм проверки будет вызывать функцию detect_logo, остальные функции должны вызываться из неё.
    detector_altair = dlib.simple_object_detector("./Detector_altair.svm")
    detector_avt = dlib.simple_object_detector("./Detector_avt.svm")
    detector_cpp = dlib.simple_object_detector("./Detector_cpp.svm")
    detector_kruzhok = dlib.simple_object_detector("./Detector_kruzhok.svm")
    detector_python = dlib.simple_object_detector("./Detector_python.svm")

    result = {"name": "", "boxes": [0, 0, 0, 0]}
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes_altair = detector_altair(frame)
    boxes_avt = detector_avt(frame)
    boxes_cpp = detector_cpp(frame)
    boxes_kruzhok = detector_kruzhok(frame)
    boxes_python = detector_python(frame)

    if boxes_altair:
        result["name"] = "altair"
        result["boxes"] = (
            boxes_altair[0].left(), boxes_altair[0].top(),
            boxes_altair[0].right(), boxes_altair[0].bottom()
        )
    elif boxes_avt:
        result["name"] = "avt"
        result["boxes"] = (
            boxes_avt[0].left(), boxes_avt[0].top(),
            boxes_avt[0].right(), boxes_avt[0].bottom()
        )
    elif boxes_cpp:
        result["name"] = "cpp"
        result["boxes"] = (
            boxes_cpp[0].left(), boxes_cpp[0].top(),
            boxes_cpp[0].right(), boxes_cpp[0].bottom()
        )
    elif boxes_python:
        result["name"] = "python"
        result["boxes"] = (
            boxes_python[0].left(), boxes_python[0].top(),
            boxes_python[0].right(), boxes_python[0].bottom()
        )
    elif boxes_kruzhok:
        result["name"] = "kruzhok"
        result["boxes"] = (
            boxes_kruzhok[0].left(), boxes_kruzhok[0].top(),
            boxes_kruzhok[0].right(), boxes_kruzhok[0].bottom()
        )

    x1, y1, x2, y2 = result["boxes"]
    # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # cv2.imshow("frame", frame)
    # cv2.waitKey(0)
    return result["name"], (x1, y1, x2 - x1, y2 - y1)
