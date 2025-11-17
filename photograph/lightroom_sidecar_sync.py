#!/usr/bin/env python3
"""
Sync missing Lightroom sidecar (.xmp) files from a source photo directory
to matching photos in a target directory.

Logic:
1. Recursively index all photo files in target (default: /Volumes/SSK/Unsorted).
2. Recursively walk source (default: /Volumes/SSK/JPG). For each photo file:
   - If a sidecar `<filename>.xmp` exists beside the source photo,
     find all target photos with the same filename (case-insensitive match).
   - For each matching target photo missing its own sidecar, copy the source sidecar.
3. Report summary statistics. Respect --dry-run (no file copies performed).

Duplicate Filenames:
If the same filename appears multiple times in the target tree, the sidecar will
be copied to each location missing it.

Usage examples:
  Dry run (no actual copies):
    python lightroom_sidecar_sync.py --dry-run
  Actual copy:
    python lightroom_sidecar_sync.py
  Custom paths:
    python lightroom_sidecar_sync.py --source /path/to/JPG --target /path/to/Unsorted
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import shutil
from typing import Dict, List, Tuple

DEFAULT_SOURCE = "/Volumes/SSK/JPG"
DEFAULT_TARGET = "/Volumes/SSK/Unsorted"
# Supported photo file extensions (case-insensitive)
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".heic", ".heif", ".hif"}


def build_target_index(target_root: Path) -> Dict[str, List[Path]]:
    """Return mapping from lowercase filename to list of full paths in target tree."""
    index: Dict[str, List[Path]] = {}
    for path in target_root.rglob("*"):
        if path.is_file() and path.suffix.lower() in PHOTO_EXTENSIONS:
            key = path.name.lower()
            index.setdefault(key, []).append(path)
    return index


def find_source_photos(source_root: Path) -> List[Path]:
    return [
        p
        for p in source_root.rglob("*")
        if p.is_file() and p.suffix.lower() in PHOTO_EXTENSIONS
    ]


def copy_sidecar(
    src_sidecar: Path, dest_photo: Path, dry_run: bool
) -> Tuple[bool, str]:
    """Copy sidecar beside dest_photo if missing. Returns (action_taken, message)."""
    dest_sidecar = dest_photo.with_suffix(".xmp")
    if dest_sidecar.exists():
        return False, f"EXISTS  {dest_sidecar}"
    if dry_run:
        return True, f"DRYRUN COPY {src_sidecar} -> {dest_sidecar}"
    try:
        # Ensure destination directory exists (it should, but be safe).
        dest_sidecar.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_sidecar, dest_sidecar)
        return True, f"COPIED  {src_sidecar} -> {dest_sidecar}"
    except Exception as e:
        return False, f"ERROR   {dest_sidecar}: {e}"


def process(source_root: Path, target_root: Path, dry_run: bool, verbose: bool) -> None:
    if not source_root.is_dir():
        print(f"Source directory not found: {source_root}", file=sys.stderr)
        sys.exit(1)
    if not target_root.is_dir():
        print(f"Target directory not found: {target_root}", file=sys.stderr)
        sys.exit(1)

    print(f"Indexing target photos under {target_root} ...")
    target_index = build_target_index(target_root)
    print(
        f"Indexed {sum(len(v) for v in target_index.values())} target photos (unique filenames: {len(target_index)})"
    )

    print(f"Scanning source photos under {source_root} ...")
    source_photos = find_source_photos(source_root)
    print(f"Found {len(source_photos)} source photos")

    total_with_sidecar = 0
    total_missing_in_target = 0
    total_sidecars_to_copy = 0
    total_sidecars_copied = 0

    for src_photo in source_photos:
        src_key = src_photo.name.lower()
        src_sidecar = src_photo.with_suffix(".xmp")
        has_sidecar = src_sidecar.exists()
        if has_sidecar:
            total_with_sidecar += 1
        # Find matching target photos
        matches = target_index.get(src_key, [])
        if not matches:
            total_missing_in_target += 1
            if verbose:
                print(f"NO MATCH IN TARGET: {src_photo}")
            continue
        if not has_sidecar:
            # Nothing to copy.
            if verbose:
                print(f"NO SOURCE SIDECAR: {src_photo}")
            continue
        # Copy sidecar for each missing in target
        for dest_photo in matches:
            action, msg = copy_sidecar(src_sidecar, dest_photo, dry_run=dry_run)
            if action:
                total_sidecars_to_copy += 1
                if not dry_run:
                    total_sidecars_copied += 1
            if verbose or action:
                print(msg)

    print("\nSummary:")
    print(f"Source photos: {len(source_photos)}")
    print(f"Source photos with sidecar: {total_with_sidecar}")
    print(f"Source filenames missing in target: {total_missing_in_target}")
    print(f"Target sidecars needed: {total_sidecars_to_copy}")
    if dry_run:
        print(f"(Dry run) Sidecars that would be copied: {total_sidecars_to_copy}")
    else:
        print(f"Sidecars copied: {total_sidecars_copied}")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync missing .xmp sidecar files between photo directories."
    )
    parser.add_argument(
        "--source",
        default=DEFAULT_SOURCE,
        type=Path,
        help="Source photo root (with good sidecars)",
    )
    parser.add_argument(
        "--target",
        default=DEFAULT_TARGET,
        type=Path,
        help="Target photo root to receive missing sidecars",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not copy files; only report intended actions",
        default=True,
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed per-file actions",
        default=True,
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    args = parse_args(argv)
    process(args.source, args.target, dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    main(sys.argv[1:])
