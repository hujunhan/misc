from skimage.transform import hough_line, hough_line_peaks
from skimage.feature import canny
from skimage.draw import line as draw_line
from skimage import data
import skimage
import matplotlib.pyplot as plt
from matplotlib import cm
from skimage.filters import threshold_yen, try_all_threshold
from skimage.morphology import remove_small_holes, remove_small_objects, closing, disk

import numpy as np

# Load the image
img_path = "/Users/hu/Downloads/油位/4B/4B/4B_2d.png"
image = skimage.io.imread(img_path, as_gray=True)

# convert the image to grayscale
# image = skimage.color.rgb2gray(image)

# # apply edge detection
# image = canny(image, sigma=2.0, low_threshold=0.0, high_threshold=0.2)

# try all thresholding


# # use yen thresholding
thresh = threshold_yen(image)
binary = image > thresh
plt.imshow(binary, cmap="gray")
plt.show()

# fill small areas
processed = remove_small_objects(binary, 300)
# plt.imshow(processed, cmap="gray")
# plt.show()

# closing
closed = closing(processed, disk(5))
plt.imshow(closed, cmap="gray")
plt.show()

# show the imageq
# plt.imshow(image)
# plt.show()
