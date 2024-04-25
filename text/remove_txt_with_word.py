# script to remove txt files with a certain word in the name

input_folder = "/Users/hu/Downloads/output2"
output_folder = "/Users/hu/Downloads/output3"
word = "xx"
size_thresh = 10  # kb


def remove_txt_with_word(input_folder, output_folder, word):
    import os
    import shutil

    # create output folder if not exist
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    count = 0
    for file in os.listdir(input_folder):
        # print(file)
        # read the file content
        with open(os.path.join(input_folder, file), "r") as f:
            for line in f.readlines():
                if word in line:
                    # move the file to output folder
                    shutil.move(os.path.join(input_folder, file), output_folder)
                    count += 1
                    print(f"removed {file}")
                    break

    print(f"removed {count} files")


def remove_txt_too_small(input_folder, output_folder, min_size):
    import os
    import shutil

    # create output folder if not exist
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    count = 0
    for file in os.listdir(input_folder):
        # print(file)
        # read the file content
        with open(os.path.join(input_folder, file), "r") as f:
            # get the file size
            size = os.path.getsize(os.path.join(input_folder, file))
            size = size / 1024
            if size < min_size:
                # move the file to output folder
                shutil.move(os.path.join(input_folder, file), output_folder)
                count += 1
                print(f"removed {file}")

    print(f"removed {count} files")


if __name__ == "__main__":
    remove_txt_with_word(input_folder, output_folder, word)
    # remove_txt_too_small(input_folder, output_folder, size_thresh)
