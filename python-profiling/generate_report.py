from enum import StrEnum
from pathlib import Path
from pstats import Stats, SortKey
from typing import Optional

import typer


class ReportType(StrEnum):
    STATS = "stats"
    CALLERS = "callers"
    CALLEES = "callees"


def main(path: Path,
         strip_dirs: bool = True,
         report_type: ReportType = ReportType.STATS,
         sort_by: SortKey = SortKey.CUMULATIVE,
         max_lines: Optional[int] = typer.Option(None, min=1, help="Count of lines"),
         percent_lines: Optional[int] = typer.Option(None, min=1, max=100, help="Percentage of lines"),
         re_filter: Optional[str] = typer.Option(None, help="Reg exp to match name")):
    if not path.is_file():
        print(f"File '{path}' doesn't exist")
        raise typer.Exit(1)

    stats = Stats(str(path))
    if strip_dirs:
        stats = stats.strip_dirs()
    stats = stats.sort_stats(sort_by)

    restrictions = []
    if max_lines is not None:
        restrictions.append(max_lines)
    if percent_lines is not None:
        restrictions.append(float(percent_lines) / 100)
    if re_filter is not None:
        restrictions.append(re_filter)

    match report_type:
        case ReportType.STATS:
            stats.print_stats(*restrictions)
        case ReportType.CALLERS:
            stats.print_callers(*restrictions)
        case ReportType.CALLEES:
            stats.print_callees(*restrictions)


typer.run(main)
