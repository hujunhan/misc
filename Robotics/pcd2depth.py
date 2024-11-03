import numpy as np
import open3d as o3d
import cv2


def load_point_cloud(file_path):
    """
    Loads a point cloud from a PLY file.

    Args:
        file_path (str): Path to the PLY file.

    Returns:
        np.ndarray: Array of points with shape (N, 3), where N is the number of points.
    """
    pcd = o3d.io.read_point_cloud(
        file_path, remove_nan_points=False, remove_infinite_points=False
    )
    return np.asarray(pcd.points)


def point_cloud_to_depth_image(pcd_points, fx, fy, cx, cy, width, height):
    """
    Converts a point cloud to a depth image using given camera intrinsics.

    Args:
        points (np.ndarray): Array of points with shape (N, 3), where N is the number of points.
        fx (float): Focal length in the x direction.
        fy (float): Focal length in the y direction.
        cx (float): Principal point in the x direction.
        cy (float): Principal point in the y direction.
        width (int): Width of the depth image.
        height (int): Height of the depth image.

    Returns:
        np.ndarray: Depth image with shape (height, width).
    """
    # 点云反向映射到像素坐标位置
    u = np.round(pcd_points[:, 0] * fx / pcd_points[:, 2] + cx).astype(int)
    v = np.round(pcd_points[:, 1] * fy / pcd_points[:, 2] + cy).astype(int)

    # 滤除超出图像尺寸的无效像素
    valid = np.bitwise_and(
        np.bitwise_and((u >= 0), (u < width)), np.bitwise_and((v >= 0), (v < height))
    )
    u, v, z = u[valid], v[valid], pcd_points[:, 2][valid]

    # 按距离填充生成深度图，近距离覆盖远距离
    img_z = np.full((height, width), np.inf)
    for ui, vi, zi in zip(u, v, z):
        img_z[vi, ui] = min((img_z[vi, ui], zi))  # 近距离像素屏蔽远距离像素

    # print non-inf values's max and min
    print(np.max(img_z[img_z != np.inf]))
    # 小洞和“透射”消除
    img_z_shift = np.array(
        [
            img_z,
            np.roll(img_z, 1, axis=0),
            np.roll(img_z, -1, axis=0),
            np.roll(img_z, 1, axis=1),
            np.roll(img_z, -1, axis=1),
        ]
    )

    img_z = np.min(img_z_shift, axis=0)

    # depth_map_color_map = cv2.applyColorMap(img_z, cv2.COLORMAP_VIRIDIS)
    # depth_map_color_map = cv2.cvtColor(depth_map_color_map, cv2.COLOR_RGB2BGR)
    # depth_map_color_map[np.isnan(img_z)[:, :]] = 0
    # cv2.imwrite("depth_image.png", depth_map_color_map)
    # cv2.imshow("Depth Image", depth_map_color_map)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return img_z


def create_point_cloud_from_depth_image(depth, fx, fy, cx, cy, scale=1, organized=True):
    """Generate point cloud using depth image only.

    Input:
        depth: [numpy.ndarray, (H,W), numpy.float32]
            depth image
        camera: [CameraInfo]
            camera intrinsics
        organized: bool
            whether to keep the cloud in image shape (H,W,3)

    Output:
        cloud: [numpy.ndarray, (H,W,3)/(H*W,3), numpy.float32]
            generated cloud, (H,W,3) for organized=True, (H*W,3) for organized=False
    """
    assert depth.shape[0] == height and depth.shape[1] == width
    xmap = np.arange(width)
    ymap = np.arange(height)
    xmap, ymap = np.meshgrid(xmap, ymap)
    points_z = depth / scale
    points_x = (xmap - cx) * points_z / fx
    points_y = (ymap - cy) * points_z / fy
    # ignore invalid points
    valid = points_z != np.inf
    points_x = points_x[valid]
    points_y = points_y[valid]
    points_z = points_z[valid]
    cloud = np.stack([points_x, points_y, points_z], axis=-1)
    if not organized:
        cloud = cloud.reshape([-1, 3])
    return cloud


if __name__ == "__main__":
    fx, fy, cx, cy = (
        1783.40026855469,
        1782.84008789062,
        979.268188476562,
        586.475830078125,
    )
    width, height = 1944, 1200
    data_path = "./ref.ply"
    pcd_points = load_point_cloud(data_path)
    img_z = point_cloud_to_depth_image(pcd_points, fx, fy, cx, cy, width, height)
    pcd_origin = o3d.geometry.PointCloud()
    pcd_origin.points = o3d.utility.Vector3dVector(pcd_points)
    point_reconstructed = create_point_cloud_from_depth_image(
        img_z, fx, fy, cx, cy, scale=1, organized=False
    )
    pcd_reconstructed = o3d.geometry.PointCloud()
    pcd_reconstructed.points = o3d.utility.Vector3dVector(point_reconstructed)
    o3d.visualization.draw_geometries([pcd_reconstructed])
