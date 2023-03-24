import cv2
import numpy as np
import matplotlib.pyplot as plt

## Load Image
left = cv2.imread("./stereo/left.png")
right = cv2.imread("./stereo/right.png")
depth_left = cv2.imread("./stereo/left_disp.png", cv2.IMREAD_GRAYSCALE)

## Define parameter //https://github.com/YuhuaXu/StereoDataset
pixel_length = 3.75e-6
base = 5e-2
focal = 8e-3
## Feature match
# Extract feature
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(left, None)
kp2, des2 = orb.detectAndCompute(right, None)
# Match
bf = cv2.BFMatcher(cv2.NORM_HAMMING, True)
matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda x: x.distance)[:30]

img3 = cv2.drawMatches(depth_left, kp1, right, kp2, matches, flags=2, outImg=None)
plt.imshow(img3), plt.show()
# Convert point to numpy
best_kp1 = []
best_kp2 = []
best_matches = []
for match in matches:
    best_kp1.append(kp1[match.queryIdx].pt)
    best_kp2.append(kp2[match.trainIdx].pt)
    best_matches.append(match)
best_kp1 = np.array(best_kp1)
best_kp2 = np.array(best_kp2)
best_matches = np.array(best_matches)

## Calculate depth /https://docs.opencv.org/4.5.5/dd/d53/tutorial_py_depthmap.html
best_depth = []
gd = []
for i in range(len(best_kp1)):
    xl = best_kp1[i][0]
    xr = best_kp2[i][0]
    depth = focal * base / ((xl - xr) * pixel_length)
    gd.append(depth_left[int(best_kp1[i][0]), int(best_kp1[i][1])] / 100)
    best_depth.append(depth)

best_depth = np.asarray(best_depth)
print(best_depth)
gd = np.asarray(gd)
print(gd - best_depth)
# img3 = cv2.drawMatches(left,kp1,right,kp2, matches, flags=2, outImg = None)
# plt.imshow(img3), plt.show()
