"""Small formatting helpers with no external dependencies."""

from __future__ import annotations

from typing import Optional

_UNITS = ("B", "KB", "MB", "GB", "TB", "PB")


def human_size(num_bytes: float) -> str:
    """Turn a byte count into a compact human string, e.g. 1536 -> '1.5 KB'.

    Uses binary steps (1 KB = 1024 B) which is what file managers show.
    """
    if num_bytes < 0:
        return "-" + human_size(-num_bytes)

    size = float(num_bytes)
    for unit in _UNITS:
        if size < 1024 or unit == _UNITS[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024
    # Unreachable, kept for type checkers.
    return f"{size:.1f} PB"


def human_duration(seconds: Optional[int]) -> str:
    """Turn a number of seconds into 'Hh Mm', e.g. 5400 -> '1h 30m'."""
    if seconds is None or seconds < 0:
        return "unknown"
    minutes = seconds // 60
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes:02d}m"
    return f"{minutes}m"
