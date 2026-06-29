#!/usr/bin/env python3
"""Build index.html from src/index.template.html and data/survey_data.csv."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from pathlib import Path


KEYS = ["dt", "lv", "kind", "season", "title", "ep", "p1", "p2", "p3", "p4", "p5", "etype", "memo"]
PERCENT_KEYS = {"p1", "p2", "p3", "p4", "p5"}
DEFAULT_AFFILIATE_CONFIG = {
    "enabled": False,
    "siteName": "ニコ生アニメアンケート資料室",
    "rakutenLinks": [],
}


def blank(value: object) -> bool:
    return value is None or str(value).strip() == ""


def csv_value(row: dict[str, str], key: str) -> object:
    value = row.get(key, "")
    if key in PERCENT_KEYS:
        if blank(value):
            return None
        return float(value)
    return "" if value is None else str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != KEYS:
            raise SystemExit(f"{path} header is invalid")
        return list(reader)


def old4(row: dict[str, str]) -> bool:
    return blank(row.get("p3")) and all(not blank(row.get(key)) for key in ["p1", "p2", "p4", "p5"])


def meta_for(rows: list[dict[str, str]], csv_path: Path) -> dict[str, object]:
    dates = [row["dt"] for row in rows if row.get("dt")]
    return {
        "count": len(rows),
        "titles": len({row["title"] for row in rows if row.get("title")}),
        "old4": sum(1 for row in rows if old4(row)),
        "minDate": min(dates) if dates else "",
        "maxDate": max(dates) if dates else "",
        "csvSha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
    }


def load_affiliate_config(path: Path | None) -> dict[str, object]:
    if path and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return DEFAULT_AFFILIATE_CONFIG


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the single-file public site.")
    parser.add_argument("--csv", default="data/survey_data.csv")
    parser.add_argument("--template", default="src/index.template.html")
    parser.add_argument("--out", default="index.html")
    parser.add_argument("--affiliate-config", default="data/affiliate_config.json")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    template_path = Path(args.template)
    out_path = Path(args.out)
    affiliate_path = Path(args.affiliate_config) if args.affiliate_config else None

    rows = read_csv(csv_path)
    raw = [[csv_value(row, key) for key in KEYS] for row in rows]
    meta = meta_for(rows, csv_path)
    affiliate_config = load_affiliate_config(affiliate_path)

    html = template_path.read_text(encoding="utf-8")
    replacements = {
        "__META_JSON__": json.dumps(meta, ensure_ascii=False, separators=(",", ":")),
        "__RAW_JSON__": json.dumps(raw, ensure_ascii=False, separators=(",", ":")),
        "__AFFILIATE_CONFIG_JSON__": json.dumps(affiliate_config, ensure_ascii=False, separators=(",", ":")),
    }
    for marker, value in replacements.items():
        if marker not in html:
            raise SystemExit(f"template marker not found: {marker}")
        html = html.replace(marker, value)

    if out_path.exists():
        backup_path = out_path.with_suffix(out_path.suffix + ".bak")
        shutil.copy2(out_path, backup_path)
    out_path.write_text(html, encoding="utf-8", newline="\n")
    print(f"built {out_path} with {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
