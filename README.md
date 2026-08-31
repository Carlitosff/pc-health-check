# pc-health-check

A command-line tool that scores your computer's health component by component (CPU, memory, disk, battery, temperature) and finds the largest files and folders eating up your disk space. Cross-platform (Windows, macOS, Linux), no bloated dependencies.

```
$ pchealth check

  Component      Score   Grade
  ────────────────────────────
  CPU             96     A
  Memory          71     D
  Disk            94     A
  Battery         88     B
  Temperature     n/a    -

  Overall: B (89/100)
```

## Why this exists

Most "system info" tools either dump raw numbers with no context, or hide behind a bloated GUI you have to install. This is a single CLI you can run anywhere, that turns raw metrics into a score you actually understand at a glance — and doubles as a quick way to find out what's eating your disk space.

## Features

- **Component scoring** — CPU, memory, disk and battery each get a 0-100 score and a letter grade (A-F), plus a weighted overall score. Anything the OS doesn't expose (temperature sensors, load average, battery on a desktop) is reported as unavailable instead of breaking or faking a number.
- **Heavy files & folders scan** — walks a directory (defaults to your home folder) and reports the largest files and folders, with human-readable sizes and their share of the total.
- **Export** — JSON for scripting, or a clean self-contained HTML report (no frameworks, no external requests) for sharing or archiving.
- **Cross-platform** — built on `psutil`, tested on Windows; degrades gracefully wherever a metric isn't available on macOS/Linux.
- **Actually tested** — the scoring logic is fully decoupled from system access, so it's covered by unit tests with no hardware dependency.

## Install

Requires Python 3.9+.

```bash
git clone https://github.com/Carlitosff/pc-health-check.git
cd pc-health-check
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
```

## Usage

Run a full diagnostic:

```bash
pchealth check
```

Find the heaviest files and folders in a directory:

```bash
pchealth scan --path ~/Downloads --top 20
```

Export a report:

```bash
pchealth check --export report.json
pchealth check --export report.html
```

Run `pchealth --help` for the full list of options.

### Full diagnostic

```bash
pchealth check
```

```
┌─ Overall health  B  (89/100) ──┐
│      Host  MSI                 │
│  Platform  Windows 11 AMD64    │
│ Generated  2026-08-31T20:21:45 │
└────────────────────────────────┘
Components
┌─────────────┬───────┬───────┬────────┬──────────────────────────────────────┐
│ Component   │ Grade │ Score │ Weight │ Details                              │
├─────────────┼───────┼───────┼────────┼──────────────────────────────────────┤
│ CPU         │   A   │   100 │    28% │ 3% used, 16C/22T, load/core 0.00     │
│ Memory      │   D   │    68 │    28% │ 71% used, 4.5 GB free of 15.5 GB     │
│ Disk        │   A   │   100 │    33% │ 1 partition, tightest C:\ at 10%     │
│ Battery     │   B   │    85 │    11% │ 49%, charging                        │
│ Temperature │  n/a  │     - │      - │ no sensors                           │
└─────────────┴───────┴───────┴────────┴──────────────────────────────────────┘
```

Unavailable components (no battery on a desktop, no temperature sensors on
Windows) are shown as `n/a` and excluded from the overall grade instead of
dragging it down.

## How scoring works

Each component is measured against thresholds picked from realistic usage, not arbitrary cutoffs — for example, disk scoring penalizes hard once free space drops below 10%, and memory scoring accounts for the fact that modern OSes intentionally keep RAM usage high via caching. Components the OS doesn't expose (temperature sensors on Windows, load average on Windows, battery on a desktop) are excluded from the weighted overall score rather than penalizing the machine for something it can't report.

The full logic lives in [`src/pchealth/scoring.py`](src/pchealth/scoring.py) — it's pure functions over plain data, with no system calls, which is what makes it unit-testable without needing real hardware.

## Project structure

```
pc-health-check/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/pchealth/
│   ├── cli.py               # argparse entry point
│   ├── models.py            # plain dataclasses shared across the codebase
│   ├── diagnostics.py       # orchestrates collectors -> scoring -> report
│   ├── scoring.py           # pure scoring logic, no system access
│   ├── collectors/          # cpu.py, memory.py, disk.py, battery.py, heavy_files.py
│   └── report/               # terminal.py (rich), json.py, html.py
└── tests/                    # pytest, mocked/fixture-based, no hardware dependency
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT — see [LICENSE](LICENSE).
