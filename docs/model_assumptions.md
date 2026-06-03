# Model Assumptions

This document records assumptions that must remain consistent between COMSOL files, scripts, results, and the final report.

## Biological Assumptions

- HER2 is modeled as a diluted species.
- The sensing surface is graphene functionalized with immobilized antibodies.
- Antigen-antibody binding is reversible.
- Antibody site density is finite, so binding saturates at high antigen exposure.
- No wet-lab validation is included in the current scope.

## Transport Assumptions

- The baseline model uses diffusion-only transport.
- Optional flow or convection cases can be added as comparison scenarios.
- No-flux boundaries are used where the geometry represents impermeable walls.
- Inlet or source boundaries represent HER2 exposure.
- Heterogeneous diffusivity can be used when modeling cortex/medulla-inspired domains.

## Surface Binding Assumptions

Surface binding uses local HER2 concentration at the sensing boundary:

```text
r_s = k_f c_HER2 (Gamma_max - Gamma_bound) - k_r Gamma_bound
```

where `Gamma_bound` is bound HER2 surface density and `Gamma_max` is available antibody site density.

## Electrical Assumptions

- Bound HER2 perturbs local surface charge near the GFET channel.
- Surface charge perturbation is approximated as an effective carrier density shift.
- Drain-source current modulation is proportional to the effective carrier density change:

```text
Delta I_DS = (W / L) e mu V_DS Delta n
```

- Coupling efficiency should be stated explicitly when converting bound molecule count into `Delta n`.
- Physiological ionic strength may reduce sensitivity through Debye screening.

## Analysis Assumptions

- Sensitivity is estimated from the slope of `Delta I_DS` versus HER2 concentration.
- LOD is estimated as:

```text
LOD = 3 sigma / S
```

where `sigma` is the assumed or measured noise standard deviation and `S` is sensitivity.

## Open Items

- Confirm kinetic constants `k_f` and `k_r` from literature or report assumptions.
- Confirm diffusion coefficients for the selected medium.
- Confirm GFET geometry, mobility, bias voltage, and noise floor.
- Define whether final results are reported under diffusion-only or flow-assisted conditions.
