import math
import cv2
import mediapipe as mp

LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]


def check_list(data: list):
    count = 0
    last_value = data[0]
    for j in data:
        if j == 1 and last_value != j:
            count += 1
        last_value = j
    return count


# расчёт дистанции между двумя точками на декартовой плоскости
def euclidean_distance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
    return distance


# рассчёт отношения вертикального и горизонтального размера глаза,
# для левого и правого глаз
# возвращает среднее арифметическое для двух глаз
def blink_ratio(img, landmarks, right_indices, left_indices, draw=True):
    # RIGHT EYE
    # horizontal line
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]

    # vertical line
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]

    # draw lines on right eyes
    if draw:
        cv2.line(img, rh_right, rh_left, (0, 255, 0), 2)
        cv2.line(img, rv_top, rv_bottom, (255, 0, 0), 2)

    # LEFT_EYE
    # horizontal line
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]

    # vertical line
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    rh_distance = euclidean_distance(rh_right, rh_left)
    rv_distance = euclidean_distance(rv_top, rv_bottom)

    lv_distance = euclidean_distance(lv_top, lv_bottom)
    lh_distance = euclidean_distance(lh_right, lh_left)

    re_ratio = rv_distance / rh_distance
    le_ratio = lv_distance / lh_distance

    ratio = (re_ratio + le_ratio) / 2
    return ratio


mp_drawing = mp.solutions.drawing_utils  # Утилиты MediaPipe для рисования лица, рук и тд
mp_face_mesh = mp.solutions.face_mesh  # Утилиты MediaPipe для работы с лицом: нахождения лица, точек на лице и тд
mp_hands = mp.solutions.hands  # Утилиты MediaPipe для работы с руками: нахождение рук, точек на руках и тд
mp_drawing_styles = mp.solutions.drawing_styles  # Утилиты MediaPipe с готовыми стилями рисования

face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True)
print("Done")

blinking = []
cam = cv2.VideoCapture(0)
key = 0
while key != 27:
    ret, frame = cam.read()
    if ret:
        # frame = cv2.resize(frame, (0, 0), None, 0.5, 0.5)
        # cv2.imshow("Frame", frame)

        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        annotated_image = frame.copy()
        face_landmarks = results.multi_face_landmarks[0]

        # рисование сетки, соединяющей ключевые точки
        mp_drawing.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())

        # рисование серого контура лица и обводки глаз и бровей
        mp_drawing.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())

        # рисование обводки зрачков
        mp_drawing.draw_landmarks(
            image=annotated_image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_iris_connections_style())

        # выводим изображение с отрисованной сеткой
        # cv2.imshow('DetectFace', annotated_image)

        frame_w, frame_h = frame.shape[:2]

        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        eyes_image = frame.copy()

        face_landmarks = results.multi_face_landmarks[0]

        # пересчитываем координаты точек в координаты пикселей для всех найденных точек
        landmarks_coords = [(int(landmark.x * frame_w),
                             int(landmark.y * frame_h)) for landmark in face_landmarks.landmark
                            ]

        # вызываем функцию рассчёта отношения для глаз
        eyes_ratio = blink_ratio(eyes_image, landmarks_coords, LEFT_EYE, RIGHT_EYE)

        # print('Eyes Ratio:', round(eyes_ratio, 2))
        if eyes_ratio > 0.17:  # измените значение порога на то,
            # которое вы определили экспериментально
            # print('Глаза открыты!')
            blinking.append(0)
        else:
            # print('Глаза закрыты!')
            blinking.append(1)
        if len(blinking) == 15:
            print(check_list(blinking))
            blinking = []
        #
#         # cv2.imshow('Eyes Detect', eyes_image)

        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        point_eyes_frame = frame.copy()

        frame_h, frame_w = point_eyes_frame.shape[:2]

        face_landmarks = results.multi_face_landmarks[0]

        # перебираем индексы в списке для правого глаза
        for i, landmark_idx in enumerate(RIGHT_EYE):
            landmark = face_landmarks.landmark[landmark_idx]

            # пересчитываем координаты ключевых точек в
            # координаты соответствующих точкам пикселей пикселей
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            if i in (0, 4, 8, 12):  # эти точки рисуем зелёным цветом
                color = (0, 255, 0)
            else:  # остальные красным
                color = (0, 0, 255)

            cv2.circle(point_eyes_frame, (x, y), 3, color, -1)
        for i, landmark_idx in enumerate(LEFT_EYE):
            landmark = face_landmarks.landmark[landmark_idx]

            # пересчитываем координаты ключевых точек в
            # координаты соответствующих точкам пикселей пикселей
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            if i in (0, 4, 8, 12):  # эти точки рисуем зелёным цветом
                color = (0, 255, 0)
            else:  # остальные красным
                color = (0, 0, 255)

            cv2.circle(point_eyes_frame, (x, y), 3, color, -1)

        # cv2.imshow('point_eyes_frame', point_eyes_frame)
    else:
        print('end of video')

    key = cv2.waitKey(1)

cam.release()
cv2.destroyAllWindows()
