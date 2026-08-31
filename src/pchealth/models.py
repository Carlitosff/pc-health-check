"""Plain data structures shared across the tool.

These dataclasses are deliberately dumb: collectors fill them with raw
numbers read from the operating system, and the scoring module turns them
into grades. Keeping the two apart means scoring can be tested with
hand-built metrics, without touching real hardware.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CPUMetrics:
    physical_cores: Optional[int]
    logical_cores: Optional[int]
    freq_current_mhz: Optional[float]
    freq_max_mhz: Optional[float]
    percent: float
    # Load average over 1 minute, already divided by the number of logical
    # cores (so 1.0 means "fully loaded"). None when the platform does not
    # expose it in a meaningful way.
    load_per_core: Optional[float] = None


@dataclass
class MemoryMetrics:
    total_bytes: int
    available_bytes: int
    used_bytes: int
    percent: float
    swap_total_bytes: int
    swap_used_bytes: int
    swap_percent: float


@dataclass
class DiskPartition:
    device: str
    mountpoint: str
    fstype: str
    total_bytes: int
    used_bytes: int
    free_bytes: int
    percent: float


@dataclass
class DiskMetrics:
    partitions: List[DiskPartition] = field(default_factory=list)


@dataclass
class BatteryMetrics:
    available: bool
    percent: Optional[float] = None
    plugged: Optional[bool] = None
    secs_left: Optional[int] = None


@dataclass
class TemperatureReading:
    label: str
    current: float
    high: Optional[float] = None
    critical: Optional[float] = None


@dataclass
class TemperatureMetrics:
    available: bool
    readings: List[TemperatureReading] = field(default_factory=list)

    @property
    def max_current(self) -> Optional[float]:
        if not self.readings:
            return None
        return max(reading.current for reading in self.readings)


@dataclass
class SystemMetrics:
    """Everything a full diagnostic collects, in one bag."""

    cpu: CPUMetrics
    memory: MemoryMetrics
    disk: DiskMetrics
    battery: BatteryMetrics
    temperature: TemperatureMetrics


@dataclass
class ComponentScore:
    """The result of grading one component."""

    name: str
    score: float          # 0-100
    grade: str            # A-F
    summary: str          # short human-readable line
    available: bool = True
    # Weight this component carried in the overall grade. Filled in by the
    # aggregator so reports can show how the global number was built.
    weight: float = 0.0


@dataclass
class FileEntry:
    path: str
    size_bytes: int


@dataclass
class ScanResult:
    root: str
    top_files: List[FileEntry] = field(default_factory=list)
    top_dirs: List[FileEntry] = field(default_factory=list)
    total_bytes: int = 0
    files_scanned: int = 0
    errors: int = 0
