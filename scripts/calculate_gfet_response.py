#!/usr/bin/env python3
"""Calculate GFET current response from bound molecule counts."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw_csv"
PROCESSED = ROOT / "results" / "processed_csv"

E_CHARGE = 1.602176634e-19
W_OVER_L = 10.0
MU = 0.1
VDS = 0.05
AEFF = 4e-11
ALPHAS = [0.01, 0.03]


def delta_ids(n_bound: float, alpha: float) -> float:
    return W_OVER_L * E_CHARGE * MU * VDS * alpha * n_bound / AEFF


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    with (RAW / "M3_bound_molecule_count.csv").open(newline="", encoding="utf-8") as handle:
        rows = [
            row for row in csv.DictReader(handle)
            if row["sensor_config"] == "local_sensor"
        ]

    output = []
    for row in rows:
        for alpha in ALPHAS:
            ids = delta_ids(float(row["N_bound"]), alpha)
            output.append({
                "time_s": row["time_s"],
                "concentration_pM": row["concentration_pM"],
                "alpha": alpha,
                "N_bound": row["N_bound"],
                "deltaIds_A": ids,
                "deltaIds_pA": ids * 1e12,
            })

    with (PROCESSED / "M4_deltaIds_vs_time.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=output[0].keys())
        writer.writeheader()
        writer.writerows(output)

    final_rows = [row for row in output if float(row["time_s"]) == 6000]
    with (PROCESSED / "M4_deltaIds_vs_concentration.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=final_rows[0].keys())
        writer.writeheader()
        writer.writerows(final_rows)


if __name__ == "__main__":
    main()
