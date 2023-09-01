import os
import re


def update_categories_in_md(file_path, new_categories):
    """Update the 'categories' section in a Markdown file."""
    in_categories_section = False
    updated_lines = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith("categories:"):
                in_categories_section = True
                updated_lines.append(line)

                for category in new_categories:
                    updated_lines.append(f"- {category}")
            elif in_categories_section and line.startswith("-"):
                continue  # Skip old categories
            else:
                in_categories_section = False
                updated_lines.append(line)

    with open(file_path, "w") as file:
        for line in updated_lines:
            file.write(f"{line}\n")


def update_all_md_files(root_folder):
    """Update the 'categories' section in all Markdown files within the root folder."""
    for subdir, _, files in os.walk(root_folder):
        relative_path = os.path.relpath(subdir, root_folder)

        new_categories = relative_path.split(os.sep)

        new_categories = [re.sub(r"[^\w\s]", "-", cat) for cat in new_categories]
        new_categories = [re.sub(r"\s+", "-", cat) for cat in new_categories]

        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(subdir, file)
                update_categories_in_md(file_path, new_categories)


# Example usage:
root_folder = "/Users/hu/Downloads/test_markdown"
update_all_md_files(root_folder)
