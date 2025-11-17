from pathlib import Path
from typing import Dict, List


# ---- CONFIG ----
root_dir = Path("/Volumes/SSK/LightroomCompress/Personal/Life")

check_dir = root_dir / "westmar"
other_dirs = [
    root_dir / "2022",
    root_dir / "2023",
    root_dir / "2024",
    root_dir / "2025",
]
# ---------------


def iter_files(directory: Path):
    """Yield all files under 'directory' recursively."""
    for path in directory.rglob("*"):
        if path.is_file():
            yield path


def build_name_index(directories) -> Dict[str, List[Path]]:
    """
    Build index:
        filename -> [list of paths]
    for all files in other_dirs.
    """
    index: Dict[str, List[Path]] = {}

    for d in directories:
        if not d.exists():
            print(f"[WARN] Skipping missing directory: {d}")
            continue

        print(f"[INFO] Indexing: {d}")
        for file_path in iter_files(d):
            key = file_path.name
            index.setdefault(key, []).append(file_path)

    return index


def find_duplicates_by_name(check_dir: Path, other_dirs):
    print(f"[INFO] Building filename index for other dirs...")
    index = build_name_index(other_dirs)

    print(f"[INFO] Checking files in: {check_dir}")
    duplicates_found = 0

    for file_path in iter_files(check_dir):
        key = file_path.name

        if key in index:
            duplicates_found += 1
            print(f"\n[DUPLICATE] {file_path}")
            for other_path in index[key]:
                print(f"    -> also found in: {other_path}")

    print(f"\n[RESULT] Duplicate filenames found: {duplicates_found}")


if __name__ == "__main__":
    if not check_dir.exists():
        raise SystemExit(f"[FATAL] check_dir does not exist: {check_dir}")

    find_duplicates_by_name(check_dir, other_dirs)
