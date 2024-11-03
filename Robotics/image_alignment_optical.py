import numpy as np
from matplotlib import pyplot as plt
from skimage.color import rgb2gray
from skimage.data import stereo_motorcycle, vortex
from skimage.transform import warp
from skimage.registration import optical_flow_tvl1, optical_flow_ilk
import skimage
import cv2

# --- Load the sequence
image_path = "./data/left1p5.jpeg"
template_path = "./data/template.jpeg"
# image0, image1, disp = stereo_motorcycle()
image1 = skimage.io.imread(image_path)
image0 = skimage.io.imread(template_path)
# downsize the images for faster computation
image0 = skimage.transform.resize(
    image0, (image0.shape[0] // 4, image0.shape[1] // 4), anti_aliasing=True
)
image1 = skimage.transform.resize(
    image1, (image1.shape[0] // 4, image1.shape[1] // 4), anti_aliasing=True
)
print(f"Image0 shape: {image0.shape}")
image0_backup = image0.copy()
image1_backup = image1.copy()
# --- Convert the images to gray level: color is not supported.
image0 = rgb2gray(image0)
image1 = rgb2gray(image1)

# --- Compute the optical flow
v, u = optical_flow_ilk(image0, image1, radius=10, num_warp=20, gaussian=True)

# --- Use the estimated optical flow for registration

nr, nc = image0.shape

row_coords, col_coords = np.meshgrid(np.arange(nr), np.arange(nc), indexing="ij")

for color_channel in range(3):
    image1_warp = warp(
        image1_backup[..., color_channel],
        np.array([row_coords + v, col_coords + u]),
        mode="constant",
    )
    image1_backup[..., color_channel] = image1_warp
# image1_warp = warp(image1, np.array([row_coords + v, col_coords + u]), mode="edge")

# --- Show the result
overly = image0_backup.copy()
output = image1_backup.copy()
cv2.addWeighted(overly, 0.5, output, 0.5, 0, output)
plt.imshow(image1_backup)
plt.title("Registered sequence")
plt.show()
# fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(5, 10))

# ax0.imshow(seq_im)
# ax0.set_title("Unregistered sequence")
# ax0.set_axis_off()

# ax1.imshow(reg_im)
# ax1.set_title("Registered sequence")
# ax1.set_axis_off()

# ax2.imshow(target_im)
# ax2.set_title("Target")
# ax2.set_axis_off()

# fig.tight_layout()
# plt.show()
