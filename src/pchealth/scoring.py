"""Turn raw metrics into 0-100 scores and A-F grades.

Every function here is pure: it takes a dataclass from :mod:`pchealth.models`
and returns a :class:`ComponentScore`. No system calls, no I/O. That is what
makes the grading logic testable with hand-written inputs.

The thresholds below are opinionated but deliberately simple. The guiding
idea: a component sitting comfortably scores in the A/B range; a component
under pressure drops to C/D; a component that is effectively out of headroom
(a nearly full disk, a critically hot chip) fails.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from .models import (
    BatteryMetrics,
    CPUMetrics,
    ComponentScore,
    DiskMetrics,
    MemoryMetrics,
    TemperatureMetrics,
)

# Default weights for the overall grade. Components reported as unavailable
# are dropped and the remaining weights are renormalized, so a desktop with
# no battery is not punished for it.
DEFAULT_WEIGHTS: Dict[str, float] = {
    "CPU": 0.25,
    "Memory": 0.25,
    "Disk": 0.30,
    "Battery": 0.10,
    "Temperature": 0.10,
}


def grade_letter(score: float) -> str:
    """Map a 0-100 score to a single letter."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _finalize(score: float) -> Tuple[int, str]:
    """Round a raw score to a whole number and grade that same number.

    Grading the rounded value (rather than the raw float) guarantees the
    number shown to the user and its letter never disagree at a boundary.
    """
    rounded = int(round(_clamp(score)))
    return rounded, grade_letter(rounded)


def _linear_penalty(value: float, good: float, bad: float) -> float:
    """Score 100 at or below ``good``, 0 at or above ``bad``, linear between.

    Works when higher values are worse (the usual case for usage percentages).
    """
    if bad == good:
        return 100.0 if value <= good else 0.0
    if value <= good:
        return 100.0
    if value >= bad:
        return 0.0
    fraction = (value - good) / (bad - good)
    return _clamp(100.0 * (1.0 - fraction))


def score_cpu(cpu: CPUMetrics) -> ComponentScore:
    """Grade CPU on sustained usage, with load average as a tie-breaker.

    Usage is the primary signal (100% pegged is bad). When a normalized load
    average is available and exceeds 1.0 per core, an extra penalty is folded
    in, because that means work is queueing up faster than it clears.
    """
    usage_score = _linear_penalty(cpu.percent, good=50.0, bad=95.0)
    score = usage_score

    if cpu.load_per_core is not None and cpu.load_per_core > 1.0:
        # 1.0 per core = no penalty, 2.0 per core (heavily oversubscribed) = -30.
        overload = min(cpu.load_per_core - 1.0, 1.0)
        score = _clamp(score - overload * 30.0)

    cores = _describe_cores(cpu)
    summary = f"{cpu.percent:.0f}% used{cores}"
    if cpu.load_per_core is not None:
        summary += f", load/core {cpu.load_per_core:.2f}"

    final, grade = _finalize(score)
    return ComponentScore("CPU", final, grade, summary)


def _describe_cores(cpu: CPUMetrics) -> str:
    if cpu.physical_cores and cpu.logical_cores:
        return f", {cpu.physical_cores}C/{cpu.logical_cores}T"
    if cpu.logical_cores:
        return f", {cpu.logical_cores} threads"
    return ""


def score_memory(mem: MemoryMetrics) -> ComponentScore:
    """Grade RAM on usage, with heavy swap use pulling the score down.

    Swap being used at all is normal; swap being *full* means the machine is
    thrashing, so it only bites past the halfway mark.
    """
    score = _linear_penalty(mem.percent, good=60.0, bad=95.0)

    if mem.swap_total_bytes > 0 and mem.swap_percent > 50.0:
        swap_penalty = (mem.swap_percent - 50.0) / 50.0 * 20.0
        score = _clamp(score - swap_penalty)

    total_gb = mem.total_bytes / (1024 ** 3)
    avail_gb = mem.available_bytes / (1024 ** 3)
    summary = f"{mem.percent:.0f}% used, {avail_gb:.1f} GB free of {total_gb:.1f} GB"
    if mem.swap_total_bytes > 0:
        summary += f", swap {mem.swap_percent:.0f}%"

    final, grade = _finalize(score)
    return ComponentScore("Memory", final, grade, summary)


