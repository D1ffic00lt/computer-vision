# -*- coding: utf-8 -*-
from typing import Tuple
import cv2
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

    label = "avt"
    bbox = (233, 341, 372, 279)
    binary = cv2.inRange(image, (90, 90, 90), (210, 210, 210))
    cv2.imshow("binary", binary)

    cv2.waitKey(10000)
    contours = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
    for cont in contours:
        sm = cv2.arcLength(cont, True)
        apd = cv2.approxPolyDP(cont, 0.02 * sm, True)
        if len(apd) == 3:
            cv2.drawContours(image, [apd], -1, (0, 255, 0), 4)
    cv2.imwrite('result.jpg', image)
    return label, bbox
