# scipt to process image of colony of bacteria
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

root_path = "/Users/hu/Downloads/cleanCd"
os.chdir(root_path)
# Load image
img_path = r"5Cd.jpg"
img = cv2.imread(img_path, cv2.IMREAD_COLOR)

H, W, C = img.shape

# Convert to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
# Select background by thresholding the gray image, value<100
_, bg = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

# set the background to black
gray[bg == 0] = 0

# New image with pure background
new_img = np.zeros_like(gray)

# Use mouse to select the region of interest, 9 times, and save the region
# of interest to the new image
roi_list = []
for i in range(9):
    roi = cv2.selectROI("Select ROI", gray)
    x, y, w, h = roi
    roi_list.append(roi)

# Spilit the image into 10 rows, the 9 roi will be placed in the 1,2,3,4,5,7,8,9,10 row
# copy the roi to the new image, center the roi in the row
index_list = [0, 1, 2, 3, 4, 6, 7, 8, 9]
row = 10
row_height = H // row
row_center_list = [row_height * i + row_height // 2 for i in range(row)]
# all start with same x, the first roi's x is the all row's x
same_x = roi_list[0][0]
for i, roi in enumerate(roi_list):
    print(i, roi)
    x, y, w, h = roi
    new_img[
        row_center_list[index_list[i]]
        - h // 2 : row_center_list[index_list[i]]
        - h // 2
        + h,
        same_x : same_x + w,
    ] = gray[y : y + h, x : x + w]


# Display the new image
plt.imshow(new_img, cmap="gray")
plt.show()
# Save the new image, original name with _processed
cv2.imwrite(img_path.replace(".jpg", "_processed.bmp"), new_img)
# save the roi_list
np.save(img_path.replace(".jpg", "_roi.npy"), roi_list)
row_center_list[i] - h // 2
