# script to fix the date in the markdown notes that not in the format of YYYY-MM-DD

import os
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
import random

root_pat = Path("/Users/hu/Library/Mobile Documents/com~apple~CloudDocs/MarkdownNotes")


md_files = root_pat.glob("**/*.md")
error_files = []
# find out all files has wrong date format, shoud be YYYY-MM-DD HH:MM:SS
for file_path in md_files:
    file_name = file_path.stem
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("date:"):
                try:
                    date_str = line[6:].strip()
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    print(file_name)
                    error_files.append(file_path)
                    break
                break

# fix the date format
# for file_path in error_files:
#     file_name = file_path.stem
#     with open(file_path, "r") as file:
#         lines = file.readlines()
#     with open(file_path, "w") as file:
#         for line in lines:
#             if line.startswith("date:"):
#                 date_str = line[6:].strip()
#                 date = datetime.strptime(date_str, "%Y-%m-%d")
#                 # random choose the HH:MM:SS
#                 hour = random.randint(9, 23)
#                 minute = random.randint(0, 59)
#                 second = random.randint(0, 59)
#                 date = date.replace(hour=hour, minute=minute, second=second)
#                 new_date_str = date.strftime("%Y-%m-%d %H:%M:%S")
#                 new_line = f"date: {new_date_str}\n"
#                 # print(new_line)
#                 file.write(new_line)
#             else:
#                 file.write(line)
#                 pass
