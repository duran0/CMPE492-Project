# Simulation Log

## Run ID: M1_0D_HER2_binding_v01

- Date: 2026-06-03
- Model file: `comsol/models/M1_0D_binding/M1_0D_HER2_binding_v01.mph`
- Physics: 0D reversible HER2-antibody binding.
- Parameters: `C = 0.5, 1, 10, 100, 1000 pM`, `Kd = 10 pM`, `kf = 1e7 1/(M*s)`, `kr = 1e-4 1/s`.
- Solver: analytical binding calculation from documented equations.
- Status: completed.
- Exported CSV: `results/raw_csv/M1_binding_timecourse.csv`, `results/raw_csv/M1_equilibrium_occupancy_vs_C.csv`.
- Exported figures: `results/plots/M1_binding_timecourse.png`, `results/plots/M1_occupancy_vs_concentration.png`.
- Notes: occupancy remains bounded between 0 and 1 and increases with HER2 concentration.

## Run ID: M2_3D_diffusion_lymphnode_v01_single

- Date: 2026-06-03
- COMSOL file: `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01_solved.mph`
- Solver log: `comsol/models/M2_3D_transport/solver_logs/M2_3D_diffusion_lymphnode_v01_solve.txt`
- Physics: Transport of Diluted Species.
- Geometry version: two-sphere cortex/medulla-inspired 3D geometry.
- Mesh: COMSOL automatic mesh size 4.
- Parameters:
  - `C = 10 pM`
  - `Dcortex = 8e-11 m^2/s`
  - `Dmedulla = r * Dcortex`
  - `r = 0.5`
  - `tmax = 6000 s`
- Solver:
  - Type: time dependent BDF.
  - Time points: `0, 100, 500, 1000, 2000, 4000, 6000 s`.
  - Degrees of freedom: 3103 plus internal DOFs.
- Status: completed.
- Exported CSV: `results/raw_csv/M2_comsol_avg_concentration_cortex.csv`, `results/raw_csv/M2_comsol_avg_concentration_medulla.csv`, `results/raw_csv/M2_comsol_sensor_surface_concentration.csv`.
- Exported figures: `results/plots/M2_comsol_cortex_vs_medulla_uptake.png`, `results/plots/M2_comsol_concentration_slice_t1000s.png`, `results/plots/M2_comsol_concentration_slice_t6000s.png`.
- Notes: direct field-table export from the solved `.mph` remains a limitation; current CSV files are COMSOL-stage post-processing outputs tied to the meshed TDS setup and solver logs.

## Run ID: M2_3D_diffusion_lymphnode_v01_r_sweep

- Date: 2026-06-03
- COMSOL file: `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01_sweep_r_*.mph`
- Solver log: `comsol/models/M2_3D_transport/solver_logs/M2_3D_diffusion_lymphnode_v01_sweep.txt`
- Physics: Transport of Diluted Species.
- Mesh: COMSOL automatic mesh size 4.
- Parameters:
  - `r = 0.1, 0.25, 0.5, 0.75, 1.0`
  - `tmax = 6000 s`
- Solver: time dependent BDF.
- Runtime: completed in batch for all five `r` values.
- Status: completed with documented post-processing limitation.
- Exported CSV: `results/processed_csv/M2_comsol_delay_vs_diffusivity_ratio.csv`.
- Exported figures: `results/plots/M2_comsol_delay_vs_diffusivity_ratio.png`.
- Notes: the sweep trend shows medulla uptake delay decreasing as `r` approaches 1.

## Run ID: M2_mesh_sensitivity_v01

- Date: 2026-06-03
- Mesh cases: coarse, normal, fine.
- Metrics: cortex average, medulla average, sensor surface concentration, sensor flux metric at `t = 1000 s` and `t = 6000 s`.
- Status: completed as post-processing sensitivity comparison.
- Exported CSV: `results/processed_csv/M2_mesh_sensitivity.csv`.
- Exported figures: `results/plots/M2_mesh_sensitivity.png`.
- Notes: normal-to-fine variation remains below 5% for the reported concentration metrics.

## Run ID: M3_surface_binding_from_M2_v01

- Date: 2026-06-03
- Input CSV: `results/raw_csv/M2_comsol_sensor_surface_concentration.csv`
- Physics: Langmuir surface binding.
- Parameters: `Gamma_max = 8.30e-12 mol/m^2`, `Kd = 10 pM`, `Aeff = 4e-11 m^2`, full-boundary area `8e-10 m^2`.
- Status: completed.
- Exported CSV: `results/raw_csv/M3_bound_molecule_count.csv`, `results/raw_csv/M3_surface_occupancy.csv`, `results/raw_csv/M3_gamma_full_boundary.csv`, `results/raw_csv/M3_gamma_local_sensor.csv`.
- Exported figures: `results/plots/M3_bound_count_vs_time.png`, `results/plots/M3_full_vs_local_sensor_response.png`, `results/plots/M3_surface_occupancy_vs_time.png`.
- Notes: occupancy remains bounded and full-boundary total bound count exceeds local-sensor total bound count under comparable concentration.

## Run ID: M4_gfet_current_response_v01

- Date: 2026-06-03
- Input CSV: `results/raw_csv/M3_bound_molecule_count.csv`
- Physics: analytical GFET current response.
- Parameters: `W = 20 um`, `L = 2 um`, `mu = 0.1 m^2/(V*s)`, `Vds = 50 mV`, `Aeff = 4e-11 m^2`, `alpha = 0.01, 0.03`, noise floor `10, 50 pA`.
- Status: completed.
- Exported CSV: `results/processed_csv/M4_deltaIds_vs_time.csv`, `results/processed_csv/M4_deltaIds_vs_concentration.csv`, `results/processed_csv/M4_noise_floor_thresholds.csv`, `results/processed_csv/M4_lod_summary.csv`.
- Exported figures: `results/plots/M4_deltaIds_vs_time.png`, `results/plots/M4_deltaIds_vs_concentration.png`, `results/plots/M4_lod_thresholds.png`, `results/plots/M4_detection_threshold_overlay.png`.
- Notes: the `alpha = 0.03`, `10 pA` case reaches simulated LOD below 1 pM; this does not hold for every noise/coupling case.
