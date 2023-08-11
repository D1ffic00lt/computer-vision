import cv2
import pandas as pd

from tqdm import tqdm

data = pd.read_csv("annotations.csv")

for i in tqdm(data.values):
    with open(f"{i[0].split('.')[:1][0] + '.txt'}", "+w") as file:
        img = cv2.imread(i[0])
        h, w = img.shape[:2]
        x, y, rw, rh = i[1], i[2], i[3], i[4]
        x += rw / 2
        y += rh / 2
        file.write(" ".join(["0", str(x / w), str(y / h), str(rw / w), str(rh / h)]))
