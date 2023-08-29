import os
import json


def get_folder_structure(root_folder):
    folder_structure = {}

    for root, dirs, files in os.walk(root_folder):
        current_folder = {}

        # Add Markdown files to the current folder dictionary
        markdown_files = [f for f in files if f.endswith(".md")]
        if markdown_files:
            current_folder["files"] = markdown_files

        # Recursively add subfolders
        for d in dirs:
            sub_folder_structure = get_folder_structure(os.path.join(root, d))
            if sub_folder_structure:
                current_folder[d] = sub_folder_structure

        return current_folder if current_folder else None


if __name__ == "__main__":
    root_folder = (
        "/Users/hu/Downloads/MarkdownNotes"  # Replace with the actual folder path
    )
    folder_structure = get_folder_structure(root_folder)

    # print(json.dumps(folder_structure, indent=4))
    print(folder_structure)
