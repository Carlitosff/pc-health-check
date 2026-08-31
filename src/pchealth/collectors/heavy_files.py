"""Find the heaviest files and directories under a path.

The walk is done bottom-up so each directory's size is the sum of its own
files plus the already-computed sizes of its children. Symlinks are not
followed, which keeps the scan bounded and avoids double counting.
"""

from __future__ import annotations

import heapq
import os
from typing import Optional

from ..models import FileEntry, ScanResult


def scan_path(path: str, top_n: int = 10) -> ScanResult:
    """Scan ``path`` and return the ``top_n`` heaviest files and directories.

    Directory sizes are cumulative (they include every descendant). Files
    and directories that cannot be read are counted in ``errors`` and
    skipped, so a single unreadable entry never aborts the scan.
    """
    root = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(root):
        raise FileNotFoundError(f"Path does not exist: {root}")
    if not os.path.isdir(root):
        # A single file: report it directly.
        size = _safe_size(root)
        entry = FileEntry(path=root, size_bytes=size or 0)
        return ScanResult(
            root=root,
            top_files=[entry] if size is not None else [],
            top_dirs=[],
            total_bytes=size or 0,
            files_scanned=1 if size is not None else 0,
            errors=0 if size is not None else 1,
        )

    dir_sizes: dict[str, int] = {}
    files: list[FileEntry] = []
    total = 0
    files_scanned = 0
    errors = 0

    # topdown=False guarantees children are visited before their parent.
    for current, subdirs, filenames in os.walk(root, topdown=False, followlinks=False):
        own_size = 0
        for name in filenames:
            full = os.path.join(current, name)
            if os.path.islink(full):
                continue
            size = _safe_size(full)
            if size is None:
                errors += 1
                continue
            own_size += size
            total += size
            files_scanned += 1
            files.append(FileEntry(path=full, size_bytes=size))

        subtree = own_size
        for name in subdirs:
            child = os.path.join(current, name)
            subtree += dir_sizes.get(child, 0)
        dir_sizes[current] = subtree

    dirs = [
        FileEntry(path=p, size_bytes=s)
        for p, s in dir_sizes.items()
        if p != root  # the root itself is not an interesting "heavy folder"
    ]

    return ScanResult(
        root=root,
        top_files=heapq.nlargest(top_n, files, key=lambda e: e.size_bytes),
        top_dirs=heapq.nlargest(top_n, dirs, key=lambda e: e.size_bytes),
        total_bytes=total,
        files_scanned=files_scanned,
        errors=errors,
    )


def _safe_size(path: str) -> Optional[int]:
    """File size in bytes, or ``None`` if the entry cannot be read."""
    try:
        return os.path.getsize(path)
    except (OSError, ValueError):
        return None
