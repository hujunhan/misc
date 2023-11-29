## Automate the image import process
import os
import subprocess
import sys

## Get the path to the folder containing the images
root_path = sys.argv[1]
# root_path = "/Volumes/Untitled/DCIM/10131014"
## Define the extensions of the raw and jpg files
raw_extensions = [".DND", ".RW2", ".NEF", ".ORF", ".ARW"]
jpg_extensions = [".JPG", ".JPEG", ".HIF"]

## Find the raw files and the jpg files
raw_list = []
jpg_list = []
jpg_remove_list = []
for rext in raw_extensions:
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(rext):
                raw_list.append(file[: -len(rext)])
print(raw_list)

for jext in jpg_extensions:
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(jext):
                jpg_list.append(file[: -len(jext)])
print(jpg_list)


## Find the jpg files that have a corresponding raw file
for jpg in jpg_list:
    if jpg in raw_list:
        jpg_remove_list.append(jpg)

## Delete the jpg files that have a corresponding raw file
print(jpg_remove_list)
for jext in jpg_extensions:
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(jext) and file[: -len(jext)] in jpg_remove_list:
                os.remove(os.path.join(root, file))
                print(f"removing {os.path.join(root,file)}")

## Open the remaining raw and jpg files in default application
command_list = ["open", "-a", "Adobe Lightroom"]
for root, dirs, files in os.walk(root_path):
    for file in files:
        ## Exclude hidden files and dat files
        if (
            not file.startswith(".")
            and not file.endswith(".DAT")
            and not (file.endswith(jext) and file[: -len(jext)] in jpg_remove_list)
        ):
            command_list.append(os.path.join(root, file))
print(command_list)
subprocess.run(command_list)