def score_disk(disk: DiskMetrics) -> ComponentScore:
    """Grade disks by their worst partition.

    A single partition running out of space can wedge the whole system, so
    the overall disk grade tracks the fullest partition rather than an
    average. Free space below 10% is penalized hard.
    """
    if not disk.partitions:
        return ComponentScore(
            "Disk", 0.0, "F", "no readable partitions", available=False
        )

    worst_score = 100.0
    worst_part = disk.partitions[0]
    for part in disk.partitions:
        # 70% used is still fine; 97% used is nearly out of room.
        part_score = _linear_penalty(part.percent, good=70.0, bad=97.0)
        if part_score < worst_score:
            worst_score = part_score
            worst_part = part

    free_gb = worst_part.free_bytes / (1024 ** 3)
    count = len(disk.partitions)
    noun = "partition" if count == 1 else "partitions"
    summary = (
        f"{count} {noun}, tightest "
        f"{worst_part.mountpoint} at {worst_part.percent:.0f}% "
        f"({free_gb:.1f} GB free)"
    )
    final, grade = _finalize(worst_score)
    return ComponentScore("Disk", final, grade, summary)


def score_battery(battery: BatteryMetrics) -> ComponentScore:
    """Grade battery on charge level.

    When plugged in, charge level is not really a health problem, so a
    plugged machine floors at a B rather than being marked down for sitting
    at 40%. A very low charge while unplugged is what actually hurts.
    """
    if not battery.available or battery.percent is None:
        return ComponentScore(
            "Battery", 0.0, "F", "not available", available=False
        )

    charge = battery.percent
    if battery.plugged:
        score = max(85.0, charge)
        state = "charging" if charge < 100 else "full"
    else:
        # Unplugged: 100% -> 100, 20% -> ~40, 0% -> 0.
        score = _clamp(20.0 + charge * 0.8)
        state = "on battery"

    summary = f"{charge:.0f}%, {state}"
    final, grade = _finalize(score)
    return ComponentScore("Battery", final, grade, summary)


def score_temperature(temp: TemperatureMetrics) -> ComponentScore:
    """Grade the hottest sensor against its own critical threshold.

    When a sensor reports a critical limit we score relative to it; otherwise
    we fall back to a generic 45C-good / 90C-bad ramp.
    """
    if not temp.available or not temp.readings:
        return ComponentScore(
            "Temperature", 0.0, "F", "no sensors", available=False
        )

    worst_score = 100.0
    hottest = temp.readings[0]
    for reading in temp.readings:
        if reading.critical:
            # 60% of the way to critical is fine; at critical, score 0.
            good = reading.critical * 0.6
            bad = reading.critical
        else:
            good, bad = 45.0, 90.0
        reading_score = _linear_penalty(reading.current, good=good, bad=bad)
        if reading_score < worst_score:
            worst_score = reading_score
            hottest = reading

    summary = f"hottest {hottest.label} at {hottest.current:.0f}C"
    final, grade = _finalize(worst_score)
    return ComponentScore("Temperature", final, grade, summary)


def overall_score(
    components: Sequence[ComponentScore],
    weights: Dict[str, float] = None,
) -> Tuple[float, str, List[ComponentScore]]:
    """Combine component scores into a weighted global grade.

    Unavailable components are excluded and the remaining weights are
    renormalized to sum to 1. Returns ``(score, grade, components)`` where
    each returned component has its effective ``weight`` filled in.
    """
    weights = weights or DEFAULT_WEIGHTS
    usable = [c for c in components if c.available]

    if not usable:
        return 0.0, "F", list(components)

    total_weight = sum(weights.get(c.name, 0.0) for c in usable)
    if total_weight <= 0:
        # Fall back to an equal split if nothing matched the weight table.
        even = 1.0 / len(usable)
        for c in usable:
            c.weight = even
        score = sum(c.score for c in usable) / len(usable)
        final, grade = _finalize(score)
        return final, grade, list(components)

    score = 0.0
    for c in usable:
        effective = weights.get(c.name, 0.0) / total_weight
        c.weight = round(effective, 4)
        score += c.score * effective

    final, grade = _finalize(score)
    return final, grade, list(components)
