# Script to process an image of a colony of bacteria
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

THRESHOLD = 30
BRIGHTNESS_SCALE = 1
NAME = "40Cd"
# Set working directory
working_directory = "/Users/hu/Downloads/yck"
os.chdir(working_directory)

# load the ROI list
roi_list = np.load(f"{NAME}_add_roi.npy")

# Load the original image
original_image = cv2.imread(f"{NAME}_processed_sharp.png", cv2.IMREAD_GRAYSCALE)
image_height, image_width = original_image.shape

# Load the new image
grayscale_image = cv2.imread(f"{NAME}.png", cv2.IMREAD_GRAYSCALE)
## add some random noise

# Apply a Gaussian blur to the grayscale image
grayscale_blurred = cv2.GaussianBlur(grayscale_image, (3, 3), 0)

# Create a background mask by thresholding the blurred grayscale image (pixels below 60 are considered background)
_, background_mask = cv2.threshold(grayscale_blurred, THRESHOLD, 255, cv2.THRESH_BINARY)
grayscale_image[background_mask == 0] = 0
grayscale_image = np.clip(
    grayscale_image.astype(float) * BRIGHTNESS_SCALE, 0, 255
).astype(np.uint8)

grayscale_blurred = cv2.GaussianBlur(grayscale_image, (3, 3), 0)
# blurred background mask
blurred_background_mask = cv2.GaussianBlur(background_mask, (3, 3), 0)
edge_mask = cv2.bitwise_and(
    (blurred_background_mask > 0).astype(int),
    (blurred_background_mask < 255).astype(int),
)

# grayscale_image[blurred_background_mask == 0] = 0
grayscale_image[edge_mask == 1] = grayscale_blurred[edge_mask == 1]

# Part II: add grayscale_image to original_image
num_rows = 10
row_height = image_height // num_rows
row_centers = row_height * 5 + row_height // 2
width_roi = roi_list[0]
block_width = int(width_roi[2] / 6)
start_col = width_roi[0]
col_center = [start_col + block_width * i + block_width // 2 for i in range(6)]


# select roi of the new image 6 times and add to the original image
for i in range(6):
    roi = roi_list[i + 1]
    x, y, w, h = roi
    original_image[
        row_centers - h // 2 : row_centers - h // 2 + h,
        col_center[i] - w // 2 : col_center[i] - w // 2 + w,
    ] = grayscale_image[y : y + h, x : x + w]


# create a new image, add a row height black in the center
new_image = np.zeros((image_height + row_height, image_width), dtype=np.uint8)
new_image[0 : image_height // 2, :] = original_image[0 : image_height // 2, :]
new_image[image_height // 2 + row_height :, :] = original_image[image_height // 2 :, :]
# save the new image
plt.imshow(new_image, cmap="gray")
plt.show()
cv2.imwrite(f"{NAME}_add.png", new_image)
