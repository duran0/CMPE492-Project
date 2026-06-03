#!/usr/bin/env python3
"""Estimate sensitivity and limit of detection from response data."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Estimate LOD using LOD = 3 * sigma / sensitivity."
    )
    parser.add_argument("input_csv", type=Path, help="CSV containing concentration and response columns.")
    parser.add_argument("--concentration-column", default="concentration_pM")
    parser.add_argument("--response-column", default="delta_ids_A")
    parser.add_argument("--blank-column", default=None, help="Optional column with blank/noise response values.")
    parser.add_argument("--noise-sigma-a", type=float, default=None, help="Known current noise standard deviation in A.")
    parser.add_argument("--output-csv", type=Path, default=None, help="Optional one-row CSV output path.")
    return parser.parse_args()


def read_float(value: str) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def linear_slope(points: list[tuple[float, float]]) -> float:
    if len(points) < 2:
        raise ValueError("At least two concentration-response points are required.")

    mean_x = statistics.fmean(point[0] for point in points)
    mean_y = statistics.fmean(point[1] for point in points)
    numerator = sum((x_value - mean_x) * (y_value - mean_y) for x_value, y_value in points)
    denominator = sum((x_value - mean_x) ** 2 for x_value, _ in points)
    if denominator == 0:
        raise ValueError("Concentration values must not all be identical.")
    return numerator / denominator


def residual_sigma(points: list[tuple[float, float]], slope: float) -> float:
    intercept = statistics.fmean(y_value - slope * x_value for x_value, y_value in points)
    residuals = [y_value - (slope * x_value + intercept) for x_value, y_value in points]
    if len(residuals) < 3:
        raise ValueError("Residual sigma needs at least three points. Provide --noise-sigma-a instead.")
    return statistics.stdev(residuals)


def main() -> None:
    args = parse_args()
    rows = load_rows(args.input_csv)

    points: list[tuple[float, float]] = []
    blank_values: list[float] = []

    for row in rows:
        concentration = read_float(row.get(args.concentration_column, ""))
        response = read_float(row.get(args.response_column, ""))
        if concentration is not None and response is not None:
            points.append((concentration, response))

        if args.blank_column:
            blank = read_float(row.get(args.blank_column, ""))
            if blank is not None:
                blank_values.append(blank)

    sensitivity = linear_slope(points)

    if args.noise_sigma_a is not None:
        sigma = args.noise_sigma_a
    elif blank_values:
        if len(blank_values) < 2:
            raise ValueError("Blank-column sigma needs at least two blank values.")
        sigma = statistics.stdev(blank_values)
    else:
        sigma = residual_sigma(points, sensitivity)

    if sensitivity == 0:
        raise ValueError("Sensitivity is zero; LOD cannot be calculated.")

    lod = 3 * sigma / abs(sensitivity)
    result = {
        "sensitivity_A_per_pM": sensitivity,
        "sigma_A": sigma,
        "lod_pM": lod,
        "points_used": len(points),
    }

    if args.output_csv:
        with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=result.keys())
            writer.writeheader()
            writer.writerow(result)

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
