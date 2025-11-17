#!/usr/bin/env python3
"""
Script to flatten nested subfolders by moving all files to their root subfolder.

For a structure like:
/Travel/
    A/
        file1.jpg
        B/
            file2.jpg
            C/
                file3.jpg
    D/
        file4.jpg

This will result in:
/Travel/
    A/
        file1.jpg
        file2.jpg
        file3.jpg
    D/
        file4.jpg
"""

import os
import shutil
from pathlib import Path


def flatten_subfolder(root_subfolder):
    """
    Move all files from nested subfolders to the root subfolder.

    Args:
        root_subfolder: Path object pointing to a root subfolder (e.g., A, D)
    """
    root_path = Path(root_subfolder)

    if not root_path.is_dir():
        print(f"Skipping {root_path} - not a directory")
        return

    print(f"\nProcessing: {root_path.name}")
    files_moved = 0

    # Walk through all subdirectories
    for current_dir, subdirs, files in os.walk(root_path, topdown=False):
        current_path = Path(current_dir)

        # Skip the root subfolder itself
        if current_path == root_path:
            continue

        # Move all files in current directory to root subfolder
        for filename in files:
            source_file = current_path / filename
            dest_file = root_path / filename

            # Handle filename conflicts
            if dest_file.exists():
                # Add a suffix to avoid overwriting
                base_name = dest_file.stem
                extension = dest_file.suffix
                counter = 1
                while dest_file.exists():
                    dest_file = root_path / f"{base_name}_{counter}{extension}"
                    counter += 1
                print(f"  Conflict resolved: {filename} -> {dest_file.name}")

            try:
                shutil.move(str(source_file), str(dest_file))
                print(
                    f"  Moved: {source_file.relative_to(root_path)} -> {dest_file.name}"
                )
                files_moved += 1
            except Exception as e:
                print(f"  Error moving {source_file}: {e}")

    # Remove empty subdirectories
    for current_dir, subdirs, files in os.walk(root_path, topdown=False):
        current_path = Path(current_dir)

        # Skip the root subfolder itself
        if current_path == root_path:
            continue

        # Remove if empty
        try:
            if not any(current_path.iterdir()):
                current_path.rmdir()
                print(
                    f"  Removed empty directory: {current_path.relative_to(root_path)}"
                )
        except Exception as e:
            print(f"  Could not remove {current_path}: {e}")

    print(f"Finished {root_path.name}: {files_moved} files moved")


def main():
    source_folder = "/Volumes/SSK/Lightroom/Personal/Travel"
    source_path = Path(source_folder)

    if not source_path.exists():
        print(f"Error: Source folder does not exist: {source_folder}")
        return

    if not source_path.is_dir():
        print(f"Error: Source path is not a directory: {source_folder}")
        return

    print(f"Processing subfolders in: {source_folder}")
    print("=" * 60)

    # Get all immediate subfolders (A, D, etc.)
    root_subfolders = [item for item in source_path.iterdir() if item.is_dir()]

    if not root_subfolders:
        print("No subfolders found in source folder")
        return

    print(f"Found {len(root_subfolders)} root subfolders to process")

    # Process each root subfolder
    for subfolder in sorted(root_subfolders):
        flatten_subfolder(subfolder)

    print("\n" + "=" * 60)
    print("All subfolders processed!")


if __name__ == "__main__":
    main()
