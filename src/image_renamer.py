import os
from glob import glob

temp = glob("./data/*/*.png")
likes = glob("./data/dataset/like/*.png")
dislikes = glob("./data/dataset/dislike/*.png")

name = ""

count = 1
for image in temp:
    os.rename(image, f"./data/temp/{name}{count}.png")
    count += 1

for image in likes:
    os.rename(image, f"./data/dataset/like/{name}{count}.png")
    count += 1

for image in dislikes:
    os.rename(image, f"./data/dataset/dislike/{name}{count}.png")
    count += 1 