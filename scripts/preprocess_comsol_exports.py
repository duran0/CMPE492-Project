#!/usr/bin/env python3
"""Normalize simple COMSOL CSV exports for downstream plotting scripts."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


COMMENT_PREFIXES = ("%", "#")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean COMSOL CSV exports into standard comma-separated CSV.")
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--delimiter", default=",", help="Input delimiter, usually ',' or ';'.")
    return parser.parse_args()


def is_data_line(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and not stripped.startswith(COMMENT_PREFIXES)


def clean_cell(cell: str) -> str:
    return " ".join(cell.strip().split())


def main() -> None:
    args = parse_args()
    lines = [line for line in args.input_csv.read_text(encoding="utf-8").splitlines() if is_data_line(line)]

    if not lines:
        raise ValueError("No data rows found after removing COMSOL comment/header lines.")

    reader = csv.reader(lines, delimiter=args.delimiter)
    rows = [[clean_cell(cell) for cell in row] for row in reader]

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.output_csv}")


if __name__ == "__main__":
    main()
