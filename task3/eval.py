# -*- coding: utf-8 -*-
import pickle
import warnings
import numpy as np
import torch

from sklearn.preprocessing import LabelEncoder

from model import SimpleCnn
from dataloader import ImagesDataset

warnings.filterwarnings("ignore")

# TODO: Допишите импорт библиотек, которые собираетесь использовать

with open("label_encoder.pkl", "rb") as file:
    encoder: LabelEncoder = pickle.load(file)


def predict_one_sample(model, inputs):
    """Предсказание, для одной картинки"""
    dataset = ImagesDataset(inputs)
    with torch.no_grad():
        model.eval()
        logit = model(dataset[0].unsqueeze(0)).cpu()
        probs = torch.nn.functional.softmax(logit, dim=-1).numpy()
        y_pred = np.argmax(probs, -1)
    return y_pred


def load_models():
    """ Функция осуществляет загрузку модели(ей) нейросети(ей) из файла(ов).
        Выходные данные: загруженный(е) модели(и)

        Если вы не собираетесь использовать эту функцию, пусть возвращает пустой список []
        Если вы используете несколько моделей, возвращайте их список [model1, model2]

        То, что вы вернёте из этой функции, будет передано вторым аргументом в функцию predict_sign()
    """

    # TODO: Отредактируйте функцию по своему усмотрению.
    # Модель нейронной сети, загрузите на онайн-платформу вместе с eval.py.

    # Пример загрузки моделей из файлов
    # Yolo-модели
    # net = cv2.dnn.readNetFromDarknet('yolo.cfg', 'yolo.weights')
    # yolo_model = cv2.dnn_DetectionModel(net)
    # yolo_model.setInputParams(scale=1/255, size=(416, 416), swapRB=True)
    # models = [yolo_model]

    # Пример загрузки модели TensorFlow (не забудьте импортировать библиотеку tensorflow)
    # tf_model = tf.keras.models.load_model('model.h5')
    # models.append(tf_model)
    # models = [yolo_model]
    model = SimpleCnn(8)
    model.load_state_dict(torch.load("./model.pth", map_location=torch.device('cpu')))
    model.eval()
    models = [model]

    return models


def predict_sign(image, models) -> str:
    """
        Функция для классификации знаков дорожного движения.

        Входные данные: Входные данные: изображение (bgr), прочитано cv2.imread
        Выходные данные: название знака дорожного движения, str
            Примечание: Дорожный знак на изображение всегда ровно один!

        Всевозможные названия знаков дорожного движения:
            artificial_roughness
            give_way
            movement_prohibition
            no_entry
            parking
            pedestrian_crossing
            road_works
            stop

        Примеры вывода:
            "artificial_roughness"

            "road_works"

    """

    # TODO: Отредактируйте эту функцию по своему усмотрению.
    # Для удобства можно создать собственные функции в этом файле.
    # Алгоритм проверки один раз вызовет функцию load_models()
    # и для каждого тестового изображения будет вызывать функцию predict_sign()
    # Все остальные функции должны вызываться из вышеперечисленных.

    my_model = models[0]
    # image = np.expand_dims(image)
    output = predict_one_sample(my_model, image)
    # label = interpreter_output(output) # интерпретируйте вывод модели и получите тесктовое название знака
    return str([encoder.classes_[i] for i in output][0])

