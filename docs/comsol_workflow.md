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
