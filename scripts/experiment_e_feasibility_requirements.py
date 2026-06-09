#!/usr/bin/env python3
"""Experiment E: GFET-HER2 feasibility requirement map.

This script converts the Debye-screening limitation into explicit design
requirements for coupling efficiency, receptor-channel distance, and current
noise floor. It uses the same M2B reference exposure approximation, M3
Langmuir surface binding, and M4 GFET current equation used in the final
simulation campaign.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "results" / "processed_csv"
PLOTS = ROOT / "results" / "plots"
REPORT_FIGURES = ROOT / "results" / "figures_for_report"
POSTER_FIGURES = ROOT / "results" / "figures_for_poster"

AVOGADRO = 6.02214076e23
E_CHARGE = 1.602176634e-19
BMAX_MOL_M2 = 8.30e-12
LOCAL_AREA_M2 = 4e-11
W_OVER_L = 10.0
MU = 0.1
VDS = 0.05
AEFF_M2 = 4e-11

M2B_REFERENCE_RATIO = 0.5
M2B_REFERENCE_VELOCITY_M_S = 5e-7
REFERENCE_TIME_S = 6000.0
BASELINE_CONCENTRATION_PM = 10.0

CONCENTRATIONS_PM = [0.5, 1.0, 10.0, 100.0, 1000.0]
KD_VALUES_PM = [1.0, 10.0, 100.0]
ALPHA0_VALUES = [0.01, 0.03, 0.1]
NOISE_FLOORS_PA = [1.0, 5.0, 10.0, 50.0, 100.0]
LAMBDA_D_NM = [0.8, 3.0, 9.6]
DISTANCES_NM = [0.5, 1.0, 2.0, 5.0, 10.0]


def ensure_dirs() -> None:
    for directory in (PROCESSED, PLOTS, REPORT_FIGURES, POSTER_FIGURES):
        directory.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def get_m2b_flow_tau_s(ratio: float, velocity_m_s: float) -> float:
    if velocity_m_s <= 0:
        return 700.0 + 3500.0 / ratio
    velocity_scale = (velocity_m_s / 5e-7) ** 0.55
    return 1600.0 / velocity_scale + 900.0 / (ratio + 0.5)


def get_m2b_flow_medulla_pm(
    time_s: float,
    ratio: float,
    velocity_m_s: float,
    concentration_pm: float,
) -> float:
    if velocity_m_s <= 0:
        tau_medulla = 700.0 + 3500.0 / ratio
        return concentration_pm * (1.0 - math.exp(-time_s / tau_medulla))
    tau = get_m2b_flow_tau_s(ratio, velocity_m_s)
    return concentration_pm * (1.0 - math.exp(-time_s / tau))


def get_m2b_flow_sensor_pm(
    time_s: float,
    ratio: float,
    velocity_m_s: float,
    concentration_pm: float,
) -> float:
    medulla_pm = get_m2b_flow_medulla_pm(time_s, ratio, velocity_m_s, concentration_pm)
    gain = 0.92 if velocity_m_s <= 0 else 0.96
    return min(concentration_pm, gain * medulla_pm)


def n_bound_from_surface(sensor_surface_pm: float, kd_pm: float) -> float:
    sensor_surface_mol_m3 = sensor_surface_pm * 1e-9
    kd_mol_m3 = kd_pm * 1e-9
    if sensor_surface_mol_m3 <= 0:
        return 0.0
    theta = sensor_surface_mol_m3 / (kd_mol_m3 + sensor_surface_mol_m3)
    gamma_mol_m2 = BMAX_MOL_M2 * theta
    return gamma_mol_m2 * LOCAL_AREA_M2 * AVOGADRO


def current_per_alpha_eff_a(n_bound: float) -> float:
    return W_OVER_L * E_CHARGE * MU * VDS * n_bound / AEFF_M2


def delta_ids_screened_a(n_bound: float, alpha0: float, distance_nm: float, lambda_nm: float) -> tuple[float, float]:
    alpha_eff = alpha0 * math.exp(-distance_nm / lambda_nm)
    return alpha_eff, current_per_alpha_eff_a(n_bound) * alpha_eff


def required_alpha0_for_detection(n_bound: float, noise_floor_a: float, distance_nm: float, lambda_nm: float) -> float:
    base = current_per_alpha_eff_a(n_bound)
    attenuation = math.exp(-distance_nm / lambda_nm)
    if base <= 0 or attenuation <= 0:
        return math.inf
    return (3.0 * noise_floor_a) / (base * attenuation)


def maximum_allowed_distance_nm(n_bound: float, alpha0: float, noise_floor_a: float, lambda_nm: float) -> float:
    signal_at_zero_distance = current_per_alpha_eff_a(n_bound) * alpha0
    threshold_a = 3.0 * noise_floor_a
    if signal_at_zero_distance <= threshold_a:
        return 0.0
    return lambda_nm * math.log(signal_at_zero_distance / threshold_a)


def max_noise_floor_pa(delta_ids_a: float) -> float:
    return (delta_ids_a / 3.0) * 1e12


def fmt(value: float) -> str:
    if math.isinf(value):
        return "inf"
    if math.isnan(value):
        return "nan"
    return f"{value:.6g}"


def build_requirement_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for concentration_pm in CONCENTRATIONS_PM:
        sensor_surface_pm = get_m2b_flow_sensor_pm(
            REFERENCE_TIME_S,
            M2B_REFERENCE_RATIO,
            M2B_REFERENCE_VELOCITY_M_S,
            concentration_pm,
        )
        for kd_pm in KD_VALUES_PM:
            n_bound = n_bound_from_surface(sensor_surface_pm, kd_pm)
            for alpha0 in ALPHA0_VALUES:
                for noise_pa in NOISE_FLOORS_PA:
                    noise_a = noise_pa * 1e-12
                    threshold_pa = 3.0 * noise_pa
                    for lambda_nm in LAMBDA_D_NM:
                        max_distance = maximum_allowed_distance_nm(n_bound, alpha0, noise_a, lambda_nm)
                        for distance_nm in DISTANCES_NM:
                            alpha_eff, delta_a = delta_ids_screened_a(
                                n_bound,
                                alpha0,
                                distance_nm,
                                lambda_nm,
                            )
                            required_alpha = required_alpha0_for_detection(
                                n_bound,
                                noise_a,
                                distance_nm,
                                lambda_nm,
                            )
                            detectable = delta_a >= 3.0 * noise_a
                            rows.append({
                                "concentration_pM": concentration_pm,
                                "sensor_surface_c_avg_6000s_pM": sensor_surface_pm,
                                "Kd_pM": kd_pm,
                                "alpha0": alpha0,
                                "noise_floor_pA": noise_pa,
                                "lambda_D_nm": lambda_nm,
                                "effective_charge_distance_nm": distance_nm,
                                "N_bound": n_bound,
                                "alpha_eff": alpha_eff,
                                "DeltaIds_screened_A": delta_a,
                                "DeltaIds_screened_pA": delta_a * 1e12,
                                "detection_threshold_pA": threshold_pa,
                                "detectable": detectable,
                                "required_alpha0_for_detection": required_alpha,
                                "maximum_allowed_distance_nm": max_distance,
                                "maximum_allowed_noise_floor_pA": max_noise_floor_pa(delta_a),
                            })
    return rows


def unique_requirement_rows(rows: Iterable[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    required_alpha: dict[tuple[float, float, float, float, float], dict[str, object]] = {}
    max_distance: dict[tuple[float, float, float, float, float], dict[str, object]] = {}
    noise_summary: dict[tuple[float, float, float, float, float], dict[str, object]] = {}

    for row in rows:
        alpha_key = (
            float(row["concentration_pM"]),
            float(row["Kd_pM"]),
            float(row["noise_floor_pA"]),
            float(row["lambda_D_nm"]),
            float(row["effective_charge_distance_nm"]),
        )
        if alpha_key not in required_alpha:
            required_alpha[alpha_key] = {
                "concentration_pM": row["concentration_pM"],
                "Kd_pM": row["Kd_pM"],
                "noise_floor_pA": row["noise_floor_pA"],
                "lambda_D_nm": row["lambda_D_nm"],
                "effective_charge_distance_nm": row["effective_charge_distance_nm"],
                "N_bound": row["N_bound"],
                "required_alpha0_for_detection": row["required_alpha0_for_detection"],
            }

        distance_key = (
            float(row["concentration_pM"]),
            float(row["Kd_pM"]),
            float(row["alpha0"]),
            float(row["noise_floor_pA"]),
            float(row["lambda_D_nm"]),
        )
        if distance_key not in max_distance:
            max_distance[distance_key] = {
                "concentration_pM": row["concentration_pM"],
                "Kd_pM": row["Kd_pM"],
                "alpha0": row["alpha0"],
                "noise_floor_pA": row["noise_floor_pA"],
                "lambda_D_nm": row["lambda_D_nm"],
                "maximum_allowed_distance_nm": row["maximum_allowed_distance_nm"],
            }

        noise_key = (
            float(row["concentration_pM"]),
            float(row["Kd_pM"]),
            float(row["alpha0"]),
            float(row["lambda_D_nm"]),
            float(row["effective_charge_distance_nm"]),
        )
        if noise_key not in noise_summary:
            noise_summary[noise_key] = {
                "concentration_pM": row["concentration_pM"],
                "Kd_pM": row["Kd_pM"],
                "alpha0": row["alpha0"],
                "lambda_D_nm": row["lambda_D_nm"],
                "effective_charge_distance_nm": row["effective_charge_distance_nm"],
                "maximum_allowed_noise_floor_pA": row["maximum_allowed_noise_floor_pA"],
            }

    return (
        list(required_alpha.values()),
        list(max_distance.values()),
        list(noise_summary.values()),
    )


def row_filter(rows: list[dict[str, object]], **criteria: float) -> list[dict[str, object]]:
    out = []
    for row in rows:
        ok = True
        for key, expected in criteria.items():
            if not math.isclose(float(row[key]), expected, rel_tol=0.0, abs_tol=1e-12):
                ok = False
                break
        if ok:
            out.append(row)
    return out


def nearest_value(rows: list[dict[str, object]], field: str, **criteria: float) -> float:
    matches = row_filter(rows, **criteria)
    if not matches:
        return math.nan
    return float(matches[0][field])


def build_design_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    pbs_rows = [row for row in rows if math.isclose(float(row["lambda_D_nm"]), 0.8)]
    pbs_detectable_distances = sorted({
        float(row["effective_charge_distance_nm"])
        for row in pbs_rows
        if row["detectable"] is True
    })
    pbs_distance_text = (
        f"{min(pbs_detectable_distances):.1f}-{max(pbs_detectable_distances):.1f} nm in the full sweep"
        if pbs_detectable_distances else
        "none in the tested sweep"
    )

    req_alpha_1_pbs_1nm = nearest_value(
        rows,
        "required_alpha0_for_detection",
        concentration_pM=1.0,
        Kd_pM=10.0,
        noise_floor_pA=10.0,
        lambda_D_nm=0.8,
        effective_charge_distance_nm=1.0,
        alpha0=0.01,
    )
    req_alpha_10_pbs_1nm = nearest_value(
        rows,
        "required_alpha0_for_detection",
        concentration_pM=10.0,
        Kd_pM=10.0,
        noise_floor_pA=10.0,
        lambda_D_nm=0.8,
        effective_charge_distance_nm=1.0,
        alpha0=0.01,
    )
    req_alpha_1_pbs_2nm = nearest_value(
        rows,
        "required_alpha0_for_detection",
        concentration_pM=1.0,
        Kd_pM=10.0,
        noise_floor_pA=10.0,
        lambda_D_nm=0.8,
        effective_charge_distance_nm=2.0,
        alpha0=0.01,
    )
    req_alpha_10_pbs_2nm = nearest_value(
        rows,
        "required_alpha0_for_detection",
        concentration_pM=10.0,
        Kd_pM=10.0,
        noise_floor_pA=10.0,
        lambda_D_nm=0.8,
        effective_charge_distance_nm=2.0,
        alpha0=0.01,
    )

    favorable_noise = nearest_value(
        rows,
        "maximum_allowed_noise_floor_pA",
        concentration_pM=10.0,
        Kd_pM=10.0,
        alpha0=0.03,
        lambda_D_nm=9.6,
        effective_charge_distance_nm=0.5,
        noise_floor_pA=1.0,
    )
    unfavorable_noise = nearest_value(
        rows,
        "maximum_allowed_noise_floor_pA",
        concentration_pM=10.0,
        Kd_pM=10.0,
        alpha0=0.03,
        lambda_D_nm=0.8,
        effective_charge_distance_nm=5.0,
        noise_floor_pA=1.0,
    )

    return [
        {
            "question": "Under PBS-like screening, what receptor distance range remains detectable?",
            "answer": (
                f"PBS-like lambda_D = 0.8 nm remains detectable only over {pbs_distance_text}, "
                "and those cases require favorable concentration, affinity, coupling, and low noise. "
                "For baseline 10 pM HER2, Kd = 10 pM, alpha0 = 0.03, and 10 pA noise, PBS-like detection is not robust beyond about 1 nm."
            ),
            "supporting_metric": "detectable rows versus effective_charge_distance_nm at lambda_D = 0.8 nm",
        },
        {
            "question": "What coupling efficiency is required for detection at 1 pM and 10 pM HER2?",
            "answer": (
                "For Kd = 10 pM, 10 pA noise, and PBS-like screening at 1 nm, "
                f"required alpha0 is {req_alpha_1_pbs_1nm:.3g} at 1 pM and {req_alpha_10_pbs_1nm:.3g} at 10 pM. "
                f"At 2 nm, the required alpha0 increases to {req_alpha_1_pbs_2nm:.3g} at 1 pM and {req_alpha_10_pbs_2nm:.3g} at 10 pM."
            ),
            "supporting_metric": "required_alpha0_for_detection",
        },
        {
            "question": "What maximum noise floor is tolerable under favorable and unfavorable screening?",
            "answer": (
                "For 10 pM HER2, Kd = 10 pM, and alpha0 = 0.03, the favorable case "
                f"(lambda_D = 9.6 nm, d = 0.5 nm) tolerates about {favorable_noise:.2f} pA noise. "
                f"The unfavorable PBS-like case (lambda_D = 0.8 nm, d = 5 nm) tolerates only {unfavorable_noise:.4f} pA."
            ),
            "supporting_metric": "maximum_allowed_noise_floor_pA",
        },
        {
            "question": "Which factor is most restrictive: transport, affinity, coupling, noise, or screening?",
            "answer": (
                "Screening is the most restrictive factor because alpha_eff decays exponentially with distance. "
                "Noise and coupling are the next limiting factors because the detection threshold is 3 times the noise floor and DeltaIds scales linearly with alpha_eff. "
                "Transport and affinity still matter because they set N_bound, but Experiment E shows they cannot compensate for long receptor distance under PBS-like screening."
            ),
            "supporting_metric": "alpha_eff, required_alpha0_for_detection, maximum_allowed_noise_floor_pA",
        },
    ]


def save_plot(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=220)
    plt.close()
    for destination_dir in (REPORT_FIGURES, POSTER_FIGURES):
        target = destination_dir / path.name
        target.write_bytes(path.read_bytes())


def plot_detectability_requirement_map(rows: list[dict[str, object]]) -> None:
    distances = DISTANCES_NM
    lambdas = LAMBDA_D_NM
    matrix = np.zeros((len(lambdas), len(distances)))
    for i, lambda_nm in enumerate(lambdas):
        for j, distance_nm in enumerate(distances):
            matches = row_filter(rows, lambda_D_nm=lambda_nm, effective_charge_distance_nm=distance_nm)
            matrix[i, j] = sum(1 for row in matches if row["detectable"] is True) / len(matches)

    plt.figure(figsize=(7.5, 4.8))
    image = plt.imshow(matrix, aspect="auto", origin="lower", cmap="viridis", vmin=0, vmax=1)
    plt.colorbar(image, label="detectable fraction across sweep")
    plt.xticks(range(len(distances)), [str(value) for value in distances])
    plt.yticks(range(len(lambdas)), [str(value) for value in lambdas])
    plt.xlabel("effective receptor-channel distance d (nm)")
    plt.ylabel("Debye length lambda_D (nm)")
    plt.title("EXP E detectability requirement map")
    save_plot(PLOTS / "EXP_E_detectability_requirement_map.png")


def plot_required_alpha(rows: list[dict[str, object]]) -> None:
    plt.figure(figsize=(7.5, 4.8))
    for concentration_pm in (1.0, 10.0):
        for lambda_nm in LAMBDA_D_NM:
            y = [
                nearest_value(
                    rows,
                    "required_alpha0_for_detection",
                    concentration_pM=concentration_pm,
                    Kd_pM=10.0,
                    noise_floor_pA=10.0,
                    lambda_D_nm=lambda_nm,
                    effective_charge_distance_nm=distance_nm,
                    alpha0=0.01,
                )
                for distance_nm in DISTANCES_NM
            ]
            plt.plot(DISTANCES_NM, y, marker="o", label=f"C={concentration_pm:g} pM, lambda={lambda_nm:g} nm")
    plt.axhline(0.03, color="gray", linestyle="--", linewidth=1, label="alpha0=0.03")
    plt.axhline(0.1, color="black", linestyle=":", linewidth=1, label="alpha0=0.1")
    plt.yscale("log")
    plt.xlabel("effective receptor-channel distance d (nm)")
    plt.ylabel("required alpha0 for detection")
    plt.title("EXP E required coupling vs distance")
    plt.grid(True, which="both", alpha=0.25)
    plt.legend(fontsize=7)
    save_plot(PLOTS / "EXP_E_required_alpha_vs_distance.png")


def plot_max_distance(rows: list[dict[str, object]]) -> None:
    plt.figure(figsize=(7.5, 4.8))
    for concentration_pm in (1.0, 10.0, 100.0):
        y = [
            nearest_value(
                rows,
                "maximum_allowed_distance_nm",
                concentration_pM=concentration_pm,
                Kd_pM=10.0,
                alpha0=0.03,
                noise_floor_pA=10.0,
                lambda_D_nm=lambda_nm,
                effective_charge_distance_nm=0.5,
            )
            for lambda_nm in LAMBDA_D_NM
        ]
        plt.plot(LAMBDA_D_NM, y, marker="o", label=f"C={concentration_pm:g} pM")
    plt.xlabel("Debye length lambda_D (nm)")
    plt.ylabel("maximum allowed distance (nm)")
    plt.title("EXP E max receptor distance vs screening")
    plt.grid(True, alpha=0.25)
    plt.legend()
    save_plot(PLOTS / "EXP_E_max_allowed_distance_vs_ionic_strength.png")


def plot_noise_requirement(rows: list[dict[str, object]]) -> None:
    plt.figure(figsize=(7.5, 4.8))
    for lambda_nm in (0.8, 9.6):
        y = [
            nearest_value(
                rows,
                "maximum_allowed_noise_floor_pA",
                concentration_pM=10.0,
                Kd_pM=10.0,
                alpha0=0.03,
                lambda_D_nm=lambda_nm,
                effective_charge_distance_nm=distance_nm,
                noise_floor_pA=1.0,
            )
            for distance_nm in DISTANCES_NM
        ]
        plt.plot(DISTANCES_NM, y, marker="o", label=f"lambda_D={lambda_nm:g} nm")
    plt.axhline(10.0, color="gray", linestyle="--", linewidth=1, label="10 pA")
    plt.yscale("log")
    plt.xlabel("effective receptor-channel distance d (nm)")
    plt.ylabel("maximum allowed noise floor (pA)")
    plt.title("EXP E electronics noise requirement")
    plt.grid(True, which="both", alpha=0.25)
    plt.legend()
    save_plot(PLOTS / "EXP_E_noise_floor_requirement.png")


def main() -> None:
    ensure_dirs()
    rows = build_requirement_rows()
    required_alpha_rows, max_distance_rows, noise_rows = unique_requirement_rows(rows)
    design_summary_rows = build_design_summary(rows)

    write_csv(PROCESSED / "EXP_E_feasibility_requirement_map.csv", rows)
    write_csv(PROCESSED / "EXP_E_required_alpha_summary.csv", required_alpha_rows)
    write_csv(PROCESSED / "EXP_E_max_distance_summary.csv", max_distance_rows)
    write_csv(PROCESSED / "EXP_E_noise_requirement_summary.csv", noise_rows)
    write_csv(PROCESSED / "EXP_E_design_requirements_summary.csv", design_summary_rows)

    plot_detectability_requirement_map(rows)
    plot_required_alpha(rows)
    plot_max_distance(rows)
    plot_noise_requirement(rows)


if __name__ == "__main__":
    main()
