from PIL import Image, ExifTags
import numpy as np
import matplotlib.pyplot as plt
import glob


root = "/Users/hu/Downloads/all"
jpg_list = glob.glob(f"{root}/*.jpg")
print(len(jpg_list))


from collections import Counter

focal_counter = Counter()
device_counter = Counter()
for path in jpg_list:
    try:
        img = Image.open(path)
        focal_length = img._getexif()[41989]
        device_model = img._getexif()[272]

        # print(focal_length)
        focal_counter[focal_length] += 1
        device_counter[device_model] += 1
    except:
        pass


res = focal_counter.most_common(10)
print(f"focal length: {res}, total: {sum([x[1] for x in res])}")
for x in res:
    print(f"{x[0]}: {x[1]}")
