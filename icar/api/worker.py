import requests
import cv2
import mediapipe as mp
import pickle
import numpy as np

with open('comandsDetcet.bf', 'rb') as model:
    modelHands = pickle.load(model)


mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

WRIST = 0  # запястье
PALM_CENTER = 9  # центр ладони
THUMB = 4  # большой палец
INDEX = 8  # указательный палец
MIDDLE = 12  # средний палец
RING = 16  # безымянный палец
PINKY = 20  # мизинец


def catDetect(landmarks) -> str:
    # получаем координаты по y точек руки
    wrist_y = landmarks[WRIST].y
    palm_center_y = landmarks[PALM_CENTER].y
    thumb_y = landmarks[THUMB].y
    index_y = landmarks[INDEX].y
    middle_y = landmarks[MIDDLE].y
    ring_y = landmarks[RING].y
    pinky_y = landmarks[PINKY].y

    return modelHands.predict(np.array([wrist_y, palm_center_y, thumb_y, index_y, middle_y, ring_y, pinky_y]))


hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
cam = cv2.VideoCapture(0)
i = 0

while True:
    if i % 10 == 0:
        print(f"[INFO]: iteration {i}")
    ret, frame = cam.read()
    if ret:
        frame = cv2.resize(frame, (576, 416))

        image = frame.copy()

        image_h, image_w = image.shape[:2]

        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            for landmark_id, landmark in enumerate(hand_landmarks.landmark):
                x = int(landmark.x * image_w)
                y = int(landmark.y * image_h)

        image = frame.copy()

        image_h, image_w = image.shape[:2]

        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            gesture = catDetect(hand_landmarks.landmark)
            print(gesture[0])
            response = requests.post("http://192.168.4.1:1354/app/api/v1.0/do/", json={"object": gesture[0]})
    else:
        break
    i += 1
    # time.sleep(0.5)
