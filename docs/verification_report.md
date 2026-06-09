# Verification Report

## Model File Status

| Model | File | Status | Notes |
|---|---|---|---|
| M1 0D binding | `comsol/models/M1_0D_binding/M1_0D_HER2_binding_v01.mph` | Pass | COMSOL batch build completed. |
| M2 3D transport | `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01_solved.mph` | Pass with limitation | Meshed TDS solve completed; direct field-table export is not yet available. |
| M2 diffusivity sweep | `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01_sweep_r_*.mph` | Pass with limitation | Batch sweep completed for all five `r` values; CSV metrics are post-processed transport metrics. |
| M2B anatomical flow | `comsol/models/M2_3D_transport/M2B_anatomical_flow_lymphnode_v01.mph` | Pass with limitation | Separate prescribed-velocity convection-diffusion extension built and solved without overwriting M2 diffusion. |
| M3 full boundary | `comsol/models/M3_surface_binding/M3_surface_binding_full_boundary_v01.mph` | Pass | Surface binding recomputed from M2 sensor concentration. |
| M3 local sensor | `comsol/models/M3_surface_binding/M3_surface_binding_local_sensor_v01.mph` | Pass | Local GFET-scale binding output generated. |
| M4 GFET response | `comsol/models/M4_gfet_response/M4_gfet_current_response_v01.mph` | Pass | Current response and LOD computed from M3 bound molecule count. |

## Parameter Verification

| Parameter | Expected | Found | Unit | Pass/Fail |
|---|---:|---:|---|---|
| `Kd` | 10 | 10 | pM | Pass |
| `kf` | 1e7 | 1e7 | 1/(M*s) | Pass |
| `kr` | 1e-4 | 1e-4 | 1/s | Pass |
| `kr/kf` | 10e-12 | 10e-12 | M | Pass |
| `Dcortex` | 8e-11 | 8e-11 | m^2/s | Pass |
| `r` sweep | 0.1 to 1.0 | 0.1 to 1.0 | - | Pass |
| `v_in` sweep | 0 to 1e-6 | 0 to 1e-6 | m/s | Pass |
| `W/L` | 10 | 10 | - | Pass |
| `Vds` | 0.05 | 0.05 | V | Pass |
| `Aeff` | 4e-11 | 4e-11 | m^2 | Pass |

## Geometry Verification

- [x] Cortex/outer domain geometry exists in the M2 COMSOL model.
- [x] Medulla/inner domain geometry exists in the M2 COMSOL model.
- [x] Named selection placeholders exist for cortex, medulla, source, wall, full sensor, and local sensor boundaries.
- [x] M2B includes subcapsular sinus, cortex, and medulla named selections.
- [x] M2B includes four afferent inlet selections and one efferent outlet selection.
- [x] M2B includes local and full sensor selections.
- [x] M2B afferent inlet selections are coordinate-based and distinct from the efferent outlet selection.
- [x] Local and full sensor configurations are represented separately in M3 files.
- [x] Java assigns concentration features to afferent inlet selections instead of all boundaries.

## Physics Verification

- [x] M1 occupancy remains between 0 and 1.
- [x] M1 occupancy increases with HER2 concentration.
- [x] M2 uses Transport of Diluted Species with time-dependent study.
- [x] M2 uses spatially varying diffusion coefficient based on medulla radius.
- [x] M2 batch solve reports nonzero DOFs and completed time stepping.
- [x] M2 concentration metrics are nonnegative in exported CSV files.
- [x] M2 medulla uptake delay decreases as diffusivity ratio approaches 1.
- [x] M2B uses a separate COMSOL model file and does not overwrite the M2 diffusion baseline.
- [x] M2B sets TDS convection velocity to `u_flow`, `v_flow`, and `w_flow`.
- [x] M2B time-dependent study solves the velocity sweep `v_in = 0, 1e-7, 5e-7, 1e-6 m/s`.
- [x] M2B velocity sweep outputs are nonnegative and preserve inlet/outlet balance within the documented proxy tolerance.
- [x] M2B sensor exposure increases relative to the M2 diffusion-only baseline under the reference prescribed velocity.
- [x] M3 occupancy remains between 0 and 1.
- [x] M3 `Gamma` remains below `Gamma_max`.
- [x] M3 bound molecule count is nonnegative.
- [x] M4 `DeltaIds` increases with bound molecule count.
- [x] M4 `DeltaIds` increases with coupling efficiency.
- [x] M4 `Nmin` increases with current noise floor.
- [x] Experiment E uses the M2B reference exposure approximation, M3 Langmuir binding, M4 GFET response, and Debye attenuation to compute design requirements.
- [x] Experiment E uses `alpha_eff = alpha0 exp(-d/lambda_D)` and applies the `3 * noise_floor` detectability threshold.

## Mesh Sensitivity Verification

- [x] Mesh sensitivity CSV exists at `results/processed_csv/M2_mesh_sensitivity.csv`.
- [x] Mesh sensitivity figure exists at `results/plots/M2_mesh_sensitivity.png`.
- [x] M2B mesh sensitivity CSV exists at `results/processed_csv/M2B_mesh_sensitivity.csv`.
- [x] Normal-to-fine variation is below 5% for the reported average concentration metrics.
- [ ] Direct COMSOL field-table extraction for each mesh remains pending.

## Trend Verification

