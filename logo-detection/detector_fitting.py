import cv2
import os
import dlib
import xml.etree.ElementTree as pars

path = r"./"

images = {"cpp": [], "python": [], "kruzhok": [], "altair": [], "avt": []}
anot = {"cpp": [], "python": [], "kruzhok": [], "altair": [], "avt": []}

images_names_list = os.listdir(path + "images/")
# print(images_names_list)

for file in images_names_list:
    image = cv2.imread(path + "images/" + file)
    # cv2.imshow("image", image)
    # cv2.waitKey(100)
    filename = file.split(".")[0]
    print(filename)
    xml = pars.parse(path + "anot/" + filename + ".xml")
    root = xml.getroot()
    value = root.find("object")

    for i in root.findall("object"):
        bbox = value.find("bndbox")

        x1 = int(bbox.find("xmin").text)
        y1 = int(bbox.find("ymin").text)
        x2 = int(bbox.find("xmax").text)
        y2 = int(bbox.find("ymax").text)

        source_image = image.copy()
        cv2.rectangle(source_image, (x1, y1), (x2, y2), (0, 200, 0))
        # cv2.imshow("image", source_image)
        # cv2.waitKey(0)

        images[value.find("name").text].append(image)
        anot[value.find("name").text].append([dlib.rectangle(left=x1, top=y1, right=x2, bottom=y2)])

for i in anot.keys():
    options = dlib.simple_object_detector_training_options()
    options.add_left_right_image_flips = False
    options.C = 5
    options.num_threads = 3
    options.be_verbose = True
    detector = dlib.train_simple_object_detector(images[i], anot[i], options)

    detector.save(f"Detector_{i}.svm")
    print(f"{i} Detector saved")
