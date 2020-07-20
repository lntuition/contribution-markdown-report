import pytablewriter as ptw

from datetime import datetime, timedelta
from pytablewriter.style import Style as ptwStyle
from typing import Any, Dict, List

DATE_IDX = 0


def _get_formatted_dt(year: str, week: str) -> str:
    return f"Week {week} of {year}"


def append_csv_data(target: str, path: str, commits: List[Dict[str, Any]]) -> None:
    target_dt = datetime.strptime(target, "%Y-%m-%d")

    writer = ptw.CsvTableWriter()
    writer.from_csv(path)

    year, week, day = target_dt.isocalendar()
    formatted_dt = _get_formatted_dt(year=year, week=week)
    if day == 1 and writer.value_matrix[-1][DATE_IDX] != formatted_dt:
        writer.value_matrix.append(
            [formatted_dt] + [""] * 7)

    for commit in reversed(commits):
        if commit["data-date"] == target:
            writer.value_matrix[-1][day] = "X" if commit["data-count"] == "0" else "O"
            break
    else:
        raise Exception("Cannot find target date from commit")

    csv = writer.dumps()
    with open(path, "w") as data:
        data.write(csv)


def generate_csv_data(start: str, target: str, path: str, commits: List[Dict[str, Any]]) -> None:
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    end_dt = datetime.strptime(target, "%Y-%m-%d")

    if not timedelta(days=0) <= datetime.today() - start_dt <= timedelta(days=366):
        raise Exception("Start date must be within one year")

    writer = ptw.CsvTableWriter()
    writer.headers = ["DATE", "MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    writer.value_matrix = []

    commit_length = len(commits)
    for i in range(0, commit_length):
        if commits[i]["data-date"] == start:
            commit_idx = i
            break
    else:
        raise Exception("Cannot find start date from commit")

    while start_dt < end_dt:
        year, week, day = start_dt.isocalendar()
        formatted_dt = _get_formatted_dt(year=year, week=week)

        if not writer.value_matrix or writer.value_matrix[-1][DATE_IDX] != formatted_dt:
            writer.value_matrix.append([formatted_dt] + [""] * 7)

        writer.value_matrix[-1][day] = "X" if commits[commit_idx]["data-count"] == "0" else "O"

        start_dt += timedelta(days=1)
        commit_idx += 1

    csv = writer.dumps()
    with open(path, "w") as data:
        data.write(csv)


def generate_markdown_table(data_path: str, table_path: str) -> None:
    writer = ptw.MarkdownTableWriter()
    writer.from_csv(data_path)
    writer.column_styles = [ptwStyle(align="center")] * 8
    writer.margin = 1

    with open(table_path, "w") as table:
        writer.stream = table
        writer.write_table(flavor="github")
