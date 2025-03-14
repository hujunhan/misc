# script to split video into shorter clips
import os
import cv2

MAX_DURATION = 15 * 60 - 10  # seconds

src_dir = "/Users/hu/Movies/screen"
dst_dir = "/Users/hu/Movies/screen_split"

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)


def with_opencv(filename):
    video = cv2.VideoCapture(filename)

    duration = video.get(cv2.CAP_PROP_POS_MSEC)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    return duration, frame_count


# order with file name
# for file in os.listdir(src_dir):
for file in sorted(os.listdir(src_dir)):
    print(file)
    # if there is space in file name, replace it with "_"
    if " " in file:
        new_file = file.replace(" ", "_")
        os.rename(f"{src_dir}/{file}", f"{src_dir}/{new_file}")
        file = new_file
    # check length, if < MAX_DURATION, skip
    duration, frame_count = with_opencv(f"{src_dir}/{file}")
    duration = frame_count / 60 / 60
    if duration < 15:
        print(f"{file} is too short, skip")
        os.system(f"mv {src_dir}/{file} {dst_dir}/{file}")
        continue
    # use ffmpeg to split video
    # example: ffmpeg -i input.mp4 -c copy -map 0 -segment_time 8 -f segment output%03d.mp4
    os.system(
        "ffmpeg -i {}/{} -c copy -map 0 -segment_time {} -f segment -reset_timestamps 1 {}/{}%03d.mp4".format(
            src_dir, file, MAX_DURATION, dst_dir, file
        )
    )
    print(f"{file} split into shorter clips")
