#!/usr/bin/env python3
"""Validate nicolive survey CSV data without filling or guessing missing values."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


REQUIRED_COLUMNS = ["dt", "lv", "kind", "season", "title", "ep", "p1", "p2", "p3", "p4", "p5", "etype", "memo"]
PERCENT_COLUMNS = ["p1", "p2", "p3", "p4", "p5"]


def is_blank(value: object) -> bool:
    return value is None or str(value).strip() == ""


def parse_percent(value: str, row_number: int, column: str, errors: list[str]) -> float | None:
    if is_blank(value):
        return None
    try:
        number = float(value)
    except ValueError:
        errors.append(f"row {row_number}: {column} is not numeric: {value!r}")
        return None
    if number < 0 or number > 100:
        errors.append(f"row {row_number}: {column} is outside 0-100: {value!r}")
    return number


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    return fieldnames, rows


def validate(path: Path, expected_count: int | None = None) -> tuple[int, dict[str, object]]:
    errors: list[str] = []
    warnings: list[str] = []
    fieldnames, rows = read_rows(path)

    if fieldnames != REQUIRED_COLUMNS:
        errors.append(f"CSV header must be exactly: {','.join(REQUIRED_COLUMNS)}")
        errors.append(f"Current header: {','.join(fieldnames)}")

    if expected_count is not None and len(rows) != expected_count:
        errors.append(f"row count is {len(rows)}, expected {expected_count}")

    old4_count = 0
    blank_percent_count = 0
    titles: set[str] = set()
    seen_keys: set[tuple[str, ...]] = set()
    duplicate_keys = 0

    for row_number, row in enumerate(rows, start=2):
        title = (row.get("title") or "").strip()
        if title:
            titles.add(title)
        else:
            warnings.append(f"row {row_number}: title is blank")

        dt = (row.get("dt") or "").strip()
        if not dt:
            warnings.append(f"row {row_number}: dt is blank")

        values = {col: parse_percent(row.get(col, ""), row_number, col, errors) for col in PERCENT_COLUMNS}
        present = [v for v in values.values() if v is not None]
        if not present:
            blank_percent_count += 1
        old4 = values["p3"] is None and all(values[col] is not None for col in ["p1", "p2", "p4", "p5"])
        if old4:
            old4_count += 1

        if present and (len(present) == 5 or old4):
            total = sum(present)
            if abs(total - 100.0) > 0.6:
                warnings.append(f"row {row_number}: percent total is {total:.1f}")

        key = (
            (row.get("dt") or "").strip(),
            (row.get("lv") or "").strip(),
            (row.get("kind") or "").strip(),
            (row.get("season") or "").strip(),
            (row.get("title") or "").strip(),
            (row.get("ep") or "").strip(),
        )
        if key in seen_keys:
            duplicate_keys += 1
        else:
            seen_keys.add(key)

    summary = {
        "csv": str(path),
        "rows": len(rows),
        "titles": len(titles),
        "old4": old4_count,
        "blank_percent_rows": blank_percent_count,
        "duplicate_keys": duplicate_keys,
        "warnings": warnings[:50],
        "warning_count": len(warnings),
        "errors": errors,
    }
    return (1 if errors else 0), summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate survey_data.csv.")
    parser.add_argument("csv_path", nargs="?", default="data/survey_data.csv")
    parser.add_argument("--expected-count", type=int, default=None)
    args = parser.parse_args()

    code, summary = validate(Path(args.csv_path), args.expected_count)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
