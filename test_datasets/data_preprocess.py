from extract_regions import get_bbox_regions
from rectangle2square import rectangle2square
import os


def main(root_dir, datasets_root_dir):
    for subdir in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, subdir)
        if os.path.isdir(subdir_path):
            for data_path in os.listdir(subdir_path):
                if len(data_path) == 1:
                    data_dir = os.path.join(subdir_path, data_path)
                    image_id = int(data_path)
                    image_name = data_path + ".png"
                    label_json_name = data_path + "_labels.json"
                    template_txt_name = data_path + "_template_bbox.txt"

                    image_file_path = os.path.join(data_dir, image_name)
                    label_json_path = os.path.join(data_dir, label_json_name)
                    save_label_txt_path = os.path.join(data_dir, template_txt_name)

                    datasets_rgb_dir = datasets_root_dir + "/rgb"
                    datasets_depth_dir = datasets_root_dir + "/depth"
                    datasets_ply_dir = datasets_root_dir + "/ply"

                    os.makedirs(datasets_rgb_dir, exist_ok=True)
                    os.makedirs(datasets_depth_dir, exist_ok=True)
                    os.makedirs(datasets_ply_dir, exist_ok=True)

                    if os.path.exists(image_file_path) and os.path.exists(label_json_path):
                        rectangle2square(image_file_path, label_json_path, save_label_txt_path)
                        get_bbox_regions(image_id,image_file_path, save_label_txt_path, datasets_rgb_dir)



if __name__ == "__main__":
    root_dir = "./test_datasets/data"
    datasets_dir = "./test_datasets/datasets"
    main(root_dir, datasets_dir)
