# script to prepare data for model
# output RGB, depth, and ply files for each bounding box in the image
# 1. read the captured image and ply file
# 2. read the template ply file and bounding box coordinates
# 3. point cloud registration from the captured ply file to the template ply file
# 4. convert the registered point cloud to depth image
# 5. extract bounding box regions from the depth image
# 6. convert back the bounding box regions to point cloud
# 7. convert the point cloud to depth image
# 8. bound the new uv area to a box
# 9. crop the new bounding box area of the depth image and RGB and corresponding point cloud to ply
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import os
import copy
from PIL import Image

DEBUG = True


def create_point_cloud_from_depth_image(depth):
    fx, fy, cx, cy = (
        1783.40026855469,
        1782.84008789062,
        979.268188476562,
        586.475830078125,
    )
    width, height = 1944, 1200
    xmap = np.arange(width)
    ymap = np.arange(height)
    xmap, ymap = np.meshgrid(xmap, ymap)
    points_z = depth
    points_x = (xmap - cx) * points_z / fx
    points_y = (ymap - cy) * points_z / fy
    # ignore invalid points
    valid = points_z != np.inf
    points_x = points_x[valid]
    points_y = points_y[valid]
    points_z = points_z[valid]
    cloud = np.stack([points_x, points_y, points_z], axis=-1)
    cloud = cloud.reshape([-1, 3])
    return cloud


def pcd_to_depth_image(pcd_points):
    fx, fy, cx, cy = (
        1783.40026855469,
        1782.84008789062,
        979.268188476562,
        586.475830078125,
    )
    width, height = 1944, 1200
    # conver to numpy array
    pcd_points = np.asarray(pcd_points)
    print(pcd_points.shape)
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
    # img_z_shift = np.array(
    #     [
    #         img_z,
    #         np.roll(img_z, 1, axis=0),
    #         np.roll(img_z, -1, axis=0),
    #         np.roll(img_z, 1, axis=1),
    #         np.roll(img_z, -1, axis=1),
    #     ]
    # )

    # img_z = np.min(img_z_shift, axis=0)
    return img_z


def preprocess_pcd(pcd, name):
    # downsample the point cloud
    voxel_size = 1
    pcd = pcd.voxel_down_sample(voxel_size)
    pcd.points = o3d.utility.Vector3dVector(np.asarray(pcd.points).astype(np.float32))
    # remove the outliers
    cl, ind = pcd.remove_radius_outlier(nb_points=20, radius=5.0)
    inlier_cloud = pcd.select_by_index(ind)
    return inlier_cloud
    # o3d.io.write_point_cloud(name, inlier_cloud, write_ascii=True)


def execute_global_registration(
    source_down, target_down, source_fpfh, target_fpfh, voxel_size
):
    distance_threshold = voxel_size * 1.5
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down,
        target_down,
        source_fpfh,
        target_fpfh,
        True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3,
        [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold
            ),
        ],
        o3d.pipelines.registration.RANSACConvergenceCriteria(100000, 0.999),
    )

    # fast global registration based on feature matching
    # result = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(
    #     source_down,
    #     target_down,
    #     source_fpfh,
    #     target_fpfh,
    # )
    return result


def point_cloud_registration(captured_pcd, template_pcd):
    # res_example = np.asarray(
    #     [
    #         [0.977868351, 0.00392439069, 0.20918434, -50.4452225],
    #         [-0.0020659664, 0.999956443, -0.0091019079, -2.82676358],
    #         [-0.209210948, 0.00846829985, 0.977833865, 47.0264168],
    #         [0.0, 0.0, 0.0, 1.0],
    #     ]
    # )
    # return res_example
    template_pcd = preprocess_pcd(template_pcd, "template.ply")
    captured_pcd = preprocess_pcd(captured_pcd, "captured.ply")
    radius_normal = 2
    radius_feature = 5
    # estimate normals
    template_pcd.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30)
    )
    template_pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        template_pcd,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100),
    )
    captured_pcd.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30)
    )
    captured_pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        captured_pcd,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100),
    )

    res = execute_global_registration(
        captured_pcd,
        template_pcd,
        captured_pcd_fpfh,
        template_pcd_fpfh,
        voxel_size=1,
    )
    print(res)
    print(res.transformation)

    return res.transformation


