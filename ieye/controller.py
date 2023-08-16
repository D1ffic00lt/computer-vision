import math
import cv2
import mediapipe as mp
import requests

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

        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        annotated_image = frame.copy()
        if not results.multi_face_landmarks:
            continue
        face_landmarks = results.multi_face_landmarks[0]
        frame_w, frame_h = frame.shape[:2]

        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        eyes_image = frame.copy()

        landmarks_coords = [(int(landmark.x * frame_w),
                             int(landmark.y * frame_h)) for landmark in face_landmarks.landmark
                            ]

        eyes_ratio = blink_ratio(eyes_image, landmarks_coords, LEFT_EYE, RIGHT_EYE)

        if eyes_ratio > 0.17:
            blinking.append(0)
        else:
            blinking.append(1)
        if len(blinking) == 25:
            value = check_list(blinking)
            print(value)
            if value != 0:
                response = requests.post("http://192.168.4.1:1664/app/api/v1.0/do/", json={"object": value})
            blinking = []
    else:
        print('end of video')

    key = cv2.waitKey(1)

cam.release()
cv2.destroyAllWindows()
