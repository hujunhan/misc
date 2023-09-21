# script to move question markdown notes from one folder to another
# and update the categories in the markdown files

import os
import re
import shutil
import glob
from datetime import datetime

# define the origin folder
src_folder = "/Users/hu/code/WorkNote/Question"
src_files = glob.glob(src_folder + "/*.md")


def get_header(file_name, data_str):
    new_file = []
    new_file.append(
        f"""---
title: {file_name} Question
author: Junhan Hu
tags:
  - questions
mathjax: true
categories:
  - MarkdownNotes
  - Life Skill
  - Questions
  - {data_str}
"""
    )
    return new_file


# define the destination folder
dst_folder = "/Users/hu/Library/Mobile Documents/com~apple~CloudDocs/MarkdownNotes/Life Skill/Questions"
dst_files = glob.glob(dst_folder + "*/*/*.md")
dst_name_set = set(x.split("/")[-1] for x in dst_files)
print(dst_name_set)

for file_path in src_files:
    name = file_path.split("/")[-1]
    if name in dst_name_set:
        print(f"{name} already exists in destination folder")
    else:
        # read the md file
        with open(file_path, "r") as file:
            START_FLAG = False
            for line in file:
                if line.startswith("date: "):
                    START_FLAG = True
                    # print(line.split(' ')[1])
                    ## Convert date string to datetime object
                    ## Format of date string: 2021-01-01
                    date = datetime.strptime(line.split(" ")[1], "%Y-%m-%d")
                    year = date.year
                    month = date.month
                    # form string last two digit of year and 2 digit of month like 2101, 2212
                    date_str = str(year)[-2:] + str(month).zfill(2)
                    new_file = get_header(name.split(".")[0], date_str)
                if START_FLAG:
                    new_file.append(line)
        # write the md file to dst_folder/date_str/namer
        # check if the folder exists
        if not os.path.exists(os.path.join(dst_folder, date_str)):
            os.makedirs(os.path.join(dst_folder, date_str))
        with open(os.path.join(dst_folder, date_str, name), "w") as file:
            for line in new_file:
                file.write(f"{line}")
            print(f"{name} has been moved to destination folder")
