# Literature Summary

This page collects the scientific background that should be traceable to the final report bibliography.

## HER2 as a Biomarker

HER2 is a clinically important breast cancer biomarker associated with aggressive disease subtypes and treatment selection. The project treats HER2 as the target antigen to be detected by immobilized antibodies on a GFET sensing surface.

## Antigen-Antibody Binding

The sensing model uses reversible binding between free HER2 antigen and antibody binding sites on the graphene functionalization layer:

```text
Ag + Ab <-> AgAb
r = k_f [Ag][Ab] - k_r [AgAb]
K_d = k_r / k_f
```

For surface binding, free antibody sites are represented as the remaining available surface density rather than a volume concentration.

## FET and GFET Biosensing

Field-effect biosensors convert local electrostatic changes near the channel into electrical signal changes. In GFET biosensors, bound biomolecules perturb the effective carrier density in graphene, producing a drain-source current shift.

## Related Work Buckets

- ISFET foundations: early ion-sensitive transistor work that established chemical/electrical transduction.
- FET immunosensors: antibody-functionalized field-effect devices for label-free biomarker sensing.
- Graphene biosensors: high surface-area channels with strong sensitivity to surface charge and local electrostatics.
- GFET antigen detection: studies mapping antigen binding to measurable current or transfer-curve shifts.

## Reference Tracking

Add each source to `report/references.bib` and note which parameter or claim it supports. Claims about diffusion coefficients, HER2 concentration ranges, antibody kinetics, Debye screening, or noise floors should not remain uncited in the final report.
