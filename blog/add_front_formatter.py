import os
import datetime
import glob

root_path = "Z:\\WorkNote"
path_list = glob.glob(root_path + "/**/*.md", recursive=True)
for file_path in path_list:
    print(file_path)
    # get the last modified date of the file
    last_modified = os.path.getmtime(file_path)
    date = datetime.datetime.fromtimestamp(last_modified).strftime("%Y-%m-%d")
    time = datetime.datetime.fromtimestamp(last_modified).strftime("%H:%M:%S")
    # get the title from the file name
    title = os.path.splitext(os.path.basename(file_path))[0].replace("_", " ").title()

    # create the YAML front matter
    yaml_front_matter = f"---\ntitle: {title}\nauthor: Junhan Hu\nmathjax: true\ndate: {date} {time}\n---\n"

    # read the existing Markdown content
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # prepend the YAML front matter to the Markdown content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(yaml_front_matter + content)
    # print(yaml_front_matter)
