"""Terminal rendering with rich."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..diagnostics import HealthReport
from ..models import ComponentScore, ScanResult
from ..utils import human_size

# Grade -> colour, reused by both the summary panel and the per-row cells.
_GRADE_COLOR = {
    "A": "bright_green",
    "B": "green",
    "C": "yellow",
    "D": "dark_orange",
    "F": "bright_red",
}


def _grade_text(grade: str) -> Text:
    return Text(grade, style=f"bold {_GRADE_COLOR.get(grade, 'white')}")


def render_report(report: HealthReport, console: Console = None) -> None:
    """Print a full diagnostic to the terminal."""
    console = console or Console()

    header = Table.grid(padding=(0, 2))
    header.add_column(justify="right", style="dim")
    header.add_column()
    header.add_row("Host", report.hostname or "unknown")
    header.add_row("Platform", report.platform)
    header.add_row("Generated", report.generated_at)

    grade_color = _GRADE_COLOR.get(report.overall_grade, "white")
    banner = Text.assemble(
        ("Overall health  ", "bold"),
        (f"{report.overall_grade}", f"bold {grade_color}"),
        (f"  ({report.overall_score:.0f}/100)", grade_color),
    )
    console.print(Panel(header, title=banner, border_style=grade_color, expand=False))

    table = Table(title="Components", title_justify="left", header_style="bold")
    table.add_column("Component")
    table.add_column("Grade", justify="center")
    table.add_column("Score", justify="right")
    table.add_column("Weight", justify="right")
    table.add_column("Details", overflow="fold")

    for component in report.components:
        table.add_row(*_component_row(component))

    console.print(table)


def _component_row(component: ComponentScore):
    if not component.available:
        return (
            component.name,
            Text("n/a", style="dim"),
            Text("-", style="dim"),
            Text("-", style="dim"),
            Text(component.summary, style="dim"),
        )
    weight = f"{component.weight * 100:.0f}%" if component.weight else "-"
    return (
        component.name,
        _grade_text(component.grade),
        f"{component.score:.0f}",
        weight,
        component.summary,
    )


def render_scan(result: ScanResult, console: Console = None) -> None:
    """Print the heavy-file scan to the terminal."""
    console = console or Console()

    summary = Text.assemble(
        ("Scanned  ", "dim"),
        (result.root, "bold"),
        (f"\n{result.files_scanned:,} files  ", "dim"),
        (f"{human_size(result.total_bytes)} total", "bold"),
    )
    if result.errors:
        summary.append(f"  ({result.errors} unreadable)", style="dim")
    console.print(Panel(summary, border_style="cyan", expand=False))

    if result.top_dirs:
        console.print(_entries_table("Heaviest folders", result.top_dirs, result.total_bytes))
    if result.top_files:
        console.print(_entries_table("Heaviest files", result.top_files, result.total_bytes))


def _entries_table(title: str, entries, total: int) -> Table:
    table = Table(title=title, title_justify="left", header_style="bold")
    table.add_column("#", justify="right", style="dim")
    table.add_column("Size", justify="right")
    table.add_column("Share", justify="right", style="dim")
    table.add_column("Path", overflow="fold")

    for index, entry in enumerate(entries, start=1):
        share = f"{entry.size_bytes / total * 100:.1f}%" if total else "-"
        table.add_row(
            str(index),
            Text(human_size(entry.size_bytes), style="bold"),
            share,
            entry.path,
        )
    return table


__all__ = ["render_report", "render_scan"]