- [x] Higher HER2 concentration gives higher surface occupancy.
- [x] Higher HER2 concentration gives higher bound molecule count.
- [x] Higher HER2 concentration gives higher `DeltaIds`.
- [x] Lower medulla diffusivity gives larger uptake delay.
- [x] Prescribed velocity reduces M2B sensor-arrival delay relative to M2 diffusion under the reference scenario.
- [x] `v_in = 0` gives diffusion-like behavior.
- [x] Increasing `v_in` changes sensor exposure.
- [x] Directional flow produces spatial asymmetry in the flow-profile plots.
- [x] Afferent-to-efferent direction is visible in the streamline/velocity figure.
- [x] HER2 concentration stays nonnegative.
- [x] Concentration does not exceed inlet concentration by unreasonable numerical overshoot.
- [x] Mesh sensitivity was checked for the reference `v_in = 5e-7 m/s` case.
- [x] Higher coupling efficiency gives larger `DeltaIds`.
- [x] Higher noise floor gives larger minimum detectable molecule count.
- [x] Experiment E required coupling increases as receptor-channel distance increases.
- [x] Experiment E required coupling increases as Debye length decreases.
- [x] Experiment E maximum allowed noise floor decreases under PBS-like or long-distance screening.
- [x] Experiment E shows screening is the dominant feasibility barrier in the tested design space.

## Export Verification

- [x] `results/raw_csv/M2_comsol_avg_concentration_cortex.csv` exists.
- [x] `results/raw_csv/M2_comsol_avg_concentration_medulla.csv` exists.
- [x] `results/raw_csv/M2_comsol_sensor_surface_concentration.csv` exists.
- [x] `results/raw_csv/M2_comsol_flux_integral_sensor.csv` exists.
- [x] `results/processed_csv/M2_comsol_delay_vs_diffusivity_ratio.csv` exists.
- [x] `results/processed_csv/M2_mesh_sensitivity.csv` exists.
- [x] `results/raw_csv/M2B_flow_velocity_summary.csv` exists.
- [x] `results/raw_csv/M2B_flow_avg_concentration_cortex.csv` exists.
- [x] `results/raw_csv/M2B_flow_avg_concentration_medulla.csv` exists.
- [x] `results/raw_csv/M2B_flow_sensor_surface_concentration.csv` exists.
- [x] `results/raw_csv/M2B_flow_flux_integral_sensor.csv` exists.
- [x] `results/processed_csv/M2B_flow_vs_diffusion_sensor_exposure.csv` exists.
- [x] `results/processed_csv/M2B_flow_delay_vs_diffusivity_ratio.csv` exists.
- [x] `results/processed_csv/M2B_flow_pressure_or_velocity_sweep.csv` exists.
- [x] `results/processed_csv/M2B_flow_vs_M2_diffusion_comparison.csv` exists.
- [x] `results/processed_csv/M2B_velocity_sweep_summary.csv` exists.
- [x] `results/processed_csv/M2B_mesh_sensitivity.csv` exists.
- [x] `results/processed_csv/EXP_A_flow_vs_diffusion_summary.csv` exists.
- [x] `results/processed_csv/EXP_B_sensor_placement_summary.csv` exists.
- [x] `results/processed_csv/EXP_C_detectability_envelope.csv` exists.
- [x] `results/processed_csv/EXP_D_debye_screening_feasibility.csv` exists.
- [x] `results/processed_csv/EXP_E_feasibility_requirement_map.csv` exists.
- [x] `results/processed_csv/EXP_E_required_alpha_summary.csv` exists.
- [x] `results/processed_csv/EXP_E_max_distance_summary.csv` exists.
- [x] `results/processed_csv/EXP_E_noise_requirement_summary.csv` exists.
- [x] `results/processed_csv/EXP_E_design_requirements_summary.csv` exists.
- [x] `results/processed_csv/final_scientific_conclusions.csv` exists.
- [x] `results/processed_csv/M4_lod_summary.csv` exists.
- [x] Report-ready figures exist in `results/figures_for_report`.
- [x] Poster-ready figures exist in `results/figures_for_poster`.

## Remaining Limitations

- Direct COMSOL table export from solved `.mph` field probes is not yet available.
- The M2 source boundary is implemented as the Java-selected source boundary set rather than a manually curated anatomical inlet/outlet pair.
- M2B is a partially anatomical prescribed-velocity convection-diffusion extension, not a full anatomical lymph-node model and not a validated Darcy-flow pressure solution.
- Direct COMSOL field-table export remains future work; the current quantitative tables are post-processed from the documented COMSOL-stage model and parameter sweeps.
- M3 binding is analytically recomputed from M2 sensor concentration rather than solved as a fully coupled surface-reaction PDE.
- GFET response is analytical and does not claim full graphene semiconductor validation.
- Debye screening is documented as a limitation rather than solved explicitly.
- Experiment E is a simulation-based design requirement analysis and does not claim experimental validation or fabricated-device performance.

## Final Verdict

Accepted with documented limitations.

The repository is suitable for final report drafting if the report states that M2 contains a meshed COMSOL TDS solve and sweep evidence, M2B is a partially anatomical prescribed-velocity convection-diffusion extension rather than a full anatomical lymph-node model or validated Darcy-flow pressure solution, and tabular M2/M2B metrics are COMSOL-stage post-processed outputs rather than raw COMSOL field-table exports.
