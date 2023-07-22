import cv2
import os
import dlib

path = r"./"
detector_altair = dlib.simple_object_detector("./Detector_altair.svm")
detector_avt = dlib.simple_object_detector("./Detector_avt.svm")
detector_cpp = dlib.simple_object_detector("./Detector_cpp.svm")
detector_kruzhok = dlib.simple_object_detector("./Detector_kruzhok.svm")
detector_python = dlib.simple_object_detector("./Detector_python.svm")
images_names_list = os.listdir(path + "images/")

for file in images_names_list:
    result = {"name": "", "boxes": []}
    image = cv2.imread(path + "images/" + file)
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
    # print(result)
    x1, y1, x2, y2 = result["boxes"]
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.imshow("frame", frame)
    cv2.waitKey(0)
