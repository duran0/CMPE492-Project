# Simulation Log

## Run ID: M1_0D_HER2_binding_v01

- Date: 2026-06-03
- Model file: `comsol/models/M1_0D_binding/M1_0D_HER2_binding_v01.mph`
- Physics: 0D reversible HER2-antibody binding, analytical Langmuir equilibrium and first-order approach to equilibrium.
- Parameters: `C = 0.5, 1, 10, 100, 1000 pM`, `Kd = 10 pM`, `kf = 1e7 1/(M*s)`, `kr = 1e-4 1/s`.
- Solver: analytical calculation from documented equations.
- Status: completed.
- Exported CSV: `results/raw_csv/M1_binding_timecourse.csv`, `results/raw_csv/M1_equilibrium_occupancy_vs_C.csv`.
- Exported figures: `results/plots/M1_binding_timecourse.png`, `results/plots/M1_occupancy_vs_concentration.png`.
- Notes: COMSOL `.mph` stores stage parameters and provenance; reproducible numeric outputs come from script-generated CSV.

## Run ID: M2_reduced_order_transport_v01

- Date: 2026-06-03
- Model file: `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01.mph`
- Physics: diffusion-only cortex/medulla uptake trend model.
- Geometry version: two-sphere lymph-node-inspired scaffold in COMSOL.
- Parameters: `Dcortex = 8e-11 m^2/s`, `r = 0.1, 0.25, 0.5, 0.75, 1.0`, `c0 = 10 pM`, `tmax = 6000 s`.
- Solver: reduced-order exponential uptake baseline used to validate trend direction before final 3D PDE solve.
- Status: scaffold and trend outputs completed; full 3D Transport of Diluted Species solve remains pending.
- Exported CSV: `results/raw_csv/M2_avg_concentration_cortex.csv`, `results/raw_csv/M2_avg_concentration_medulla.csv`, `results/processed_csv/M2_delay_vs_diffusivity_ratio.csv`.
- Exported figures: `results/plots/M2_cortex_vs_medulla_uptake.png`, `results/plots/M2_delay_vs_diffusivity_ratio.png`.
- Notes: smaller `r` increases medulla uptake delay, matching expected transport-limited behavior.

## Run ID: M3_surface_binding_v01

- Date: 2026-06-03
- Model files: `comsol/models/M3_surface_binding/M3_surface_binding_full_boundary_v01.mph`, `comsol/models/M3_surface_binding/M3_surface_binding_local_sensor_v01.mph`.
- Physics: Langmuir-type surface binding from local HER2 exposure.
- Parameters: `Gamma_max = 8.30e-12 mol/m^2`, `Kd = 10 pM`, local area `Aeff = 4e-11 m^2`, full-boundary area `8e-10 m^2`.
- Solver: analytical surface occupancy and bound molecule count.
- Status: completed as analytical coupling; dynamic COMSOL surface reaction remains optional.
- Exported CSV: `results/raw_csv/M3_bound_molecule_count.csv`, `results/raw_csv/M3_surface_occupancy.csv`, `results/raw_csv/M3_gamma_full_boundary.csv`, `results/raw_csv/M3_gamma_local_sensor.csv`.
- Exported figures: `results/plots/M3_bound_count_vs_time.png`, `results/plots/M3_full_vs_local_sensor_response.png`.
- Notes: full-boundary response produces larger total bound count than local sensor response because the effective exposed area is larger.

## Run ID: M4_gfet_current_response_v01

- Date: 2026-06-03
- Model file: `comsol/models/M4_gfet_response/M4_gfet_current_response_v01.mph`
- Physics: analytical GFET transduction from bound HER2 count to drain-source current shift.
- Parameters: `W = 20 um`, `L = 2 um`, `mu = 0.1 m^2/(V*s)`, `Vds = 50 mV`, `Aeff = 4e-11 m^2`, `alpha = 0.01, 0.03`, noise floor `10, 50 pA`.
- Solver: analytical calculation from `DeltaIds = (W/L) * e * mu * Vds * alpha * N / Aeff`.
- Status: completed.
- Exported CSV: `results/processed_csv/M4_deltaIds_vs_time.csv`, `results/processed_csv/M4_deltaIds_vs_concentration.csv`, `results/processed_csv/M4_noise_floor_thresholds.csv`, `results/processed_csv/M4_lod_summary.csv`.
- Exported figures: `results/plots/M4_deltaIds_vs_time.png`, `results/plots/M4_deltaIds_vs_concentration.png`, `results/plots/M4_lod_thresholds.png`.
- Notes: calculated `Nmin` is approximately 5 molecules for 10 pA and `alpha = 0.01`, and approximately 25 molecules for 50 pA and `alpha = 0.01`. The `alpha = 0.03`, 10 pA case reaches a simulated LOD below 1 pM under the current assumptions.
