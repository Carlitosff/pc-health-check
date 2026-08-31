"""CPU metrics collector."""

from __future__ import annotations

import os
from typing import Optional

import psutil

from ..models import CPUMetrics


def _load_per_core(logical_cores: Optional[int]) -> Optional[float]:
    """1-minute load average normalized by logical core count.

    ``os.getloadavg`` is a Unix concept. psutil emulates it on Windows, but
    the emulated value needs the process to have been running for a while to
    settle, so we treat any failure as "not available" rather than guessing.
    """
    getloadavg = getattr(os, "getloadavg", None)
    if getloadavg is None:
        getloadavg = getattr(psutil, "getloadavg", None)
    if getloadavg is None:
        return None
    try:
        one_minute = getloadavg()[0]
    except (OSError, ValueError, AttributeError):
        return None
    if not logical_cores:
        return one_minute
    return one_minute / logical_cores


def collect_cpu(interval: float = 0.5) -> CPUMetrics:
    """Read CPU counts, frequency and usage.

    ``interval`` blocks for that many seconds to measure a real usage sample.
    """
    logical = psutil.cpu_count(logical=True)
    physical = psutil.cpu_count(logical=False)

    freq_current: Optional[float] = None
    freq_max: Optional[float] = None
    try:
        freq = psutil.cpu_freq()
        if freq is not None:
            freq_current = freq.current or None
            freq_max = freq.max or None
    except (NotImplementedError, AttributeError, OSError):
        # Some platforms/VMs do not expose frequency at all.
        pass

    percent = psutil.cpu_percent(interval=interval)

    return CPUMetrics(
        physical_cores=physical,
        logical_cores=logical,
        freq_current_mhz=freq_current,
        freq_max_mhz=freq_max,
        percent=percent,
        load_per_core=_load_per_core(logical),
    )
