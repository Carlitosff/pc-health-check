"""Orchestration: collect metrics, grade them, bundle a report.

This is the glue between :mod:`pchealth.collectors` (system data) and
:mod:`pchealth.scoring` (grades). The reporters consume :class:`HealthReport`.
"""

from __future__ import annotations

import platform
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from . import __version__, scoring
from .collectors import collect_system
from .models import ComponentScore, SystemMetrics


@dataclass
class HealthReport:
    generated_at: str
    hostname: str
    platform: str
    tool_version: str
    overall_score: float
    overall_grade: str
    components: List[ComponentScore] = field(default_factory=list)
    metrics: SystemMetrics = None


def build_report(cpu_interval: float = 0.5) -> HealthReport:
    """Run a full diagnostic and return a graded report."""
    metrics = collect_system(cpu_interval=cpu_interval)
    components = grade_metrics(metrics)
    score, grade, components = scoring.overall_score(components)

    return HealthReport(
        generated_at=datetime.now().isoformat(timespec="seconds"),
        hostname=platform.node(),
        platform=_platform_string(),
        tool_version=__version__,
        overall_score=score,
        overall_grade=grade,
        components=components,
        metrics=metrics,
    )


def grade_metrics(metrics: SystemMetrics) -> List[ComponentScore]:
    """Score every component of a :class:`SystemMetrics` bag."""
    return [
        scoring.score_cpu(metrics.cpu),
        scoring.score_memory(metrics.memory),
        scoring.score_disk(metrics.disk),
        scoring.score_battery(metrics.battery),
        scoring.score_temperature(metrics.temperature),
    ]


def _platform_string() -> str:
    system = platform.system() or "Unknown"
    release = platform.release()
    machine = platform.machine()
    parts = [p for p in (system, release, machine) if p]
    return " ".join(parts)
