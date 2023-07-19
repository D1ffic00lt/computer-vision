# -*- coding: utf-8 -*-
import pickle
import cv2


# TODO: Допишите импорт библиотек, которые собираетесь использовать

def intersection(user_box, true_box):
    x, y, w, h = user_box
    user_box = (x, y, x + w, y + h)

    x, y, w, h = true_box
    true_box = (x, y, x + w, y + h)

    x1 = max(user_box[0], true_box[0])
    y1 = max(user_box[1], true_box[1])
    x2 = min(user_box[2], true_box[2])
    y2 = min(user_box[3], true_box[3])

    inter_area = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)

    box1_area = (user_box[2] - user_box[0] + 1) * (user_box[3] - user_box[1] + 1)
    box2_area = (true_box[2] - true_box[0] + 1) * (true_box[3] - true_box[1] + 1)
    iou = inter_area / float(box1_area + box2_area - inter_area)
    return not (iou == 0)


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
    nuts = {}
    result = []  # пустой список для засенения результата
    double = False
    while True:  # цикл чтения кадров из видео
        status, frame = video.read()  # читаем кадр
        if not status:  # выходим из цикла, если видео закончилось
            break
        frame = cv2.resize(frame, (640, 360))
        frame = frame[:, 70:-70]
        h, w = frame.shape[:2]
        frame = cv2.flip(frame, 0)
        frame = cv2.GaussianBlur(frame, (3, 3), 1)

        start_zone = int(h * 0.25)
        end_zone = int(h * 0.75)

        binary = cv2.inRange(frame, (0, 0, 0), (100, 100, 100))
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, (255, 0, 0), 2)
        if contours:
            # contours = sorted(contours, key=cv2.contourArea, reverse=True)[1:]
            for i in contours:
                bbox_x, bbox_y, bbox_w, bbox_h = cv2.boundingRect(i)
                if bbox_y >= start_zone and bbox_y + bbox_h < end_zone:
                    cv2.rectangle(frame, (bbox_x, bbox_y), (bbox_x + bbox_w, bbox_y + bbox_h), (255, 0, 0), 1)
                else:
                    cv2.rectangle(frame, (bbox_x, bbox_y), (bbox_x + bbox_w, bbox_y + bbox_h), (0, 255, 0), 1)

        cv2.line(frame, (0, start_zone), (w, start_zone), (0, 0, 255), 1)
        cv2.line(frame, (0, end_zone), (w, end_zone), (0, 0, 255), 1)
        cv2.imshow("Frame", frame)
        cv2.imshow("python_binary", binary)
        key = cv2.waitKey(10)
        if key == 27:
            break
    return result  # возвращаем полученный список
