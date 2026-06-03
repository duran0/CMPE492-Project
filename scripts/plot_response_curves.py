#!/usr/bin/env python3
"""Plot HER2 concentration-response curves from CSV exports."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot GFET response curves from exported CSV data.")
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--x-column", default="concentration_pM")
    parser.add_argument("--y-column", default="delta_ids_A")
    parser.add_argument("--occupancy-column", default=None)
    parser.add_argument("--output", type=Path, default=Path("results/electrical_response/response_curve.png"))
    parser.add_argument("--log-x", action="store_true", help="Use logarithmic x-axis.")
    return parser.parse_args()


def read_float(value: str) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def load_series(path: Path, x_column: str, y_column: str) -> tuple[list[float], list[float]]:
    x_values: list[float] = []
    y_values: list[float] = []

    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            x_value = read_float(row.get(x_column, ""))
            y_value = read_float(row.get(y_column, ""))
            if x_value is None or y_value is None:
                continue
            x_values.append(x_value)
            y_values.append(y_value)

    if not x_values:
        raise ValueError(f"No numeric data found for {x_column} and {y_column}.")

    return x_values, y_values


def main() -> None:
    args = parse_args()

    import matplotlib.pyplot as plt

    x_values, y_values = load_series(args.input_csv, args.x_column, args.y_column)

    fig, axis = plt.subplots(figsize=(6.5, 4.0))
    axis.plot(x_values, y_values, marker="o", linewidth=1.8)
    axis.set_xlabel(args.x_column)
    axis.set_ylabel(args.y_column)
    axis.grid(True, alpha=0.3)

    if args.log_x:
        axis.set_xscale("log")

    if args.occupancy_column:
        _, occupancy_values = load_series(args.input_csv, args.x_column, args.occupancy_column)
        twin_axis = axis.twinx()
        twin_axis.plot(x_values, occupancy_values, marker="s", linestyle="--", color="tab:orange")
        twin_axis.set_ylabel(args.occupancy_column)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(args.output, dpi=300)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
