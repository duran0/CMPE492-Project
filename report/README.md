# Final Report Package

## Compile Command

Run from the `report/` directory:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error final_report.tex
bibtex final_report
pdflatex -interaction=nonstopmode -halt-on-error final_report.tex
pdflatex -interaction=nonstopmode -halt-on-error final_report.tex
```

The report is intentionally one-sided and single-column for final submission readability.

## Figure Refresh Command

Run from the repository root before compiling if the final report figures need to be refreshed from the verified CSV outputs:

```powershell
py scripts\polish_final_report_figures.py
```

## Known Limitations Stated in the Report

- Simulation-only scope: no wet-lab validation, fabricated GFET, clinical validation, or biocompatibility test.
- M2B is a partially anatomical prescribed-velocity convection-diffusion extension, not a full anatomical lymph-node model and not a validated Darcy/Brinkman pressure-flow solution.
- M3 surface binding is analytical post-processing.
- M4 GFET current response is an analytical transduction estimate.
- Debye screening is modeled through exponential attenuation, not fully solved electrostatics.
- Direct COMSOL field-table export is not available for all cases; some quantitative tables are post-processed from documented model assumptions and sweeps.

## Included Result Figures

- `M1_occupancy_vs_concentration.png`
- `M2_comsol_cortex_vs_medulla_uptake.png`
- `M2_comsol_delay_vs_diffusivity_ratio.png`
- `EXP_A_flow_vs_diffusion_sensor_exposure.png`
- `EXP_B_sensor_placement_exposure.png`
- `EXP_B_sensor_placement_deltaIds.png`
- `M4_deltaIds_vs_concentration.png`
- `EXP_C_detectable_region_map.png`
- `EXP_D_lod_vs_ionic_strength.png`
- `EXP_D_detectability_map_screened.png`
- `EXP_E_detectability_requirement_map.png`
- `EXP_E_max_allowed_distance_vs_ionic_strength.png`

## Included Report Tables

- `tables/final_design_requirements_table.tex`
- `tables/final_claims_table.tex`
- `tables/final_summary_table.tex`

No required report figure is currently missing.
