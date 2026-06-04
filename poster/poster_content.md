# Title

In-body Antigen Detection via Antibodies on a Transistor: A Simulation Study of HER2 Transport, GFET Response, and Feasibility Limits

# Problem

HER2 is an important breast cancer biomarker, but continuous in-body monitoring is not established. This project asks whether a GFET biosensor concept could detect HER2 after antigen transport, antibody binding, and electrical transduction are all considered together.

# Main Message Box

Main finding: Directional flow and sensor placement improve HER2 exposure, but electrostatic screening and electronics noise dominate practical GFET detectability.

# Method Pipeline

```text
HER2 concentration
  -> diffusion / lymph-node-inspired directional flow
  -> local sensor exposure
  -> antibody binding and bound molecule count
  -> GFET current response
  -> LOD and detectability test
  -> Debye screening feasibility check
```

# COMSOL Transport and Flow Model

- M2: diffusion-only Transport of Diluted Species baseline in simplified cortex/medulla geometry.
- M2B: partially anatomical prescribed-velocity convection-diffusion extension with afferent inlet regions, hilum-side efferent outlet, local/full sensor regions, and prescribed lymph-flow velocity coupled to HER2 transport.
- Verification: `v_in = 0` matches diffusion-like behavior; increasing `v_in` changes sensor exposure.
- Limitation: M2B is a partially anatomical prescribed-velocity convection-diffusion extension, not a full anatomical lymph-node model and not a validated Darcy-flow pressure solution.

# Key Result 1: Transport / Flow / Placement

- Directional flow improves sensor exposure compared with diffusion-only transport.
- At `C = 10 pM`, reference flow `v_in = 5e-7 m/s` gives `8.73 pM` sensor concentration at 6000 s versus `4.98 pM` for diffusion-only transport.
- Time-to-50% exposure decreases from approximately `6038 s` to `1839 s`.
- Sensor placement affects response timing and current response. In the modeled sweep, the subcapsular/cortical placement is fastest and strongest under the reference flow case. Under directional flow, late-time exposure becomes high across all tested placements, while placement still changes arrival time and pathway exposure.

# Key Result 2: Current Response / LOD

- GFET current response increases with HER2 concentration, coupling efficiency, and bound molecule count.
- Detectability is not universal.
- Experiment C found `99` detectable parameter rows and `36` failing rows across concentration, coupling, noise, and `Kd` sweeps.
- Sub-pM or low-pM detectability is predicted only under favorable coupling, low noise, and binding assumptions.

# Key Result 3: Debye Screening Feasibility

- Electrostatic screening strongly reduces the effective GFET signal.
- Model used `alpha_eff = alpha_0 exp(-d/lambda_D)`.
- PBS-like physiological salt with `lambda_D = 0.8 nm` and `d >= 5 nm` produced `0/60` detectable screened cases.
- This is the main negative feasibility result.

# Main Conclusion

The model predicts detectability only under specific physical and electronic assumptions. Transport and placement influence antigen exposure, but electrostatic screening and noise are likely the main feasibility barriers.

# Limitations

- Simulation-only; no wet-lab validation.
- M2B is a partially anatomical prescribed-velocity convection-diffusion extension, not a full anatomical lymph-node model and not a validated Darcy-flow pressure solution.
- Direct COMSOL field-table export remains future work; the current quantitative tables are post-processed from the documented COMSOL-stage model and parameter sweeps.
- GFET current response is analytical rather than a full graphene device simulation.
- Debye screening parameters are feasibility assumptions, not measured implant conditions.

# Future Work

- Replace prescribed flow with validated porous/Darcy flow.
- Add direct COMSOL field-table export and probe automation.
- Model receptor linker length and charge location more explicitly.
- Explore surface chemistries that reduce effective charge distance.
- Evaluate low-noise electronics and local screening mitigation strategies.
