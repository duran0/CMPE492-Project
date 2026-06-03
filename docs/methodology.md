# Methodology

## Stage 1: 0D Binding Kinetics

Implement a reversible HER2-antibody binding model to confirm equilibrium behavior, saturation, and the relationship between `k_f`, `k_r`, and `K_d`.

Expected outputs:

- Occupancy versus time.
- Occupancy versus HER2 concentration.
- Equilibrium check against `K_d`.

## Stage 2: 3D HER2 Transport

Build a time-dependent transport model for HER2 diffusion toward the sensing region. The baseline model should be diffusion-only, with flow added only if time allows and the solver remains stable.

Expected outputs:

- Concentration maps over time.
- Surface concentration at the GFET sensing region.
- Response delay metrics.

## Stage 3: Surface Binding Boundary

Couple the local HER2 concentration at the sensing surface to antibody occupancy. Export bound HER2 surface density and total bound molecule count.

Expected outputs:

- Bound surface density versus time.
- Bound molecule count versus concentration.
- Saturation behavior at high HER2 exposure.

## Stage 4: GFET Electrical Response

Convert bound HER2 count or surface density into an effective carrier density shift and drain-source current modulation.

Expected outputs:

- `Delta I_DS` versus HER2 concentration.
- `Delta I_DS` versus time.
- Comparison between low, medium, and high concentration cases.

## Stage 5: Sensitivity and LOD

Estimate sensor sensitivity and simulated LOD using exported response curves and an explicit noise floor assumption.

Expected outputs:

- Sensitivity table.
- LOD estimate.
- Statement comparing LOD to the target `<= 1 pM`.
