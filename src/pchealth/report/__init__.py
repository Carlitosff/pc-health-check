"""Report renderers: terminal (rich), JSON and HTML."""

from __future__ import annotations

from .html import write_html_report, write_html_scan
from .json_report import report_to_dict, scan_to_dict, write_json
from .terminal import render_report, render_scan

__all__ = [
    "render_report",
    "render_scan",
    "report_to_dict",
    "scan_to_dict",
    "write_json",
    "write_html_report",
    "write_html_scan",
]
