# use open3d to read point cloud and do registration
import open3d as o3d
import numpy as np
import copy

captured_ply_path = "./test_datasets/data/0001/1-R-5/1-R-5.ply"
template_ply_path = "./test_datasets/data/0001/1/1.ply"

captured_pcd = o3d.io.read_point_cloud(captured_ply_path)
template_pcd = o3d.io.read_point_cloud(template_ply_path)

# downsample the point cloud
voxel_size = 1
captured_pcd_down = captured_pcd.voxel_down_sample(
    voxel_size=voxel_size,
)
template_pcd_down = template_pcd.voxel_down_sample(voxel_size=voxel_size)
cl, ind = captured_pcd_down.remove_radius_outlier(nb_points=25, radius=5)
captured_pcd_down = captured_pcd_down.select_by_index(ind)
cl, ind = template_pcd_down.remove_radius_outlier(nb_points=25, radius=5)
template_pcd_down = template_pcd_down.select_by_index(ind)
# show the point cloud before registration
o3d.visualization.draw_geometries([captured_pcd_down, template_pcd_down])
radius_normal = voxel_size * 2
radius_feature = voxel_size * 5
template_pcd_down.estimate_normals(
    o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30)
)
template_pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    template_pcd_down,
    o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100),
)
captured_pcd_down.estimate_normals(
    o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30)
)
captured_pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    captured_pcd_down,
    o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100),
)


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
    return result


result_ransac = execute_global_registration(
    captured_pcd_down,
    template_pcd_down,
    captured_pcd_fpfh,
    template_pcd_fpfh,
    voxel_size,
)
print(result_ransac)
print(result_ransac.transformation)
T = result_ransac.transformation
captured_pcd_down.transform(T)
# show the point cloud after registration
o3d.visualization.draw_geometries([captured_pcd_down, template_pcd_down])
