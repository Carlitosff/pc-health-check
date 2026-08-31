"""Command-line entry point for pc-health-check.

Usage:
    pchealth check [--export report.json] [--export report.html]
    pchealth scan --path ~/Downloads --top 20 [--export scan.html]
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List, Optional

from rich.console import Console

from . import __version__
from .collectors.heavy_files import scan_path
from .diagnostics import build_report
from .report import (
    render_report,
    render_scan,
    report_to_dict,
    scan_to_dict,
    write_html_report,
    write_html_scan,
    write_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pchealth",
        description="Grade your computer by component and find heavy files.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    sub = parser.add_subparsers(dest="command", metavar="command")

    check = sub.add_parser("check", help="Run a full component diagnostic.")
    check.add_argument(
        "--export",
        action="append",
        metavar="FILE",
        help="Write the report to FILE. Format is chosen by the .json or "
        ".html extension. May be given more than once.",
    )
    check.add_argument(
        "--cpu-interval",
        type=float,
        default=0.5,
        metavar="SECONDS",
        help="Sampling window for CPU usage (default: 0.5).",
    )
    check.set_defaults(func=_cmd_check)

    scan = sub.add_parser("scan", help="Find the heaviest files and folders.")
    scan.add_argument(
        "--path",
        default=os.path.expanduser("~"),
        help="Directory to scan (default: your home folder).",
    )
    scan.add_argument(
        "--top",
        type=int,
        default=10,
        metavar="N",
        help="How many entries to show for files and folders (default: 10).",
    )
    scan.add_argument(
        "--export",
        action="append",
        metavar="FILE",
        help="Write the scan to FILE (.json or .html). May be repeated.",
    )
    scan.set_defaults(func=_cmd_scan)

    return parser


def _export_format(path: str) -> Optional[str]:
    lower = path.lower()
    if lower.endswith(".json"):
        return "json"
    if lower.endswith(".html") or lower.endswith(".htm"):
        return "html"
    return None


def _cmd_check(args: argparse.Namespace, console: Console) -> int:
    report = build_report(cpu_interval=args.cpu_interval)
    render_report(report, console)

    for target in args.export or []:
        fmt = _export_format(target)
        if fmt == "json":
            write_json(report_to_dict(report), target)
        elif fmt == "html":
            write_html_report(report, target)
        else:
            console.print(
                f"[yellow]Skipping {target}: use a .json or .html extension.[/]"
            )
            continue
        console.print(f"[dim]Wrote {fmt.upper()} report to {target}[/]")
    return 0


def _cmd_scan(args: argparse.Namespace, console: Console) -> int:
    if args.top < 1:
        console.print("[red]--top must be at least 1.[/]")
        return 2
    try:
        result = scan_path(args.path, top_n=args.top)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/]")
        return 1

    render_scan(result, console)

    for target in args.export or []:
        fmt = _export_format(target)
        if fmt == "json":
            write_json(scan_to_dict(result), target)
        elif fmt == "html":
            write_html_scan(result, target)
        else:
            console.print(
                f"[yellow]Skipping {target}: use a .json or .html extension.[/]"
            )
            continue
        console.print(f"[dim]Wrote {fmt.upper()} scan to {target}[/]")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    console = Console()

    if not getattr(args, "command", None):
        parser.print_help()
        return 0

    try:
        return args.func(args, console)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/]")
        return 130


if __name__ == "__main__":
    sys.exit(main())
