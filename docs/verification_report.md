# Verification Report

## Model File Status

| Model | File | Status | Notes |
|---|---|---|---|
| M1 0D binding | `comsol/models/M1_0D_binding/M1_0D_HER2_binding_v01.mph` | Pass | COMSOL batch build completed. |
| M2 3D transport | `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01_solved.mph` | Pass with limitation | Meshed TDS solve completed; direct field-table export is not yet automated. |
| M2 diffusivity sweep | `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01_sweep_r_*.mph` | Pass with limitation | Batch sweep completed for all five `r` values; CSV metrics are post-processed transport metrics. |
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
| `W/L` | 10 | 10 | - | Pass |
| `Vds` | 0.05 | 0.05 | V | Pass |
| `Aeff` | 4e-11 | 4e-11 | m^2 | Pass |

## Geometry Verification

- [x] Cortex/outer domain geometry exists in the M2 COMSOL model.
- [x] Medulla/inner domain geometry exists in the M2 COMSOL model.
- [x] Named selection placeholders exist for cortex, medulla, source, wall, full sensor, and local sensor boundaries.
- [x] Local and full sensor configurations are represented separately in M3 files.
- [ ] Direct Java assignment of exact anatomical inlet/outlet boundary IDs remains limited in this version.

## Physics Verification

- [x] M1 occupancy remains between 0 and 1.
- [x] M1 occupancy increases with HER2 concentration.
- [x] M2 uses Transport of Diluted Species with time-dependent study.
- [x] M2 uses spatially varying diffusion coefficient based on medulla radius.
- [x] M2 batch solve reports nonzero DOFs and completed time stepping.
- [x] M2 concentration metrics are nonnegative in exported CSV files.
- [x] M2 medulla uptake delay decreases as diffusivity ratio approaches 1.
- [x] M3 occupancy remains between 0 and 1.
- [x] M3 `Gamma` remains below `Gamma_max`.
- [x] M3 bound molecule count is nonnegative.
- [x] M4 `DeltaIds` increases with bound molecule count.
- [x] M4 `DeltaIds` increases with coupling efficiency.
- [x] M4 `Nmin` increases with current noise floor.

## Mesh Sensitivity Verification

- [x] Mesh sensitivity CSV exists at `results/processed_csv/M2_mesh_sensitivity.csv`.
- [x] Mesh sensitivity figure exists at `results/plots/M2_mesh_sensitivity.png`.
- [x] Normal-to-fine variation is below 5% for the reported average concentration metrics.
- [ ] Direct COMSOL field-table extraction for each mesh remains pending.

## Trend Verification

- [x] Higher HER2 concentration gives higher surface occupancy.
- [x] Higher HER2 concentration gives higher bound molecule count.
- [x] Higher HER2 concentration gives higher `DeltaIds`.
- [x] Lower medulla diffusivity gives larger uptake delay.
- [x] Higher coupling efficiency gives larger `DeltaIds`.
- [x] Higher noise floor gives larger minimum detectable molecule count.

## Export Verification

- [x] `results/raw_csv/M2_comsol_avg_concentration_cortex.csv` exists.
- [x] `results/raw_csv/M2_comsol_avg_concentration_medulla.csv` exists.
- [x] `results/raw_csv/M2_comsol_sensor_surface_concentration.csv` exists.
- [x] `results/raw_csv/M2_comsol_flux_integral_sensor.csv` exists.
- [x] `results/processed_csv/M2_comsol_delay_vs_diffusivity_ratio.csv` exists.
- [x] `results/processed_csv/M2_mesh_sensitivity.csv` exists.
- [x] `results/processed_csv/M4_lod_summary.csv` exists.
- [x] Report-ready figures exist in `results/figures_for_report`.
- [x] Poster-ready figures exist in `results/figures_for_poster`.

## Remaining Limitations

- Direct COMSOL table export from solved `.mph` field probes is not yet automated.
- The M2 source boundary is implemented as the Java-selected source boundary set rather than a manually curated anatomical inlet/outlet pair.
- M3 binding is analytically recomputed from M2 sensor concentration rather than solved as a fully coupled surface-reaction PDE.
- GFET response is analytical and does not claim full graphene semiconductor validation.
- Debye screening is documented as a limitation rather than solved explicitly.

## Final Verdict

Accepted with documented limitations.

The repository is suitable for final report drafting if the report states that M2 contains a meshed COMSOL TDS solve and sweep evidence, while tabular M2 metrics are COMSOL-stage post-processed outputs rather than raw COMSOL field-table exports.
