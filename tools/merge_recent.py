#!/usr/bin/env python3
"""Merge checked recent rows into survey_data.csv without guessing missing values."""

from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path


REQUIRED_COLUMNS = ["dt", "lv", "kind", "season", "title", "ep", "p1", "p2", "p3", "p4", "p5", "etype", "memo"]


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return REQUIRED_COLUMNS, []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in REQUIRED_COLUMNS})
    shutil.move(str(tmp), str(path))


def row_key(row: dict[str, str]) -> tuple[str, ...]:
    lv = (row.get("lv") or "").strip()
    if lv:
        return ("lv", lv)
    return (
        "natural",
        (row.get("dt") or "").strip(),
        (row.get("kind") or "").strip(),
        (row.get("season") or "").strip(),
        (row.get("title") or "").strip(),
        (row.get("ep") or "").strip(),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge data/inbox/recent_rows.csv into data/survey_data.csv.")
    parser.add_argument("--base", default="data/survey_data.csv")
    parser.add_argument("--recent", default="data/inbox/recent_rows.csv")
    parser.add_argument("--out", default="data/survey_data.csv")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    base_path = Path(args.base)
    recent_path = Path(args.recent)
    out_path = Path(args.out)

    base_header, base_rows = read_rows(base_path)
    recent_header, recent_rows = read_rows(recent_path)

    if base_header != REQUIRED_COLUMNS:
        raise SystemExit(f"{base_path} header is invalid")
    if recent_rows and recent_header != REQUIRED_COLUMNS:
        raise SystemExit(f"{recent_path} header is invalid")

    seen = {row_key(row) for row in base_rows}
    additions: list[dict[str, str]] = []
    skipped = 0

    for row in recent_rows:
        if not any((row.get(key) or "").strip() for key in REQUIRED_COLUMNS):
            continue
        key = row_key(row)
        if key in seen:
            skipped += 1
            continue
        seen.add(key)
        additions.append({col: row.get(col, "") for col in REQUIRED_COLUMNS})

    merged = additions + base_rows
    print(f"base rows: {len(base_rows)}")
    print(f"recent rows: {len(recent_rows)}")
    print(f"added rows: {len(additions)}")
    print(f"skipped duplicates: {skipped}")
    print(f"merged rows: {len(merged)}")

    if not args.dry_run:
        write_rows(out_path, merged)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
