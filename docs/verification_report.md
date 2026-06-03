# Verification Report

## Model Files Verified

| Model | File | Status | Notes |
|---|---|---|---|
| M1 0D binding | `comsol/models/M1_0D_binding/M1_0D_HER2_binding_v01.mph` | Pass | COMSOL batch build completed. |
| M2 transport | `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01.mph` | Partial | Geometry scaffold completed; reduced-order trend outputs completed; final 3D PDE solve pending. |
| M3 full boundary | `comsol/models/M3_surface_binding/M3_surface_binding_full_boundary_v01.mph` | Partial | COMSOL scaffold completed; analytical surface-binding outputs completed. |
| M3 local sensor | `comsol/models/M3_surface_binding/M3_surface_binding_local_sensor_v01.mph` | Partial | COMSOL scaffold completed; analytical surface-binding outputs completed. |
| M4 GFET response | `comsol/models/M4_gfet_response/M4_gfet_current_response_v01.mph` | Pass | Analytical current-response outputs completed. |

## Parameter Verification

| Parameter | Expected | Found | Unit | Pass/Fail |
|---|---:|---:|---|---|
| `Kd` | 10 | 10 | pM | Pass |
| `kf` | 1e7 | 1e7 | 1/(M*s) | Pass |
| `kr` | 1e-4 | 1e-4 | 1/s | Pass |
| `kr/kf` | 10e-12 | 10e-12 | M | Pass |
| `W/L` | 10 | 10 | - | Pass |
| `Vds` | 0.05 | 0.05 | V | Pass |
| `Aeff` | 4e-11 | 4e-11 | m^2 | Pass |

## Physics Verification

- [x] M1 occupancy remains between 0 and 1.
- [x] M1 occupancy increases with HER2 concentration.
- [x] M2 concentration remains nonnegative in exported reduced-order outputs.
- [x] M2 medulla uptake delay decreases as diffusivity ratio approaches 1.
- [x] M3 surface occupancy remains between 0 and 1.
- [x] M3 bound molecule count remains nonnegative.
- [x] M3 full-boundary total bound count exceeds local-sensor total bound count under comparable concentration.
- [x] M4 `DeltaIds` increases with bound molecule count.
- [x] M4 `DeltaIds` increases with coupling efficiency.
- [x] M4 `Nmin` increases with current noise floor.
- [x] M4 LOD reaches below 1 pM for the `alpha = 0.03`, 10 pA case under the current assumptions.

## Export Verification

- [x] M1 CSV outputs exist.
- [x] M2 CSV outputs exist.
- [x] M3 CSV outputs exist.
- [x] M4 CSV outputs exist.
- [x] Required report figure PNGs exist in `results/figures_for_report`.
- [x] Required poster figure PNGs exist in `results/figures_for_poster`.
- [x] Parameter export exists at `comsol/exports/parameters.csv`.

## Remaining Fixes

- Implement and run the final 3D Transport of Diluted Species model for M2.
- Replace M2 concentration-profile and flux proxy plots with COMSOL-exported slice/streamline figures.
- Add dynamic COMSOL surface-reaction coupling for M3 if solver stability allows.
- Run mesh sensitivity for the final M2/M3 COMSOL solve.

## Final Verdict

Accepted for M1 and M4. Accepted as scaffolded baseline for M2 and M3. Final report should not present M2/M3 proxy plots as final COMSOL PDE results until the remaining fixes are completed.
