import argparse
import hashlib
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

PHOTO_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".heic",
    ".tif",
    ".tiff",
    ".dng",
    ".cr2",
    ".nef",
    ".arw",
    ".gif",
    ".bmp",
}


def is_photo(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in PHOTO_EXTENSIONS


def file_hash(path: Path, block_size: int = 1 << 20) -> str:
    """Compute SHA256 hash efficiently."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(block_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def collect_photos(root: Path) -> List[Path]:
    photos = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            p = Path(dirpath) / name
            # Skip hidden/system dotfiles (e.g. .DS_Store, ._resource forks, .thumbnails)
            if name.startswith("."):
                continue
            if is_photo(p):
                photos.append(p)
    return photos


def build_hash_index(paths: List[Path]) -> Dict[str, List[Path]]:
    index: Dict[str, List[Path]] = {}
    for p in paths:
        try:
            h = file_hash(p)
        except Exception as e:
            print(f"[WARN] Failed hashing {p}: {e}")
            continue
        index.setdefault(h, []).append(p)
    return index


def build_name_index(paths: List[Path]) -> Dict[str, List[Path]]:
    index: Dict[str, List[Path]] = {}
    for p in paths:
        key = p.name.lower()
        index.setdefault(key, []).append(p)
    return index


def build_name_size_index(paths: List[Path]) -> Dict[str, List[Path]]:
    index: Dict[str, List[Path]] = {}
    for p in paths:
        try:
            size = p.stat().st_size
        except Exception:
            continue
        key = f"{p.name.lower()}|{size}"
        index.setdefault(key, []).append(p)
    return index


def select_life_deletes(
    hash_index: Dict[str, List[Path]], life_dir: Path
) -> List[Path]:
    """Return list of paths to delete (legacy simple form)."""
    deletes: List[Path] = []
    for h, paths in hash_index.items():
        if len(paths) < 2:
            continue
        inside_life = [p for p in paths if life_dir in p.parents]
        outside_life = [p for p in paths if life_dir not in p.parents]
        if outside_life and inside_life:
            deletes.extend(inside_life)
        elif not outside_life and len(inside_life) > 1:
            deletes.extend(inside_life[1:])
    return deletes


def determine_deletion_details(
    index: Dict[str, List[Path]], life_dir: Path
) -> List[Tuple[Path, str, List[Path]]]:
    """Return detailed deletion list: (path_to_delete, reason, all_duplicate_paths)."""
    details: List[Tuple[Path, str, List[Path]]] = []
    for key, paths in index.items():
        if len(paths) < 2:
            continue
        inside_life = [p for p in paths if life_dir in p.parents]
        outside_life = [p for p in paths if life_dir not in p.parents]
        if outside_life and inside_life:
            for p in inside_life:
                details.append((p, "outside_life_exists", list(paths)))
        elif not outside_life and len(inside_life) > 1:
            # Keep first (arbitrary) deletion rest
            for p in inside_life[1:]:
                details.append((p, "extra_copy_in_life", list(paths)))
    return details


def write_report(
    details: List[Tuple[Path, str, List[Path]]],
    report_path: Path,
    life_dir: Path,
    method: str,
) -> None:
    try:
        with report_path.open("w", encoding="utf-8") as f:
            f.write("# Life Dedupe Report\n")
            f.write(f"Method: {method}\n")
            f.write(f"Life Directory: {life_dir}\n")
            f.write(f"Total Deletions: {len(details)}\n\n")
            f.write("delete_path\treason\tother_duplicates\n")
            for delete_path, reason, all_dups in details:
                others = [str(p) for p in all_dups if p != delete_path]
                f.write(f"{delete_path}\t{reason}\t{' ; '.join(others)}\n")
    except Exception as e:
        print(f"[WARN] Failed writing report {report_path}: {e}")


def summarize(deletes: List[Path], life_dir: Path) -> Tuple[int, Dict[str, int]]:
    stats: Dict[str, int] = {}
    for p in deletes:
        rel = p.relative_to(life_dir)
        top = rel.parts[0] if rel.parts else ""  # year folder etc.
        stats[top] = stats.get(top, 0) + 1
    return len(deletes), stats


def main():
    parser = argparse.ArgumentParser(
        description="Remove duplicate photos under Life folder while keeping copies elsewhere."
    )
    parser.add_argument(
        "root",
        type=Path,
        help="Root of the mega photo folder (parent of Personal/Creative).",
    )
    parser.add_argument(
        "--life-subpath",
        default="Personal/Life",
        help="Relative path from root to Life folder.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only list duplicates to delete, do not remove.",
    )
    parser.add_argument(
        "--exec",
        action="store_true",
        help="Actually perform deletions (mutually exclusive with --dry-run).",
    )
    parser.add_argument("--verbose", action="store_true", help="Print every decision.")
    parser.add_argument(
        "--method",
        choices=["hash", "name", "name_size"],
        default="name_size",
        help="Duplicate detection method: hash | name | name_size (default name_size).",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Optional path to write a text report of proposed deletions (defaults to root/life_dedupe_report.txt)",
    )
    args = parser.parse_args()

    if args.dry_run and args.exec:
        print("Cannot use --dry-run and --exec together.")
        sys.exit(1)
    if not args.dry_run and not args.exec:
        print(
            "No action flag provided; defaulting to dry-run. Use --exec to actually delete."
        )
        args.dry_run = True

    root: Path = args.root.resolve()
    life_dir: Path = (root / args.life_subpath).resolve()

    if not root.exists():
        print(f"Root does not exist: {root}")
        sys.exit(1)
    if not life_dir.exists():
        print(f"Life directory does not exist: {life_dir}")
        sys.exit(1)

    print(f"Scanning photos under root: {root}")
    photos = collect_photos(root)
    print(f"Total photos found: {len(photos)}")

    if args.method == "hash":
        index = build_hash_index(photos)
        duplicates_metric_label = "Unique hashes with duplicates"
    elif args.method == "name":
        index = build_name_index(photos)
        duplicates_metric_label = "Filenames with duplicates"
    else:  # name_size
        index = build_name_size_index(photos)
        duplicates_metric_label = "Filename+size keys with duplicates"

    duplicates_count = sum(1 for v in index.values() if len(v) > 1)
    print(f"{duplicates_metric_label}: {duplicates_count}")

    details = determine_deletion_details(index, life_dir)
    deletes = [d[0] for d in details]
    total_delete, bucket_stats = summarize(deletes, life_dir)
    print(f"Life photos marked for deletion: {total_delete}")
    if bucket_stats:
        print("Breakdown (top-level Life subfolder -> count):")
        for k, v in sorted(bucket_stats.items(), key=lambda x: (-x[1], x[0])):
            print(f"  {k}: {v}")

    if args.verbose:
        for path, reason, all_dups in details:
            print(f"DELETE: {path} | reason={reason} | duplicates={len(all_dups)}")

    # Determine report path
    report_path = args.report if args.report else (root / "life_dedupe_report.txt")
    write_report(details, report_path, life_dir, args.method)
    print(f"Report written: {report_path}")

    if args.dry_run:
        print("Dry run complete. No files were deleted.")
        return

    # Execute deletions
    deleted_ok = 0
    for p in deletes:
        try:
            p.unlink()
            deleted_ok += 1
        except Exception as e:
            print(f"[ERROR] Failed deleting {p}: {e}")
    print(
        f"Deletion complete. Successfully removed {deleted_ok} of {len(deletes)} files."
    )


if __name__ == "__main__":
    main()
