# script to batch convert ts to mp4

import os

src_folder = "/Users/hu/Downloads"
dst_folder = "/Users/hu/Downloads/mp4"

# change dir to src folder
os.chdir(src_folder)

# create dst folder if it doesn't exist
if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)


# get all ts files
ts_files = [f for f in os.listdir(src_folder) if f.endswith(".ts")]

# iterate over all the ts files
for ts_file in ts_files:
    # get the name of the file without the extension
    name = os.path.splitext(ts_file)[0]
    # create the destination file name
    dst_file = os.path.join(dst_folder, f"{name}.mp4")
    # run the ffmpeg command to convert the ts file to mp4
    os.system(f"ffmpeg -i {ts_file} -c:v h264_videotoolbox {dst_file}")
