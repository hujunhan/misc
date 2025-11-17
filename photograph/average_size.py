# by giving a extension, calculate average size of files with that extension in a directory

from pathlib import Path
from typing import Tuple


def calculate_average_file_size(
    directory: Path, extension: str
) -> Tuple[float, int, int]:
    """Return average size (bytes), file count, and total size for files matching extension."""

    normalized_ext = extension if extension.startswith(".") else f".{extension}"
    normalized_ext = normalized_ext.lower()

    files = [
        file_path
        for file_path in directory.rglob("*")
        if file_path.is_file() and file_path.suffix.lower() == normalized_ext
    ]

    if not files:
        return 0.0, 0, 0

    total_size = sum(file_path.stat().st_size for file_path in files)
    return total_size / len(files), len(files), total_size


def format_size(num_bytes: float) -> str:
    """Human readable representation matching simple 1024-based units."""

    for unit in ("B", "KB", "MB", "GB", "TB"):
        if num_bytes < 1024 or unit == "TB":
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.2f} TB"


if __name__ == "__main__":
    ext = ".raf"  # specify the extension here
    directory = Path("/Volumes/SSK/Lightroom")  # specify the directory here

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    average_size, file_count, total_size = calculate_average_file_size(directory, ext)

    if file_count == 0:
        print(f"No files with extension '{ext}' found in {directory}")
    else:
        print(f"Files scanned: {file_count}")
        print(f"Total size: {format_size(float(total_size))}")
        print(f"Average size: {format_size(average_size)}")
