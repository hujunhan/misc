#!/usr/bin/env python3
"""
Flatten-copy: copy every file from a folder tree into a single destination folder.

Examples:
  python flatten_copy.py /path/to/src /path/to/dest
  python flatten_copy.py src dest --glob "*.jpg" --glob "*.png"
  python flatten_copy.py src dest --overwrite
  python flatten_copy.py src dest --dry-run
"""

import argparse
import os
import shutil
from pathlib import Path
import fnmatch


def iter_files(src: Path):
    """Yield all files under src (recursive)."""
    for root, dirs, files in os.walk(src):
        for name in files:
            p = Path(root) / name
            if p.is_file():
                yield p


def next_available_path(dest_dir: Path, filename: str) -> Path:
    """Return a non-colliding path like 'name (1).ext', 'name (2).ext', ..."""
    base = Path(filename).stem
    suffix = Path(filename).suffix
    candidate = dest_dir / f"{base}{suffix}"
    i = 1
    while candidate.exists():
        candidate = dest_dir / f"{base} ({i}){suffix}"
        i += 1
    return candidate


def should_keep(file_path: Path, globs: list[str]) -> bool:
    """If globs provided, keep only files matching any glob; otherwise keep all."""
    if not globs:
        return True
    name = file_path.name
    return any(fnmatch.fnmatch(name, pat) for pat in globs)


def copy_flat(
    src: Path,
    dst: Path,
    globs: list[str] | None = None,
    overwrite: bool = False,
    dry_run: bool = False,
    verbose: bool = True,
) -> tuple[int, int]:
    """
    Copy files from src (recursive) into dst (flat).
    Returns (copied_count, skipped_count).
    """
    globs = globs or []
    copied = 0
    skipped = 0

    dst.mkdir(parents=True, exist_ok=True)

    for p in iter_files(src):
        if not should_keep(p, globs):
            skipped += 1
            continue

        target = dst / p.name

        if target.exists():
            if overwrite:
                if verbose:
                    print(f"[OVERWRITE] {p} -> {target}")
                if not dry_run:
                    shutil.copy2(p, target)
                copied += 1
            else:
                new_target = next_available_path(dst, p.name)
                if verbose:
                    print(f"[COPY] {p} -> {new_target}")
                if not dry_run:
                    shutil.copy2(p, new_target)
                copied += 1
        else:
            if verbose:
                print(f"[COPY] {p} -> {target}")
            if not dry_run:
                shutil.copy2(p, target)
            copied += 1

    return copied, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Copy all files in subfolders to a destination without folders (flatten)."
    )
    parser.add_argument("src", type=Path, help="Source directory")
    parser.add_argument("dst", type=Path, help="Destination directory (flat)")
    parser.add_argument(
        "--glob",
        action="append",
        default=[],
        help='Glob filter (repeatable), e.g. --glob "*.jpg" --glob "*.png"',
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite files with the same name instead of auto-renaming.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without copying any files.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce output verbosity.",
    )

    args = parser.parse_args()

    if not args.src.exists():
        raise SystemExit(f"Source does not exist: {args.src}")
    if not args.src.is_dir():
        raise SystemExit(f"Source is not a directory: {args.src}")

    copied, skipped = copy_flat(
        src=args.src,
        dst=args.dst,
        globs=args.glob,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
        verbose=not args.quiet,
    )

    if not args.quiet:
        print(
            f"\nDone. Copied: {copied} file(s). Skipped (filtered): {skipped} file(s)."
        )


if __name__ == "__main__":
    main()
