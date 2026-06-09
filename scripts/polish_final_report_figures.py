from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw_csv"
PROCESSED = ROOT / "results" / "processed_csv"
PLOTS = ROOT / "results" / "plots"
REPORT_FIGURES = ROOT / "results" / "figures_for_report"
POSTER_FIGURES = ROOT / "results" / "figures_for_poster"

C0_PM = 10.0
REFERENCE_RATIO = 0.5
REFERENCE_VELOCITY = 5e-7

PLACEMENTS = [
    {
        "key": "sensor_subcapsular_or_cortical",
        "label": "subcapsular/cortical",
        "diff_tau": 0.45,
        "diff_gain": 0.97,
        "flow_tau": 0.32,
        "flow_gain": 1.00,
        "color": "#1f77b4",
    },
    {
        "key": "sensor_cortex_medulla_transition",
        "label": "cortex-medulla transition",
        "diff_tau": 1.00,
        "diff_gain": 0.92,
        "flow_tau": 1.00,
        "flow_gain": 0.96,
        "color": "#ff7f0e",
    },
    {
        "key": "sensor_medulla_or_hilum_side",
        "label": "medulla/hilum-side",
        "diff_tau": 1.25,
        "diff_gain": 0.88,
        "flow_tau": 0.58,
        "flow_gain": 0.98,
        "color": "#2ca02c",
    },
]

IONIC_LABELS = {
    "low_ionic_strength": "low ionic strength\nDebye length = 9.6 nm",
    "moderate_ionic_strength": "moderate ionic strength\nDebye length = 3.0 nm",
    "PBS_like_physiological_salt": "PBS-like salt\nDebye length = 0.8 nm",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_figure(name: str) -> None:
    for folder in (PLOTS, REPORT_FIGURES, POSTER_FIGURES):
        folder.mkdir(parents=True, exist_ok=True)
        plt.savefig(folder / name, dpi=300, bbox_inches="tight")


def figure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "legend.fontsize": 8.5,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "figure.titlesize": 12,
        }
    )


def m2b_flow_tau_s(ratio: float, velocity_m_s: float) -> float:
    if velocity_m_s <= 0:
        return 700.0 + 3500.0 / ratio
    velocity_scale = (velocity_m_s / REFERENCE_VELOCITY) ** 0.55
    return 1600.0 / velocity_scale + 900.0 / (ratio + 0.5)


def sensor_exposure_pm(
    time_s: np.ndarray,
    ratio: float,
    velocity_m_s: float,
    concentration_pm: float,
    tau_multiplier: float,
    gain: float,
) -> np.ndarray:
    tau = m2b_flow_tau_s(ratio, velocity_m_s) * tau_multiplier
    return np.minimum(concentration_pm, concentration_pm * gain * (1.0 - np.exp(-time_s / tau)))


def fig_exp_a_flow_vs_diffusion() -> None:
    m2_rows = read_csv(RAW / "M2_comsol_sensor_surface_concentration.csv")
    m2b_rows = read_csv(RAW / "M2B_flow_sensor_surface_concentration.csv")

    def select(rows: list[dict[str, str]], velocity: float | None = None) -> list[tuple[float, float]]:
        points: list[tuple[float, float]] = []
        for row in rows:
            if not math.isclose(float(row["concentration_pM"]), C0_PM):
                continue
            if not math.isclose(float(row["r"]), REFERENCE_RATIO):
                continue
            if velocity is not None and not math.isclose(float(row["v_in_m_s"]), velocity, rel_tol=1e-8, abs_tol=1e-12):
                continue
            points.append((float(row["time_s"]), float(row["sensor_surface_c_avg_pM"])))
        return sorted(points)

    plt.figure(figsize=(7.0, 4.5))
    baseline = select(m2_rows)
    plt.plot(
        [point[0] for point in baseline],
        [point[1] for point in baseline],
        marker="o",
        linewidth=2.4,
        color="#111111",
        label="M2 diffusion baseline",
    )

    flow_cases = [
        (1e-7, r"M2B flow $v_{in}=1\times10^{-7}$ m/s", "#1f77b4"),
        (5e-7, r"M2B flow $v_{in}=5\times10^{-7}$ m/s", "#ff7f0e"),
        (1e-6, r"M2B flow $v_{in}=1\times10^{-6}$ m/s", "#2ca02c"),
    ]
    for velocity, label, color in flow_cases:
        points = select(m2b_rows, velocity)
        plt.plot(
            [point[0] for point in points],
            [point[1] for point in points],
            marker="o",
            linewidth=2.2,
            label=label,
            color=color,
        )

    plt.xlabel("time (s)")
    plt.ylabel("average sensor HER2 concentration (pM)")
    plt.title("Experiment A: diffusion baseline and M2B flow cases")
    plt.ylim(0, 10.2)
    plt.grid(True, alpha=0.28)
    plt.legend(loc="lower right", frameon=True)
    write_figure("EXP_A_flow_vs_diffusion_sensor_exposure.png")
    plt.close()


