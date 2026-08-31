"""Temperature sensor collector.

Hardware temperature is only exposed reliably on Linux. On Windows and
macOS psutil has no ``sensors_temperatures`` at all, so this collector is
built to report "not available" cleanly instead of failing.
"""

from __future__ import annotations

import psutil

from ..models import TemperatureMetrics, TemperatureReading


def collect_temperature() -> TemperatureMetrics:
    sensor = getattr(psutil, "sensors_temperatures", None)
    if sensor is None:
        return TemperatureMetrics(available=False)

    try:
        groups = sensor()
    except (NotImplementedError, AttributeError, OSError):
        return TemperatureMetrics(available=False)

    if not groups:
        return TemperatureMetrics(available=False)

    readings = []
    for chip, entries in groups.items():
        for entry in entries:
            if entry.current is None:
                continue
            label = entry.label or chip
            readings.append(
                TemperatureReading(
                    label=label,
                    current=float(entry.current),
                    high=entry.high,
                    critical=entry.critical,
                )
            )

    if not readings:
        return TemperatureMetrics(available=False)

    return TemperatureMetrics(available=True, readings=readings)
