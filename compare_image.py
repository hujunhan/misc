# scipt to compare two images
import cv2
import sys
import numpy as np


def compare_images(image_path1, image_path2):
    # Load images using OpenCV
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)
    print(np.max(img1 - img2))
    # Check if both images were loaded successfully
    if img1 is None or img2 is None:
        print("Error: One of the images did not load. Please check the file paths.")
        return False

    # Check if images have the same dimensions and number of channels
    if img1.shape != img2.shape:
        print("Images have different dimensions or channels.")
        return False

    # Compare the images using NumPy
    if np.array_equal(img1, img2):
        return True
    else:
        return False


if __name__ == "__main__":

    image1_path = r"/Users/hu/code/12bit_HCG_Pipe/031Test/result/S3_10.bmp"
    image2_path = r"/Users/hu/code/12bit_HCG_Pipe/031Test/result/S3_10_mid7.bmp"

    if compare_images(image1_path, image2_path):
        print("The images are identical (pixel-level).")
    else:
        print("The images are different (pixel-level).")
