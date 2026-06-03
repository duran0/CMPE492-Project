# In-body Antigen Detection via Antibodies on a Transistor

CMPE 492 senior design project repository for a COMSOL-based graphene field-effect transistor (GFET) biosensor model for HER2 antigen detection.

## Overview

This project studies whether an antibody-functionalized GFET can detect HER2 through a measurable drain-source current shift, `Delta I_DS`. The workflow combines antigen transport, antigen-antibody surface binding, GFET electrical response, sensitivity analysis, and limit of detection (LOD) estimation.

The repository is organized as a reproducible research package rather than only a report archive. COMSOL models and exported simulation data should be placed in the matching folders, with scripts and documentation kept close to the results they explain.

## Modeling Pipeline

```text
HER2 concentration
  -> transport in solution or tissue-inspired medium
  -> surface binding to immobilized antibodies
  -> bound HER2 count or surface density
  -> surface charge perturbation
  -> GFET carrier density change
  -> drain-source current modulation, Delta I_DS
```

## Repository Structure

| Path | Purpose |
|---|---|
| `docs/` | Background, assumptions, methodology, limitations, and project management notes. |
| `comsol/` | COMSOL model notes, parameters, exported settings, and model version tracking. |
| `results/` | Exported simulation data, post-processed tables, and analysis outputs. |
| `figures/` | Architecture diagrams, COMSOL exports, and report-ready figures. |
| `scripts/` | Python utilities for COMSOL export cleanup, response plotting, and LOD calculation. |
| `report/` | Final report source files, bibliography, and generated PDF. |
| `poster/` | Final poster assets and exported poster PDF. |
| `video/` | Final video script, storyboard, and submission link. |
| `references/` | Bibliography notes and source tracking. |

## Target Deliverables

- Final COMSOL model workflow for HER2 transport, binding, and GFET response.
- Reproducible exported data and plots for concentration sweeps.
- Sensitivity and LOD analysis targeting simulated LOD `<= 1 pM`.
- Final CMPE 492 report, poster, short video, and repository documentation.

## Current Simulation Status

- M1 binding kinetics: complete, with CSV outputs and occupancy plots.
- M2 transport: meshed COMSOL Transport of Diluted Species model completed for the baseline case, with COMSOL batch sweep files for diffusivity ratios `0.1` to `1.0`.
- M2 outputs: `M2_comsol_*` CSV and PNG files are COMSOL-stage post-processed metrics tied to the meshed TDS model and solver logs; direct field-table export from solved `.mph` files remains a documented limitation.
- M2B anatomical-flow extension: added a separate partially anatomical lymph-node-inspired model with subcapsular/cortex/medulla geometry markers, four afferent inlet markers, one efferent outlet marker, prescribed-velocity flow assumptions, velocity sweep outputs, and comparison plots against the preserved M2 diffusion baseline.
- M3 surface binding: recomputed from `results/raw_csv/M2_comsol_sensor_surface_concentration.csv`.
- M4 GFET response: recomputed from M3 bound molecule counts, including coupling and noise-floor sweeps.
- LOD: the `alpha = 0.03`, `10 pA` case reaches simulated LOD below `1 pM`; other cases are reported separately and should not be generalized.

## Reproducibility Notes

1. Store COMSOL `.mph` model files under `comsol/` or document external access if files are too large.
2. Export tabular COMSOL outputs as CSV files under the relevant `results/` subfolder.
3. Use `scripts/preprocess_comsol_exports.py` when COMSOL exports include comment headers or inconsistent spacing.
4. Use `scripts/plot_response_curves.py` and `scripts/calculate_lod.py` to regenerate analysis plots and LOD estimates from exported tables.

On this Windows setup, the current reproducible workflow is:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_comsol_models.ps1
powershell -ExecutionPolicy Bypass -File scripts\generate_verified_outputs.ps1
```

The first command rebuilds the COMSOL model files from Java source. The second command regenerates CSV outputs and PNG figures from the documented parameter assumptions.

## Citation and References

The scientific background should be tracked in `docs/literature_summary.md` and `report/references.bib`. Any parameter adopted from a paper, datasheet, or COMSOL example should be traceable to a reference entry or note.
