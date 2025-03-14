# Script to process an image of a colony of bacteria
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

THRESHOLD = 50

# Set working directory
working_directory = "/Users/hu/Downloads/cleanCd"
os.chdir(working_directory)

# Load the original image
image_path = r"40Cd.jpg"
original_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
image_height, image_width, image_channels = original_image.shape

# Convert the image to grayscale and make a copy
grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
grayscale_copy = grayscale_image.copy()

# Apply a Gaussian blur to the grayscale image
grayscale_blurred = cv2.GaussianBlur(grayscale_image, (3, 3), 0)

# Create a background mask by thresholding the blurred grayscale image (pixels below 60 are considered background)
_, background_mask = cv2.threshold(grayscale_blurred, THRESHOLD, 255, cv2.THRESH_BINARY)

# Set the background areas to black in both the blurred image and the original grayscale copy
grayscale_blurred[background_mask == 0] = 0
grayscale_copy[background_mask == 0] = 0

# Create an empty image for placing the regions of interest (ROIs)
processed_image = np.zeros_like(grayscale_image)

# Load the list of ROIs from file
roi_list = np.load(image_path.replace(".jpg", "_roi.npy"))

# Define the layout: split the image into 10 rows.
# The ROIs will be placed in rows corresponding to these indices.
row_indices = [0, 1, 6, 2, 7, 3, 8, 4, 9]
num_rows = 10
row_height = image_height // num_rows
row_centers = [row_height * i + row_height // 2 for i in range(num_rows)]

# Assume all ROIs start at the same x-coordinate (use the first ROI's x-coordinate)
start_x = roi_list[0][0]

# Copy each ROI from the grayscale copy into the processed image,
# centering each ROI within its designated row.
for i, roi in enumerate(roi_list):
    print(f"Processing ROI {i}: {roi}")
    x, y, roi_width, roi_height = roi
    row_center = row_centers[row_indices[i]]
    processed_image[
        row_center - roi_height // 2 : row_center - roi_height // 2 + roi_height,
        start_x : start_x + roi_width,
    ] = grayscale_copy[y : y + roi_height, x : x + roi_width]

# Apply a Gaussian blur to the processed image for later use
blurred_processed_image = cv2.GaussianBlur(processed_image, (3, 3), 0)

# Generate a background mask for the processed image using thresholding
_, processed_background_mask = cv2.threshold(
    processed_image, THRESHOLD, 255, cv2.THRESH_BINARY
)
blurred_background_mask = cv2.GaussianBlur(processed_background_mask, (3, 3), 0)

# Initialize the final output image as a copy of the processed image
final_image = processed_image.copy()

# Detect edges by combining conditions on the blurred background mask
edge_mask = cv2.bitwise_and(
    (blurred_background_mask > 0).astype(int),
    (blurred_background_mask < 255).astype(int),
)

# Display the edge mask
plt.imshow(edge_mask, cmap="gray")
plt.title("Edge Mask")
plt.show()

# Replace pixels in the final image at edge locations with pixels from the blurred processed image
final_image[edge_mask == 1] = blurred_processed_image[edge_mask == 1]

# Display the final processed image
plt.imshow(final_image, cmap="gray")
plt.title("Final Processed Image")
plt.show()

# Save the final image with a modified filename
output_image_path = image_path.replace(".jpg", "_processed_sharp_t.png")
cv2.imwrite(output_image_path, final_image)
