# crop sketch image to same ratio and size for combine to pdf
from PIL import Image
import os
import shutil


def process_images(folder_path, target_width, target_height):
    aspect_ratio = target_width / target_height

    for file_name in os.listdir(folder_path):
        if file_name.endswith(
            ("jpg", "jpeg", "png")
        ):  # Add/check other file types if needed
            img_path = os.path.join(folder_path, file_name)
            with Image.open(img_path) as img:
                img_width, img_height = img.size
                img_aspect_ratio = img_width * 1.0 / img_height
                if abs(img_aspect_ratio - aspect_ratio) < 0.01:
                    print(f"Skip {file_name}")
                    continue
                # Calculate the new dimensions or crop size
                if img_aspect_ratio > aspect_ratio:
                    # Image is wider than target, crop the width
                    new_width = int(img_height * aspect_ratio)
                    offset = (img_width - new_width) / 2
                    crop_area = (offset, 0, img_width - offset, img_height)
                else:
                    # Image is taller than target, crop the height
                    new_height = int(img_width / aspect_ratio)
                    offset = (img_height - new_height) / 2
                    crop_area = (0, offset, img_width, img_height - offset)

                # Crop and resize
                img_cropped = img.crop(crop_area)
                # img_resized = img_cropped.resize(
                #     (target_width, target_height), Image.LANCZOS
                # )

                # Save or display the processed image

                # delete original file
                os.remove(img_path)

                img_cropped.save(os.path.join(folder_path, f"{file_name}"), quality=70)
                # Optionally, you can show the image to check the result with img_resized.show()
                print(f"Processed {file_name}")


if __name__ == "__main__":
    process_images(
        "/Users/hu/Downloads/p_p", 3.0, 4.0
    )  # Update path and target dimensions as needed
