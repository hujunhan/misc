# Given a image with object, fill the object with another image
# random place the image in the object, size, angle, etc.

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image, with alpha channel
img_path = "/Users/hu/Downloads/IMG_4991.jpeg"
img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

# load fill image (transparent background), so the alpha channel is needed
fill_img_path = "/Users/hu/Downloads/tiger.webp"
fill_img = cv2.imread(fill_img_path, cv2.IMREAD_UNCHANGED)


# recognize the object using grabcut
mask = np.zeros(img.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
rect = (50, 50, 450, 290)
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
new_img = img * mask2[:, :, np.newaxis]

plt.imshow(new_img)
plt.show()

# fill the object with fill image, center in the mask area


# fill the unmasked background with original image
