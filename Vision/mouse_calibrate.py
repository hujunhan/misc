import numpy as np
import cv2

# Predefined 3D feature point
feature_points_3d = np.asarray(
    [
        [-32.88, -2.972, 418.41],
        [-24.568, -8.0693, 411.53],
        [11.908, 67.794, 440.13],
        [18.432, 61.431, 440.37],
    ]
)
center_p = np.asarray([5.28968, 33.56337202, 423.57384865])
# mouse callback function
feature_points_2d = []
FEATURE_NUM = 4


def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 2, (255, 0, 0), -1)
        feature_points_2d.append([x, y])
        print(feature_points_2d)


# Create a black image, a window and bind the function to window
img = cv2.imread("pure_path.jpg")
cv2.namedWindow("image")
cv2.setMouseCallback("image", draw_circle)
while 1:
    cv2.imshow("image", img)
    if (cv2.waitKey(20) & 0xFF == 27) or len(feature_points_2d) == FEATURE_NUM:
        break
cv2.destroyAllWindows()


# Calculate the R,t
cam_intri = np.asarray([[1024, 0.0, 1024], [0, 1024, 1024], [0, 0, 1]])
dist = None
obj_points = feature_points_3d.astype(float) - center_p
img_points = np.asarray(feature_points_2d).astype(float)
cameraMatrix, rvec, tvec, x = cv2.solvePnPRansac(
    obj_points, img_points, cam_intri, dist
)
rot, jac = cv2.Rodrigues(rvec)

# Show info
print("Translation: ", tvec.T)
print("Rotation Matrix: ")
print(rot)
