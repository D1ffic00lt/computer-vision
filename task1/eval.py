# -*- coding: utf-8 -*-
import pickle
import cv2
import numpy as np


# TODO: Допишите импорт библиотек, которые собираетесь использовать

def detect_defective_parts(video) -> list:
    """
        Функция для детектирования бракованных гаек.

        Входные данные: объект, полученный cv2.VideoCapture, из объекта можно читать кадры методом .read
            На кадрах конвеер, транспортирующий гайки. Гайки перемещаются от нижней границы кадра к верхней.
            Некоторые гайки повреждены: не имеют центрального отверстия, сплющены, разорваны, деформированы.

        Выходные данные: list
            Необходимо вернуть список, состоящий из нулей и единиц, где 0 - гайка надлежащего качества,
                                                                        1 - бракованная гайка.
            Длина списка должна быть равна количеству гаек на видео.

        Примеры вывода:
            [0, 0, 0, 1] - первые 3 гайки целые, последняя - бракованная
            [1, 1, 1] - все 3 гайки бракованные
            [] - на видео не было гаек

    """
    # TODO: Отредактируйте эту функцию по своему усмотрению.
    # Для удобства можно создать собственные функции в этом файле.
    # Алгоритм проверки будет вызывать функцию detect_defective_parts, остальные функции должны вызываться из неё.
    with open("model4.pkl", "rb") as file:
        model = pickle.load(file)
    i = 0
    result = []  # пустой список для засенения результата
    double = False
    while True:  # цикл чтения кадров из видео
        status, frame = video.read()  # читаем кадр
        if not status:  # выходим из цикла, если видео закончилось
            break
        frame = cv2.resize(frame, (640, 360))
        frame = frame[320:, :]
        frame = cv2.blur(frame, (2, 2), 1)

        binary = cv2.inRange(frame, (80, 80, 80), (210, 210, 210))
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[1:]
            if len(contours) > 3:
                i = 0
            if contours:
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
                area = cv2.contourArea(contours[0])
                per = cv2.arcLength(contours[0], True)
                count = 0
                for contour in contours:
                    if cv2.arcLength(contour, True) < 60:
                        count += 1
                if count >= 2:
                    double = True
                else:
                    if double:
                        i = 0
                    double = False

                if per > 60 and i == 0 and not double:
                    apd = cv2.approxPolyDP(contours[0], 0.03 * per, True)
                    if len(contours) != 2:
                        result.append(
                            int(model.predict(np.array(
                                [[len(contours), len(apd), per, area, 0, 0]],
                                dtype=np.float16)
                            )[0])
                        )
                    else:
                        # FIXME: ужас...
                        result.append(int(model.predict(np.array(
                            [[
                                len(contours), len(apd), per, area,
                                cv2.contourArea(contours[1]), cv2.arcLength(contours[1], True)
                            ]], dtype=np.float16
                        ))[0]))
                    i = 1
            else:
                i = 0
        else:
            i = 0
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(50)
        if key == 27:
            break
    return result  # возвращаем полученный список
