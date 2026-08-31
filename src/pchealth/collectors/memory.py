"""Memory (RAM + swap) metrics collector."""

from __future__ import annotations

import psutil

from ..models import MemoryMetrics


def collect_memory() -> MemoryMetrics:
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return MemoryMetrics(
        total_bytes=vm.total,
        available_bytes=vm.available,
        used_bytes=vm.used,
        percent=vm.percent,
        swap_total_bytes=swap.total,
        swap_used_bytes=swap.used,
        swap_percent=swap.percent,
    )
