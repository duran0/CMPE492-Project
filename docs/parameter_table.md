# Parameter Table

All calculations use SI units internally. Report-friendly units are included for readability.

## Biological Parameters

| Parameter | Symbol | Baseline | SI value | Unit used in calculation | Notes |
|---|---:|---:|---:|---|---|
| HER2 concentration sweep | C | 0.5, 1, 10, 100, 1000 pM | 0.5e-9 to 1e-6 | mol/m^3 | `1 pM = 1e-9 mol/m^3`. |
| Dissociation constant | Kd | 10 pM | 10e-12 | mol/L | Baseline affinity assumption for HER2-antibody binding. |
| Forward rate constant | kf | 1e7 | 1e7 | 1/(M*s) | Literature-range association-rate assumption. |
| Reverse rate constant | kr | 1e-4 | 1e-4 | 1/s | Computed from `kr = kf * Kd`. |
| Effective local binding site density | Bmax_local | 8.30e-12 | 8.30e-12 | mol/m^2 | Chosen as electrically coupled effective density. |
| Effective full-boundary binding site density | Bmax_full | 8.30e-12 | 8.30e-12 | mol/m^2 | Same density over larger exposed area. |

## Transport Parameters

| Parameter | Symbol | Baseline | SI value | Unit | Notes |
|---|---:|---:|---:|---|---|
| Cortex diffusion coefficient | Dcortex | 8e-11 | 8e-11 | m^2/s | Assumed protein-scale diffusion in tissue-like medium. |
| Diffusivity ratio | r | 0.1, 0.25, 0.5, 0.75, 1.0 | same | - | Required sweep. |
| Medulla diffusion coefficient | Dmedulla | r * Dcortex | r * 8e-11 | m^2/s | Lower medulla diffusivity delays uptake. |
| Baseline inlet concentration | c0 | 10 pM | 1e-8 | mol/m^3 | Baseline transport exposure. |
| Simulation time | tmax | 6000 | 6000 | s | Exported at fixed report time points. |
| Time points | t | 0, 100, 500, 1000, 2000, 4000, 6000 | same | s | Shared across stages. |

## GFET Parameters

| Parameter | Symbol | Baseline | SI value | Unit | Notes |
|---|---:|---:|---:|---|---|
| Channel width | W | 20 um | 20e-6 | m | GFET geometry assumption. |
| Channel length | L | 2 um | 2e-6 | m | GFET geometry assumption. |
| Width/length ratio | W/L | 10 | 10 | - | Derived from W and L. |
| Carrier mobility | mu | 0.1 | 0.1 | m^2/(V*s) | Conservative graphene mobility assumption. |
| Drain-source voltage | Vds | 50 mV | 0.05 | V | Bias voltage assumption. |
| Effective sensing area | Aeff | 4e-11 | 4e-11 | m^2 | Local GFET sensing area. |
| Coupling efficiency | alpha | 0.01, 0.03 | same | - | Required sweep. |
| Current noise floor | Ids_min | 10, 50 pA | 10e-12, 50e-12 | A | Required detection-threshold sweep. |

## Core Unit Conversions

```text
1 pM = 1e-12 mol/L = 1e-9 mol/m^3
1 um = 1e-6 m
1 pA = 1e-12 A
```
