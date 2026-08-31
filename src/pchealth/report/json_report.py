"""Serialize reports and scans to plain JSON-friendly dicts."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Dict

from ..diagnostics import HealthReport
from ..models import ScanResult
from ..utils import human_size


def report_to_dict(report: HealthReport) -> Dict[str, Any]:
    """Flatten a :class:`HealthReport` into a serializable dict."""
    return {
        "generated_at": report.generated_at,
        "hostname": report.hostname,
        "platform": report.platform,
        "tool_version": report.tool_version,
        "overall": {
            "score": report.overall_score,
            "grade": report.overall_grade,
        },
        "components": [
            {
                "name": c.name,
                "available": c.available,
                "score": c.score if c.available else None,
                "grade": c.grade if c.available else None,
                "weight": c.weight,
                "summary": c.summary,
            }
            for c in report.components
        ],
        "metrics": asdict(report.metrics) if report.metrics else None,
    }


def scan_to_dict(result: ScanResult) -> Dict[str, Any]:
    """Flatten a :class:`ScanResult`, adding human-readable sizes."""
    return {
        "root": result.root,
        "total_bytes": result.total_bytes,
        "total_human": human_size(result.total_bytes),
        "files_scanned": result.files_scanned,
        "errors": result.errors,
        "top_files": [_entry_dict(e) for e in result.top_files],
        "top_dirs": [_entry_dict(e) for e in result.top_dirs],
    }


def _entry_dict(entry) -> Dict[str, Any]:
    return {
        "path": entry.path,
        "size_bytes": entry.size_bytes,
        "size_human": human_size(entry.size_bytes),
    }


def write_json(data: Dict[str, Any], path: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
