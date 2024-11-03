import cv2
import open3d as o3d
import os
import numpy as np


def read_squares_from_txt(txt_file_path):
    squares = []

    with open(txt_file_path, "r") as file:
        for line in file:
            square_x1, square_y1, square_x2, square_y2 = map(int, line.strip().split())
            squares.append((square_x1, square_y1, square_x2, square_y2))

    return squares


def extract_square_regions(image, depth_image, pcd_cloud, squares):
    rgb_regions = []
    depth_regions = []
    ply_regions = []

    for square in squares:
        x1, y1, x2, y2 = square
        # 截取图像区域
        rgb_region = image[y1:y2, x1:x2]
        rgb_regions.append((rgb_region, square))

        depth_region = depth_image[y1:y2, x1:x2]
        depth_regions.append((depth_region, square))

        cloud_points = np.asarray(pcd_cloud.points).reshape(
            (image.shape[0], image.shape[1], 3)
        )
        panel_mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
        panel_mask[y1:y2, x1:x2] = 255
        panel_points = cloud_points[panel_mask > 0]

        panel_cloud = o3d.geometry.PointCloud()
        panel_cloud.points = o3d.utility.Vector3dVector(panel_points.astype(np.float32))
        panel_cloud.paint_uniform_color([1, 0, 0])
        ply_regions.append((panel_cloud, square))

    return rgb_regions, depth_regions, ply_regions


def save_regions(image_id, rgb_regions, depth_regions, ply_regions, output_dir):
    rgb_dir = output_dir
    depth_dir = output_dir.replace("rgb", "depth")
    ply_dir = output_dir.replace("rgb", "ply")

    for i, (region, square) in enumerate(rgb_regions):
        x1, y1, x2, y2 = square
        rgb_output_dir = os.path.join(rgb_dir, f"{image_id}_{x1}_{y1}_{x2}_{y2}.png")
        cv2.imwrite(rgb_output_dir, region)

    for i, (region, square) in enumerate(depth_regions):
        x1, y1, x2, y2 = square
        depth_output_dir = os.path.join(
            depth_dir, f"{image_id}_{x1}_{y1}_{x2}_{y2}.png"
        )
        cv2.imwrite(depth_output_dir, region)

    for i, (region, square) in enumerate(ply_regions):
        x1, y1, x2, y2 = square
        ply_output_dir = os.path.join(ply_dir, f"{image_id}_{x1}_{y1}_{x2}_{y2}.ply")
        o3d.io.write_point_cloud(ply_output_dir, region)
        # o3d.io.read_point_cloud()


def get_bbox_regions(image_id, image_path, txt_file_path, output_dir):
    image = cv2.imread(image_path)
    depth_image = cv2.imread(image_path.replace(".png", "_depth.png"))
    pcd_cloud = o3d.io.read_point_cloud(image_path.replace(".png", ".ply"))

    # 读取最小正方形的坐标
    squares = read_squares_from_txt(txt_file_path)

    # 截取图像区域
    rgb_regions, depth_regions, ply_regions = extract_square_regions(
        image, depth_image, pcd_cloud, squares
    )

    # 保存截取的图像区域
    save_regions(image_id, rgb_regions, depth_regions, ply_regions, output_dir)

    # 显示截取的区域
    # for i, (region, _) in enumerate(regions):
    #     cv2.imshow(f"Region {i + 1}", region)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
