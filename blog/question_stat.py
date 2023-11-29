# script to analyze the question markdown notes
import os
import re
import glob
from collections import defaultdict
from pathlib import Path

question_folder = "/Users/hu/Library/Mobile Documents/com~apple~CloudDocs/MarkdownNotes/Life Skill/Questions"
question_folder = Path(question_folder)
md_files = question_folder.glob("**/*.md")
question_dict = defaultdict(int)  # key is the date, value is the number of questions

for file_path in md_files:
    with open(file_path, "r") as file:
        file_name = file_path.stem
        for line in file:
            if line.startswith("## "):
                question_dict[file_name] += 1

total_question = sum(question_dict.values())
total_day = len(question_dict.keys())
# plot the number of questions over time
import matplotlib.pyplot as plt
import numpy as np

x = sorted(question_dict.keys())
y = [question_dict[key] for key in x]
plt.plot(x, y)
plt.title(
    f"{total_question} questions in {total_day} days, {total_question/total_day:.2f} questions per day"
)
plt.show()
