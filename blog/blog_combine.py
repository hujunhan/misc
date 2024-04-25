# script to combine all the blog posts into one file

import os

root_path = "/Users/hu/Library/Mobile Documents/com~apple~CloudDocs/MarkdownNotes"

md_path = []
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith(".md"):
            md_path.append(os.path.join(root, file))

print(len(md_path))

# combine all the blog posts into one file
