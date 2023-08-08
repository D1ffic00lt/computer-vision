import pandas as pd

from tqdm import tqdm

data = pd.read_csv("annotations.csv")

for i in tqdm(data.values):
    with open(f"{i[0].split('.')[:1][0] + '.txt'}", "+w") as file:
        file.write(" ".join(["light", str(i[1]), str(i[2]), str(i[3]), str(i[4])]))
