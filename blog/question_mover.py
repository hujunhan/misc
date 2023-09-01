# script to move question markdown notes from one folder to another
# and update the categories in the markdown files

import os
import re
import shutil
import glob

# define the origin folder
src_folder = "/Users/hu/code/WorkNote/Question"
src_files = glob.glob(src_folder + "/*.md")


def get_header(date_str):
    new_file = []
    new_file.append(
        f"""---
title: {date_str} Question
author: Junhan Hu
tags:
  - questions
mathjax: true
categories:
  - MarkdownNotes
  - Life Skill
  - Questions
"""
    )
    return new_file


# define the destination folder
dst_folder = "/Users/hu/Library/Mobile Documents/com~apple~CloudDocs/MarkdownNotes/Life Skill/Questions"
dst_files = glob.glob(dst_folder + "/*.md")
dst_name_set = set(x.split("/")[-1] for x in dst_files)
print(dst_name_set)

for file_path in src_files:
    name = file_path.split("/")[-1]
    if name in dst_name_set:
        print(f"{name} already exists in destination folder")
    else:
        # read the md file
        with open(file_path, "r") as file:
            new_file = get_header(name.split(".")[0])
            START_FLAG = False
            for line in file:
                if line.startswith("date: "):
                    START_FLAG = True
                if START_FLAG:
                    new_file.append(line)
        # write the md file
        with open(os.path.join(dst_folder, name), "w") as file:
            for line in new_file:
                file.write(f"{line}")