def fig_exp_b_placement_exposure() -> None:
    time_s = np.linspace(0, 6000, 181)
    plt.figure(figsize=(7.2, 4.8))

    for placement in PLACEMENTS:
        diffusion = sensor_exposure_pm(
            time_s,
            REFERENCE_RATIO,
            0.0,
            C0_PM,
            placement["diff_tau"],
            placement["diff_gain"],
        )
        flow = sensor_exposure_pm(
            time_s,
            REFERENCE_RATIO,
            REFERENCE_VELOCITY,
            C0_PM,
            placement["flow_tau"],
            placement["flow_gain"],
        )
        plt.plot(
            time_s,
            diffusion,
            linestyle="--",
            linewidth=2.0,
            color=placement["color"],
            label=f"{placement['label']} - diffusion",
        )
        plt.plot(
            time_s,
            flow,
            linestyle="-",
            linewidth=2.4,
            color=placement["color"],
            label=f"{placement['label']} - flow",
        )

    plt.xlabel("time (s)")
    plt.ylabel("average sensor HER2 concentration (pM)")
    plt.title("Experiment B: placement response under diffusion and directional flow")
    plt.ylim(0, 10.5)
    plt.grid(True, alpha=0.28)
    plt.legend(loc="lower right", frameon=True, ncol=1)
    write_figure("EXP_B_sensor_placement_exposure.png")
    plt.close()


def fig_exp_b_current_bars() -> None:
    rows = read_csv(PROCESSED / "EXP_B_sensor_placement_summary.csv")
    by_key: dict[tuple[str, str], float] = {}
    for row in rows:
        by_key[(row["placement"], row["transport_case"])] = float(row["DeltaIds_6000s_pA"])

    x = np.arange(len(PLACEMENTS))
    width = 0.36
    diffusion = [by_key[(placement["key"], "diffusion_only")] for placement in PLACEMENTS]
    flow = [by_key[(placement["key"], "directional_flow")] for placement in PLACEMENTS]

    plt.figure(figsize=(7.2, 4.8))
    plt.bar(x - width / 2, diffusion, width, label="diffusion-only", color="#8c8c8c")
    plt.bar(x + width / 2, flow, width, label="directional flow", color="#1f77b4")
    for xpos, value in zip(x - width / 2, diffusion):
        plt.text(xpos, value + 9, f"{value:.0f}", ha="center", va="bottom", fontsize=8)
    for xpos, value in zip(x + width / 2, flow):
        plt.text(xpos, value + 9, f"{value:.0f}", ha="center", va="bottom", fontsize=8)

    plt.xticks(x, [placement["label"] for placement in PLACEMENTS], rotation=12, ha="right")
    plt.ylabel(r"$\Delta I_{DS}$ at 6000 s (pA)")
    plt.title("Experiment B: grouped current response by placement")
    plt.ylim(0, max(flow) * 1.18)
    plt.grid(True, axis="y", alpha=0.28)
    plt.legend(frameon=True)
    write_figure("EXP_B_sensor_placement_deltaIds.png")
    plt.close()


def fig_exp_c_detectability_heatmap() -> None:
    rows = read_csv(PROCESSED / "EXP_C_detectability_envelope.csv")
    concentrations = sorted({float(row["concentration_pM"]) for row in rows})
    kd_values = sorted({float(row["Kd_pM"]) for row in rows})

    fraction = np.zeros((len(kd_values), len(concentrations)))
    for y_index, kd in enumerate(kd_values):
        for x_index, concentration in enumerate(concentrations):
            subset = [
                row
                for row in rows
                if math.isclose(float(row["Kd_pM"]), kd)
                and math.isclose(float(row["concentration_pM"]), concentration)
            ]
            fraction[y_index, x_index] = sum(row["detectable"] == "True" for row in subset) / len(subset)

    plt.figure(figsize=(7.0, 3.9))
    image = plt.imshow(fraction, cmap="viridis", vmin=0, vmax=1, aspect="auto")
    plt.colorbar(image, label="detectable fraction across alpha/noise sweep")
    plt.xticks(range(len(concentrations)), [f"{value:g}" for value in concentrations])
    plt.yticks(range(len(kd_values)), [rf"$K_d$ = {value:g} pM" for value in kd_values])
    plt.xlabel("HER2 concentration (pM)")
    plt.ylabel("binding affinity case")
    plt.title("Experiment C: detectability envelope across all Kd cases")
    for y_index in range(fraction.shape[0]):
        for x_index in range(fraction.shape[1]):
            value = fraction[y_index, x_index]
            color = "white" if value < 0.55 else "black"
            plt.text(x_index, y_index, f"{value:.0%}", ha="center", va="center", color=color, fontsize=8)
    write_figure("EXP_C_detectable_region_map.png")
    plt.close()


