# Simulation Log

## Run ID: M1_0D_HER2_binding_v01

- Date: 2026-03-15
- Model file: `comsol/models/M1_0D_binding/M1_0D_HER2_binding_v01.mph`
- Physics: 0D reversible HER2-antibody binding.
- Parameters: `C = 0.5, 1, 10, 100, 1000 pM`, `Kd = 10 pM`, `kf = 1e7 1/(M*s)`, `kr = 1e-4 1/s`.
- Solver: analytical binding calculation from documented equations.
- Status: completed.
- Exported CSV: `results/raw_csv/M1_binding_timecourse.csv`, `results/raw_csv/M1_equilibrium_occupancy_vs_C.csv`.
- Exported figures: `results/plots/M1_binding_timecourse.png`, `results/plots/M1_occupancy_vs_concentration.png`.
- Notes: occupancy remains bounded between 0 and 1 and increases with HER2 concentration.

## Run ID: M2_3D_diffusion_lymphnode_v01_single

- Date: 2026-03-30
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

- Date: 2026-04-13
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

- Date: 2026-04-25
- Mesh cases: coarse, normal, fine.
- Metrics: cortex average, medulla average, sensor surface concentration, sensor flux metric at `t = 1000 s` and `t = 6000 s`.
- Status: completed as post-processing sensitivity comparison.
- Exported CSV: `results/processed_csv/M2_mesh_sensitivity.csv`.
- Exported figures: `results/plots/M2_mesh_sensitivity.png`.
- Notes: normal-to-fine variation remains below 5% for the reported concentration metrics.

## Run ID: M2B_anatomical_flow_lymphnode_v01

- Date: 2026-06-03
- COMSOL file: `comsol/models/M2_3D_transport/M2B_anatomical_flow_lymphnode_v01.mph`
- Solver log: `comsol/models/M2_3D_transport/solver_logs/M2B_anatomical_flow_lymphnode_v01_solve.txt`
- Physics: Transport of Diluted Species with coupled user-defined convection velocity `u_flow`, `v_flow`, and `w_flow`.
- Geometry version: partially anatomical lymph-node-inspired scaffold with subcapsular sinus, cortex, medulla, four afferent inlet markers, one efferent outlet marker, capsule no-flow marker, and local/full sensor markers.
- Parameters:
  - `v_in = 0, 1e-7, 5e-7, 1e-6 m/s`
  - `r = 0.1, 0.25, 0.5, 0.75, 1.0`
  - `C = 0.5, 1, 10, 100, 1000 pM`
  - `t = 0, 100, 500, 1000, 2000, 4000, 6000 s`
- Solver:
  - Type: time dependent BDF with parametric velocity sweep.
  - Degrees of freedom: 7616 plus 48275 internal DOFs for each velocity case.
  - Completed cases: `v_in = 0, 1e-7, 5e-7, 1e-6 m/s`.
- Status: completed as a coupled convection-diffusion extension while preserving the M2 diffusion-only baseline.
- Exported CSV: `results/raw_csv/M2B_flow_velocity_summary.csv`, `results/raw_csv/M2B_flow_avg_concentration_cortex.csv`, `results/raw_csv/M2B_flow_avg_concentration_medulla.csv`, `results/raw_csv/M2B_flow_sensor_surface_concentration.csv`, `results/raw_csv/M2B_flow_flux_integral_sensor.csv`.
- Exported processed CSV: `results/processed_csv/M2B_flow_vs_diffusion_sensor_exposure.csv`, `results/processed_csv/M2B_flow_delay_vs_diffusivity_ratio.csv`, `results/processed_csv/M2B_flow_pressure_or_velocity_sweep.csv`, `results/processed_csv/M2B_flow_vs_M2_diffusion_comparison.csv`, `results/processed_csv/M2B_velocity_sweep_summary.csv`, `results/processed_csv/M2B_mesh_sensitivity.csv`.
- Exported figures: `results/plots/M2B_flow_velocity_streamlines.png`, `results/plots/M2B_flow_pressure_field.png`, `results/plots/M2B_flow_concentration_slice_t1000s.png`, `results/plots/M2B_flow_concentration_slice_t6000s.png`, `results/plots/M2B_flow_sensor_concentration_vs_time.png`, `results/plots/M2B_flow_vs_diffusion_sensor_exposure.png`, `results/plots/M2B_flow_delay_vs_diffusivity_ratio.png`, `results/plots/M2B_flow_vs_M2_diffusion_comparison.png`.
- Notes: the `v_in = 0` case matches the diffusion-like sensor concentration values, while increasing `v_in` increases sensor exposure. This is not a full anatomical, Darcy-flow, or clinically validated lymph-node simulation.

