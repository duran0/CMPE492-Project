#!/usr/bin/env python3
"""Reduced-order transport post-processing used before final 3D COMSOL exports."""

from __future__ import annotations

import csv
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw_csv"
PROCESSED = ROOT / "results" / "processed_csv"

TIMES = [0, 100, 500, 1000, 2000, 4000, 6000]
RATIOS = [0.1, 0.25, 0.5, 0.75, 1.0]
C0_PM = 10.0
TAU_CORTEX = 700.0


def cortex(time_s: float) -> float:
    return C0_PM * (1 - math.exp(-time_s / TAU_CORTEX))


def medulla(time_s: float, ratio: float) -> float:
    tau = 700.0 + 3500.0 / ratio
    return C0_PM * (1 - math.exp(-time_s / tau))


def write_csv(path: Path, rows: list[dict[str, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    cortex_rows = []
    medulla_rows = []
    delay_rows = []
    for ratio in RATIOS:
        for time_s in TIMES:
            cortex_rows.append({"time_s": time_s, "r": ratio, "cortex_avg_pM": cortex(time_s)})
            medulla_rows.append({"time_s": time_s, "r": ratio, "medulla_avg_pM": medulla(time_s, ratio)})
        tau = 700.0 + 3500.0 / ratio
        delay_rows.append({"r": ratio, "medulla_time_to_50pct_s": -tau * math.log(0.5)})
    write_csv(RAW / "M2_avg_concentration_cortex.csv", cortex_rows)
    write_csv(RAW / "M2_avg_concentration_medulla.csv", medulla_rows)
    write_csv(PROCESSED / "M2_delay_vs_diffusivity_ratio.csv", delay_rows)


if __name__ == "__main__":
    main()
