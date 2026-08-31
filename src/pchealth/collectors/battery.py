"""Battery metrics collector."""

from __future__ import annotations

import psutil

from ..models import BatteryMetrics


def collect_battery() -> BatteryMetrics:
    """Read battery state, or report it as unavailable on desktops.

    ``psutil.sensors_battery`` returns ``None`` on machines without a
    battery and is missing entirely on some platforms, so both cases are
    handled as "not available".
    """
    sensor = getattr(psutil, "sensors_battery", None)
    if sensor is None:
        return BatteryMetrics(available=False)

    try:
        battery = sensor()
    except (NotImplementedError, AttributeError, OSError):
        return BatteryMetrics(available=False)

    if battery is None:
        return BatteryMetrics(available=False)

    secs_left = battery.secsleft
    # psutil uses sentinel constants for "unknown" / "plugged in".
    if secs_left in (psutil.POWER_TIME_UNKNOWN, psutil.POWER_TIME_UNLIMITED):
        secs_left = None

    return BatteryMetrics(
        available=True,
        percent=round(battery.percent, 1),
        plugged=battery.power_plugged,
        secs_left=secs_left,
    )
