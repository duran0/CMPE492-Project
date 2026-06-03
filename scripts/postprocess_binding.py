#!/usr/bin/env python3
"""Regenerate M1 binding kinetics tables from documented assumptions."""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw_csv"

TIMES = [0, 100, 500, 1000, 2000, 4000, 6000]
CONCENTRATIONS_PM = [0.5, 1, 10, 100, 1000]
KD_PM = 10.0
KF = 1e7
KR = KF * KD_PM * 1e-12


def theta_eq(concentration_pm: float) -> float:
    return concentration_pm / (KD_PM + concentration_pm)


def theta_at_time(concentration_pm: float, time_s: float) -> float:
    kobs = KF * concentration_pm * 1e-12 + KR
    return theta_eq(concentration_pm) * (1 - math.exp(-kobs * time_s))


def write_csv(path: Path, rows: list[dict[str, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    write_csv(
        RAW / "M1_binding_timecourse.csv",
        [
            {
                "time_s": time_s,
                "concentration_pM": 10.0,
                "theta": theta_at_time(10.0, time_s),
                "free_fraction": 1 - theta_at_time(10.0, time_s),
                "kobs_per_s": KF * 10e-12 + KR,
            }
            for time_s in TIMES
        ],
    )
    write_csv(
        RAW / "M1_equilibrium_occupancy_vs_C.csv",
        [
            {
                "concentration_pM": concentration_pm,
                "concentration_M": concentration_pm * 1e-12,
                "theta_eq": theta_eq(concentration_pm),
                "kf_1_per_M_s": KF,
                "kr_1_per_s": KR,
                "kd_from_rates_M": KR / KF,
            }
            for concentration_pm in CONCENTRATIONS_PM
        ],
    )


if __name__ == "__main__":
    main()
