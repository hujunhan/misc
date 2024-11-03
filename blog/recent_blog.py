# script to list most recent blog posts except for the ones in the exclude list

import os
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

root_pat = Path("/Users/hu/Library/Mobile Documents/com~apple~CloudDocs/MarkdownNotes")

except_folder = "Questions"

recent_days = 30

md_files = root_pat.glob("**/*.md")
date_dict = defaultdict(datetime)
for file_path in md_files:
    file_name = file_path.stem
    if except_folder in file_path.parts:
        continue
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("date:"):
                date = datetime.strptime(line.split(" ")[1], "%Y-%m-%d")
                date_dict[file_name] = date
                break

today = datetime.today()
recent_date = today - timedelta(days=recent_days)
# print the title
for key, value in sorted(date_dict.items(), key=lambda item: item[1], reverse=True):
    if value > recent_date:
        print(key, value)