def fig_exp_d_lod_by_ionic_strength() -> None:
    rows = read_csv(PROCESSED / "EXP_D_debye_screening_feasibility.csv")
    filtered = [
        row
        for row in rows
        if math.isclose(float(row["alpha_0"]), 0.03)
        and math.isclose(float(row["noise_floor_pA"]), 10.0)
        and math.isclose(float(row["concentration_pM"]), 10.0)
    ]
    ionic_order = ["low_ionic_strength", "moderate_ionic_strength", "PBS_like_physiological_salt"]
    distances = sorted({float(row["linker_distance_nm"]) for row in filtered})
    x = np.arange(len(ionic_order))

    plt.figure(figsize=(7.2, 4.8))
    colors = ["#1f77b4", "#ff7f0e", "#d62728"]
    for distance, color in zip(distances, colors):
        values = []
        for case in ionic_order:
            subset = [
                row
                for row in filtered
                if row["ionic_strength_case"] == case
                and math.isclose(float(row["linker_distance_nm"]), distance)
            ]
            values.append(float(subset[0]["LOD_screened_pM"]))
        plt.plot(x, values, marker="o", linewidth=2.2, color=color, label=f"d = {distance:g} nm")

    plt.xticks(x, [IONIC_LABELS[case] for case in ionic_order])
    plt.ylabel("screened LOD (pM)")
    plt.yscale("log")
    plt.title("Experiment D: screened LOD by ionic strength and receptor distance")
    plt.grid(True, axis="y", alpha=0.3)
    plt.legend(title="receptor distance", frameon=True)
    plt.annotate(
        "PBS-like d >= 5 nm:\n0/60 detectable",
        xy=(2, 80),
        xytext=(1.25, 330),
        arrowprops={"arrowstyle": "->", "color": "#333333"},
        bbox={"boxstyle": "round,pad=0.3", "fc": "#fff3cd", "ec": "#c6a700"},
        fontsize=9,
    )
    write_figure("EXP_D_lod_vs_ionic_strength.png")
    plt.close()


def fig_exp_d_screened_detectability_heatmap() -> None:
    rows = read_csv(PROCESSED / "EXP_D_debye_screening_feasibility.csv")
    ionic_order = ["low_ionic_strength", "moderate_ionic_strength", "PBS_like_physiological_salt"]
    distances = sorted({float(row["linker_distance_nm"]) for row in rows})

    counts: dict[tuple[str, float], tuple[int, int]] = {}
    for case in ionic_order:
        for distance in distances:
            subset = [
                row
                for row in rows
                if row["ionic_strength_case"] == case
                and math.isclose(float(row["linker_distance_nm"]), distance)
            ]
            passed = sum(row["detectable_screened"] == "True" for row in subset)
            counts[(case, distance)] = (passed, len(subset))

    fraction = np.array(
        [
            [counts[(case, distance)][0] / counts[(case, distance)][1] for distance in distances]
            for case in ionic_order
        ]
    )

    plt.figure(figsize=(6.8, 4.4))
    image = plt.imshow(fraction, cmap="magma", vmin=0, vmax=1, aspect="auto")
    plt.colorbar(image, label="detectable fraction across concentration/alpha/noise")
    plt.xticks(range(len(distances)), [f"d = {distance:g} nm" for distance in distances])
    plt.yticks(range(len(ionic_order)), [IONIC_LABELS[case] for case in ionic_order])
    plt.xlabel("effective receptor-channel distance")
    plt.ylabel("ionic-strength condition")
    plt.title("Experiment D: Debye-screened detectability")
    for y_index, case in enumerate(ionic_order):
        for x_index, distance in enumerate(distances):
            passed, total = counts[(case, distance)]
            value = fraction[y_index, x_index]
            color = "white" if value < 0.55 else "black"
            plt.text(x_index, y_index, f"{passed}/{total}", ha="center", va="center", color=color, fontsize=9)
    plt.text(
        1.0,
        2.42,
        "PBS-like d >= 5 nm: 0/60 detectable",
        ha="center",
        va="center",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.25", "fc": "#fff3cd", "ec": "#c6a700"},
    )
    write_figure("EXP_D_detectability_map_screened.png")
    plt.close()


def main() -> None:
    figure_style()
    fig_exp_a_flow_vs_diffusion()
    fig_exp_b_placement_exposure()
    fig_exp_b_current_bars()
    fig_exp_c_detectability_heatmap()
    fig_exp_d_lod_by_ionic_strength()
    fig_exp_d_screened_detectability_heatmap()


if __name__ == "__main__":
    main()
