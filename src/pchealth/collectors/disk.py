"""Disk / partition metrics collector."""

from __future__ import annotations

import psutil

from ..models import DiskMetrics, DiskPartition


def collect_disk() -> DiskMetrics:
    """Read usage for every mounted, real partition.

    Pseudo filesystems and unreadable mounts (empty CD drives, permission
    errors) are skipped rather than crashing the whole diagnostic.
    """
    partitions = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except (PermissionError, OSError):
            # e.g. an empty optical drive on Windows raises here.
            continue
        partitions.append(
            DiskPartition(
                device=part.device,
                mountpoint=part.mountpoint,
                fstype=part.fstype,
                total_bytes=usage.total,
                used_bytes=usage.used,
                free_bytes=usage.free,
                percent=usage.percent,
            )
        )
    return DiskMetrics(partitions=partitions)
