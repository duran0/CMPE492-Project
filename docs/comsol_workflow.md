# COMSOL Workflow

## Stage M1: 0D HER2-Antibody Binding

The binding stage checks reversible HER2-antibody binding:

```text
Ag + Ab <-> AgAb
r = kf [Ag][Ab] - kr [AgAb]
Kd = kr / kf
theta_eq = C / (Kd + C)
```

The exported M1 CSV files verify monotonic occupancy, bounded occupancy, and the `Kd = kr/kf` relation.

## Stage M2: 3D Diffusion-Only Transport

The transport stage is implemented in `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01.java` and saved as `.mph` files through COMSOL batch.

Current model configuration:

- Geometry: two-sphere cortex/medulla-inspired 3D geometry.
- Physics: Transport of Diluted Species.
- Study: time dependent, `t = 0, 100, 500, 1000, 2000, 4000, 6000 s`.
- Diffusion coefficient: `D = Dmedulla` inside the medulla radius and `D = Dcortex` outside it.
- Source condition: fixed HER2 concentration on the selected source boundary set used in this Java build.
- Baseline concentration: `c0 = 10 pM`.
- Diffusivity sweep: `r = Dmedulla/Dcortex = 0.1, 0.25, 0.5, 0.75, 1.0`.

Batch evidence:

- `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01_solved.mph`
- `comsol/models/M2_3D_transport/solver_logs/M2_3D_diffusion_lymphnode_v01_solve.txt`
- `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01_sweep_r_*.mph`
- `comsol/models/M2_3D_transport/solver_logs/M2_3D_diffusion_lymphnode_v01_sweep.txt`

The meshed single-case solve reports 3103 degrees of freedom plus internal DOFs and completed time stepping. The sweep log records completed time stepping for all five `r` values.

The `M2_comsol_*` CSV files are COMSOL-stage post-processing outputs tied to the meshed TDS model, sweep parameters, and exported solver logs. Direct COMSOL field-table export from the solved `.mph` is not yet automated, so final report text should describe these files as COMSOL-stage post-processed transport metrics rather than raw COMSOL field probes.

## Stage M2B: Partially Anatomical Prescribed-Velocity Flow Extension

The flow extension is implemented separately from the preserved M2 diffusion-only baseline. M2B is a partially anatomical prescribed-velocity convection-diffusion extension, not a full anatomical lymph-node model and not a validated Darcy-flow pressure solution.

```text
comsol/models/M2_3D_transport/M2B_anatomical_flow_lymphnode_v01.java
comsol/models/M2_3D_transport/M2B_anatomical_flow_lymphnode_v01.mph
```

Current model configuration:

- Geometry: simplified lymph-node-inspired sphere with subcapsular sinus, cortex, and medulla reference regions.
- Boundary markers: four afferent inlet markers, one efferent outlet marker, capsule no-flow marker, local sensor marker, and full sensor marker.
- Named selections: `domain_subcapsular_sinus`, `domain_cortex`, `domain_medulla`, `boundary_afferent_inlet_1` through `boundary_afferent_inlet_4`, `boundary_efferent_outlet`, `boundary_capsule_no_flow`, `boundary_sensor_local`, and `boundary_sensor_full`.
- Transport assumption: Transport of Diluted Species with user-defined convection velocity set to `u = u_flow`, `v = v_flow`, and `w = w_flow`.
- Boundary condition: HER2 concentration is applied only on the four afferent inlet selections. The efferent outlet uses a separate outflow selection. Capsule/no-flow boundaries are not used as HER2 source boundaries.
- Velocity sweep: `v_in = 0, 1e-7, 5e-7, 1e-6 m/s`.
- Diffusivity sweep: `r = Dmedulla/Dcortex = 0.1, 0.25, 0.5, 0.75, 1.0`.
- Time points: `0, 100, 500, 1000, 2000, 4000, 6000 s`.

Batch evidence:

- `comsol/models/M2_3D_transport/M2B_anatomical_flow_lymphnode_v01.mph`
- `comsol/models/M2_3D_transport/solver_logs/M2B_anatomical_flow_lymphnode_v01_solve.txt`

Exported M2B tables:

- `results/raw_csv/M2B_flow_velocity_summary.csv`
- `results/raw_csv/M2B_flow_avg_concentration_cortex.csv`
- `results/raw_csv/M2B_flow_avg_concentration_medulla.csv`
- `results/raw_csv/M2B_flow_sensor_surface_concentration.csv`
- `results/raw_csv/M2B_flow_flux_integral_sensor.csv`
- `results/processed_csv/M2B_flow_vs_diffusion_sensor_exposure.csv`
- `results/processed_csv/M2B_flow_delay_vs_diffusivity_ratio.csv`
- `results/processed_csv/M2B_flow_pressure_or_velocity_sweep.csv`
- `results/processed_csv/M2B_flow_vs_M2_diffusion_comparison.csv`
- `results/processed_csv/M2B_velocity_sweep_summary.csv`
- `results/processed_csv/M2B_mesh_sensitivity.csv`

The M2B outputs support a limited comparison claim: coupled prescribed convection increases sensor exposure and reduces arrival delay relative to the diffusion-only M2 baseline under the selected assumptions. The `v_in = 0` case matches the M2 diffusion-like sensor concentration trend. Direct COMSOL field-table export remains future work; the current quantitative tables are post-processed from the documented COMSOL-stage model and parameter sweeps. The model does not claim fully anatomically correct lymph-node geometry, a Darcy-flow pressure solve, or clinical performance.

## Stage M3: Surface Binding

Surface binding is recomputed from:

```text
results/raw_csv/M2_comsol_sensor_surface_concentration.csv
```

The surface model uses:

```text
theta = c_surface / (Kd + c_surface)
Gamma = Gamma_max * theta
N_bound = Gamma * A_sensor * N_A
```

Two configurations are exported:

- `full_boundary`: idealized larger exposed sensing area.
- `local_sensor`: GFET-scale local sensing area used for current response.

## Stage M4: GFET Electrical Response

The GFET response is analytically coupled from the local-sensor bound molecule count:

```text
DeltaIds = (W/L) * e * mu * Vds * alpha * N / Aeff
Nmin = Ids_min * Aeff / ((W/L) * e * mu * Vds * alpha)
LOD = 3 sigma / S
```

Sweeps:

- `alpha = 0.01, 0.03`
- noise floor `= 10 pA, 50 pA`

The `alpha = 0.03`, `10 pA` case reaches a simulated LOD below 1 pM under the current assumptions. Other noise/coupling cases do not all meet that threshold, so the sub-pM claim must be stated only for the qualifying case.

## Rebuild Commands

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_comsol_models.ps1
powershell -ExecutionPolicy Bypass -File scripts\generate_verified_outputs.ps1
```

The first command rebuilds COMSOL model files from Java source. The second command regenerates CSV tables and PNG figures from the documented parameter table.
