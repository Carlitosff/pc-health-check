"""System data collectors.

Each module reads one component from the running machine and returns a
plain dataclass from :mod:`pchealth.models`. Nothing here computes a grade;
that lives in :mod:`pchealth.scoring`.
"""

from __future__ import annotations

from ..models import SystemMetrics
from .battery import collect_battery
from .cpu import collect_cpu
from .disk import collect_disk
from .memory import collect_memory
from .temperature import collect_temperature

__all__ = [
    "collect_battery",
    "collect_cpu",
    "collect_disk",
    "collect_memory",
    "collect_temperature",
    "collect_system",
]


def collect_system(cpu_interval: float = 0.5) -> SystemMetrics:
    """Collect every component into a single :class:`SystemMetrics`.

    ``cpu_interval`` is the sampling window (seconds) used to measure CPU
    usage; a short blocking sample gives a far more honest number than an
    instantaneous read.
    """
    return SystemMetrics(
        cpu=collect_cpu(interval=cpu_interval),
        memory=collect_memory(),
        disk=collect_disk(),
        battery=collect_battery(),
        temperature=collect_temperature(),
    )
