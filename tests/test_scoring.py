"""Tests for the pure grading logic.

None of these touch real hardware: every input is a hand-built dataclass,
which is the whole point of keeping scoring separate from collection.
"""

from __future__ import annotations

import pytest

from pchealth import scoring
from pchealth.models import (
    BatteryMetrics,
    CPUMetrics,
    ComponentScore,
    DiskMetrics,
    DiskPartition,
    MemoryMetrics,
    TemperatureMetrics,
    TemperatureReading,
)


# --- grade_letter ----------------------------------------------------------


@pytest.mark.parametrize(
    "score,expected",
    [
        (100, "A"),
        (90, "A"),
        (89.9, "B"),
        (80, "B"),
        (70, "C"),
        (60, "D"),
        (59.9, "F"),
        (0, "F"),
    ],
)
def test_grade_letter_boundaries(score, expected):
    assert scoring.grade_letter(score) == expected


# --- CPU -------------------------------------------------------------------


def _cpu(percent, load=None):
    return CPUMetrics(
        physical_cores=4,
        logical_cores=8,
        freq_current_mhz=2400,
        freq_max_mhz=3200,
        percent=percent,
        load_per_core=load,
    )


def test_idle_cpu_scores_top():
    result = scoring.score_cpu(_cpu(5))
    assert result.score == 100
    assert result.grade == "A"


def test_pegged_cpu_fails():
    result = scoring.score_cpu(_cpu(99))
    assert result.score < 60
    assert result.grade == "F"


def test_cpu_usage_is_monotonic():
    low = scoring.score_cpu(_cpu(30)).score
    mid = scoring.score_cpu(_cpu(70)).score
    high = scoring.score_cpu(_cpu(90)).score
    assert low > mid > high


def test_cpu_overload_penalty_applies():
    without = scoring.score_cpu(_cpu(60, load=None)).score
    with_load = scoring.score_cpu(_cpu(60, load=2.0)).score
    assert with_load < without


def test_cpu_normal_load_no_penalty():
    baseline = scoring.score_cpu(_cpu(60, load=None)).score
    normal = scoring.score_cpu(_cpu(60, load=0.8)).score
    assert normal == baseline


# --- Memory ----------------------------------------------------------------


def _mem(percent, swap_total=8 * 1024 ** 3, swap_percent=0.0):
    total = 16 * 1024 ** 3
    used = int(total * percent / 100)
    return MemoryMetrics(
        total_bytes=total,
        available_bytes=total - used,
        used_bytes=used,
        percent=percent,
        swap_total_bytes=swap_total,
        swap_used_bytes=int(swap_total * swap_percent / 100),
        swap_percent=swap_percent,
    )


def test_memory_comfortable_scores_high():
    assert scoring.score_memory(_mem(40)).score == 100


def test_memory_pressure_lowers_score():
    assert scoring.score_memory(_mem(97)).score < 20


def test_heavy_swap_penalty():
    no_swap = scoring.score_memory(_mem(70, swap_percent=0)).score
    thrashing = scoring.score_memory(_mem(70, swap_percent=90)).score
    assert thrashing < no_swap


def test_no_swap_device_ignored():
    # A machine with swap disabled should not be penalized for swap.
    result = scoring.score_memory(_mem(50, swap_total=0, swap_percent=0))
    assert result.score == 100


# --- Disk ------------------------------------------------------------------


def _part(mount, percent):
    total = 500 * 1024 ** 3
    used = int(total * percent / 100)
    return DiskPartition(
        device=mount,
        mountpoint=mount,
        fstype="ext4",
        total_bytes=total,
        used_bytes=used,
        free_bytes=total - used,
        percent=percent,
    )


def test_disk_tracks_worst_partition():
    disk = DiskMetrics(partitions=[_part("C:", 40), _part("D:", 98)])
    result = scoring.score_disk(disk)
    # The nearly-full D: should drive the grade down even though C: is fine.
    assert result.grade == "F"
    assert "D:" in result.summary


def test_disk_healthy():
    disk = DiskMetrics(partitions=[_part("C:", 50)])
    assert scoring.score_disk(disk).score == 100


def test_disk_no_partitions_unavailable():
    result = scoring.score_disk(DiskMetrics(partitions=[]))
    assert result.available is False


# --- Battery ---------------------------------------------------------------


def test_battery_absent_is_unavailable():
    result = scoring.score_battery(BatteryMetrics(available=False))
    assert result.available is False


def test_battery_low_on_battery_fails():
    result = scoring.score_battery(
        BatteryMetrics(available=True, percent=10, plugged=False)
    )
    assert result.grade in {"D", "F"}


def test_battery_plugged_has_floor():
    # A plugged laptop at 40% should not be graded as failing.
    result = scoring.score_battery(
        BatteryMetrics(available=True, percent=40, plugged=True)
    )
    assert result.score >= 85


# --- Temperature -----------------------------------------------------------


def test_temperature_absent_is_unavailable():
    result = scoring.score_temperature(TemperatureMetrics(available=False))
    assert result.available is False


def test_temperature_cool_scores_high():
    temp = TemperatureMetrics(
        available=True,
        readings=[TemperatureReading("cpu", current=40, critical=100)],
    )
    assert scoring.score_temperature(temp).score == 100


def test_temperature_near_critical_fails():
    temp = TemperatureMetrics(
        available=True,
        readings=[TemperatureReading("cpu", current=99, critical=100)],
    )
    assert scoring.score_temperature(temp).grade == "F"


# --- Overall ---------------------------------------------------------------


def test_overall_renormalizes_when_component_missing():
    components = [
        ComponentScore("CPU", 100, "A", ""),
        ComponentScore("Memory", 100, "A", ""),
        ComponentScore("Disk", 100, "A", ""),
        ComponentScore("Battery", 0, "F", "", available=False),
        ComponentScore("Temperature", 0, "F", "", available=False),
    ]
    score, grade, returned = scoring.overall_score(components)
    # Battery/Temperature are unavailable, so three perfect components -> 100.
    assert score == 100
    assert grade == "A"
    # Weights of the available components renormalize to sum to 1.
    weight_sum = sum(c.weight for c in returned if c.available)
    assert weight_sum == pytest.approx(1.0)


def test_overall_all_unavailable_returns_f():
    components = [ComponentScore("CPU", 0, "F", "", available=False)]
    score, grade, _ = scoring.overall_score(components)
    assert score == 0
    assert grade == "F"


def test_overall_weighting_favours_disk():
    # Disk carries the most weight, so a bad disk should hurt more than a
    # bad battery of the same score.
    bad_disk = [
        ComponentScore("CPU", 100, "A", ""),
        ComponentScore("Memory", 100, "A", ""),
        ComponentScore("Disk", 0, "F", ""),
        ComponentScore("Battery", 100, "A", ""),
        ComponentScore("Temperature", 100, "A", ""),
    ]
    bad_battery = [
        ComponentScore("CPU", 100, "A", ""),
        ComponentScore("Memory", 100, "A", ""),
        ComponentScore("Disk", 100, "A", ""),
        ComponentScore("Battery", 0, "F", ""),
        ComponentScore("Temperature", 100, "A", ""),
    ]
    disk_score, _, _ = scoring.overall_score(bad_disk)
    battery_score, _, _ = scoring.overall_score(bad_battery)
    assert disk_score < battery_score