def main(
    cap_img_path, cap_ply_path, captured_depth_path, temp_ply_path, temp_bbox_path
):
    # 1. read the captured image and ply file
    cap_img = np.asarray(Image.open(cap_img_path))
    cap_pcd = o3d.io.read_point_cloud(
        cap_ply_path, remove_nan_points=False, remove_infinite_points=False
    )
    cap_depth = np.asarray(Image.open(captured_depth_path))
    # 2. read the template ply file and bounding box coordinates
    temp_pcd = o3d.io.read_point_cloud(
        temp_ply_path, remove_nan_points=False, remove_infinite_points=False
    )
    bounding_boxes = np.loadtxt(temp_bbox_path, dtype=int)
    # 3. point cloud registration from the captured ply file to the template ply file
    T = point_cloud_registration(cap_pcd, temp_pcd)
    if DEBUG:
        print(T)
    test_pcd = copy.deepcopy(cap_pcd)
    test_pcd.transform(T)
    o3d.visualization.draw_geometries([test_pcd, temp_pcd])
    inv_T = np.linalg.inv(T)

    print(inv_T)
    # registed_points = (T[:3, :3].T @ np.asarray(cap_pcd.points).T).T + T[:3, 3]
    registed_points = np.asarray(test_pcd.points)
    print("finish registration")
    # 4. convert the registered point cloud to depth image

    img_z = pcd_to_depth_image(registed_points)

    if DEBUG:
        plt.imshow(img_z)
        # draw the bounding boxes in the image
        for bbox in bounding_boxes:
            x1, y1, x2, y2 = bbox
            plt.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], "r-")
        plt.show()
    # 5. extract bounding box regions from the depth image
    new_bounding_boxes = []
    # reverse the bonding box order, from back to front
    bounding_boxes = bounding_boxes[::-1]
    for bbox in bounding_boxes:
        x1, y1, x2, y2 = bbox
        depth_bbox = np.full_like(img_z, np.inf)
        depth_bbox[y1:y2, x1:x2] = img_z[y1:y2, x1:x2]
        # 6. convert back the bounding box regions to point cloud
        bbox_points = create_point_cloud_from_depth_image(depth_bbox)
        bbox_pcd = o3d.geometry.PointCloud()
        bbox_pcd.points = o3d.utility.Vector3dVector(bbox_points)

        bbox_pcd.transform(inv_T)
        # remove outliers
        # cl, ind = bbox_pcd.remove_radius_outlier(nb_points=10, radius=5.0)
        # bbox_pcd = bbox_pcd.select_by_index(ind)
        # 7. convert the point cloud to depth image
        try:
            bbox_img_z = pcd_to_depth_image(np.asarray(bbox_pcd.points))
        except Exception as e:
            print(e)
            print("No valid points in the bounding box")
        # 8. bound the new uv area to a box (bounding box of non-inf values)
        non_inf = bbox_img_z != np.inf
        non_inf_indices = np.argwhere(non_inf)
        y1, x1 = non_inf_indices.min(axis=0)
        y2, x2 = non_inf_indices.max(axis=0)
        print(x1, y1, x2, y2)
        # 9. crop the new bounding box area of the depth image and RGB and corresponding point cloud to ply
        bbox_img = cap_img[y1:y2, x1:x2]
        bbox_pcd = bbox_pcd
        bbox_depth = cap_depth[y1:y2, x1:x2]
        if DEBUG:
            plt.subplot(1, 2, 1)
            plt.imshow(bbox_img)
            plt.title("bbox img")
            plt.subplot(1, 2, 2)
            plt.imshow(bbox_depth)
            plt.title("bbox depth")
            plt.show()
        new_bounding_boxes.append([x1, y1, x2, y2])
        if DEBUG:
            o3d.visualization.draw_geometries([bbox_pcd])
        # draw the new bounding boxes in the captured image
    plt.imshow(cap_img)
    for bbox in new_bounding_boxes:
        x1, y1, x2, y2 = bbox
        plt.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], "r-")
    plt.show()


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    captured_img_path = "./data/0001/1-R-5/1-R-5.png"
    captured_ply_path = "./data/0001/1-R-5/1-R-5.ply"
    captured_depth_path = "./data/0001/1-R-5/1-R-5_depth.png"
    template_ply_path = "./data/0001/1/1.ply"
    template_bbox_path = "./data/0001/1/1_template_bbox.txt"
    main(
        captured_img_path,
        captured_ply_path,
        captured_depth_path,
        template_ply_path,
        template_bbox_path,
    )