## Run ID: M3_surface_binding_from_M2_v01

- Date: 2026-05-10
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

## Run ID: final_scientific_experiment_campaign

- Date: 2026-06-04
- Input data: M2 diffusion baseline, verified M2B convection-diffusion outputs, M3 local-sensor binding assumptions, and M4 GFET current-response equation.
- Experiments:
  - Experiment A: flow versus diffusion at `C = 10 pM`.
  - Experiment B: sensor placement sweep under `v_in = 0` and `v_in = 5e-7 m/s`.
  - Experiment C: detectability envelope over concentration, `alpha_0`, current noise floor, and `Kd`.
  - Experiment D: Debye screening feasibility using low, moderate, and PBS-like Debye lengths.
- Status: completed as post-processing experiment campaign with explicit positive and negative conclusions.
- Exported CSV: `results/processed_csv/EXP_A_flow_vs_diffusion_summary.csv`, `results/processed_csv/EXP_B_sensor_placement_summary.csv`, `results/processed_csv/EXP_C_detectability_envelope.csv`, `results/processed_csv/EXP_D_debye_screening_feasibility.csv`, `results/processed_csv/final_scientific_conclusions.csv`.
- Exported figures: `results/plots/EXP_A_flow_vs_diffusion_sensor_exposure.png`, `results/plots/EXP_B_sensor_placement_exposure.png`, `results/plots/EXP_B_sensor_placement_deltaIds.png`, `results/plots/EXP_C_deltaIds_vs_concentration.png`, `results/plots/EXP_C_lod_heatmap_alpha_noise.png`, `results/plots/EXP_C_detectable_region_map.png`, `results/plots/EXP_D_alpha_eff_vs_distance.png`, `results/plots/EXP_D_lod_vs_ionic_strength.png`, `results/plots/EXP_D_detectability_map_screened.png`.
- Notes: flow and placement can improve antigen exposure, but detectability still fails under weak coupling, high noise, poor affinity, or PBS-like Debye screening at longer effective charge distances.

## Run ID: EXP_E_feasibility_requirement_map

- Date: 2026-06-09
- Script: `scripts/experiment_e_feasibility_requirements.py`
- Input model assumptions: M2B reference sensor exposure, M3 Langmuir local-sensor binding, M4 analytical GFET current response, and Debye attenuation `alpha_eff = alpha0 exp(-d/lambda_D)`.
- Parameters:
  - `C = 0.5, 1, 10, 100, 1000 pM`
  - `Kd = 1, 10, 100 pM`
  - `alpha0 = 0.01, 0.03, 0.1`
  - noise floor `= 1, 5, 10, 50, 100 pA`
  - `lambda_D = 0.8, 3.0, 9.6 nm`
  - effective charge distance `d = 0.5, 1, 2, 5, 10 nm`
- Exported CSV: `results/processed_csv/EXP_E_feasibility_requirement_map.csv`, `results/processed_csv/EXP_E_required_alpha_summary.csv`, `results/processed_csv/EXP_E_max_distance_summary.csv`, `results/processed_csv/EXP_E_noise_requirement_summary.csv`, `results/processed_csv/EXP_E_design_requirements_summary.csv`.
- Exported figures: `results/plots/EXP_E_detectability_requirement_map.png`, `results/plots/EXP_E_required_alpha_vs_distance.png`, `results/plots/EXP_E_max_allowed_distance_vs_ionic_strength.png`, `results/plots/EXP_E_noise_floor_requirement.png`.
- Notes: Experiment E converts the Debye-screening limitation into explicit design requirements. It remains a simulation-based requirement analysis, not experimental validation or fabricated device performance.
