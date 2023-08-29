# script to count the number of blog posts written by hour
import glob
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

pre_path = "/Users/hu/Library/Mobile Documents/com~apple~CloudDocs/MarkdownNotes"
md_path = sorted(glob.glob(pre_path + "/**/*.md", recursive=True))

hour_count_dict = defaultdict(int)
for path in md_path:
    md_name = path.split("/")[-1]
    f = open(path, "r")
    data = f.read()

    ## Count by time
    for line in data.split("\n"):
        if "date:" in line:
            line_split = line.split(" ")
            if len(line_split) == 3:
                hour = int(line_split[2].split(":")[0])
                hour_count_dict[hour] += 1
            ## Convert date string to datetime object
            ## Format of date string: 2021-01-01
            # date=datetime.strptime(line.split(' ')[1],'%Y-%m-%d')
            break
        # print the title
        if "title:" in line:
            print(line[6:])

## order the dict by key
hour_count_dict = dict(sorted(hour_count_dict.items(), key=lambda item: item[0]))

## plot the dict using bar chart
plt.bar(hour_count_dict.keys(), hour_count_dict.values())
plt.show()
