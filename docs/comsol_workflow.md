# COMSOL Workflow

## Stage M1: 0D HER2-Antibody Binding

The first stage checks reversible HER2-antibody binding using:

```text
Ag + Ab <-> AgAb
r = kf [Ag][Ab] - kr [AgAb]
Kd = kr / kf
theta_eq = C / (Kd + C)
```

The generated CSV outputs verify equilibrium occupancy, monotonic concentration response, and the `Kd = kr/kf` relation.

## Stage M2: Diffusion-Only Transport

The transport stage uses a simplified cortex/medulla model to evaluate delayed HER2 uptake. The full COMSOL geometry target is a two-domain lymph-node-inspired geometry with cortex and medulla regions, a fixed-concentration inlet, no-flux walls, and sensor boundaries.

Current exported baseline outputs use the documented reduced-order diffusion equations to verify parameter trends before committing final 3D solver results:

```text
cortex_avg(t) = c0 * (1 - exp(-t / tau_cortex))
medulla_avg(t, r) = c0 * (1 - exp(-t / tau_medulla(r)))
```

where smaller `r = Dmedulla / Dcortex` increases medulla uptake delay.

## Stage M3: Surface Binding

Surface binding is computed from local sensor concentration using Langmuir-type occupancy:

```text
theta = c_surface / (Kd + c_surface)
Gamma = Gamma_max * theta
N_bound = Gamma * A_sensor * N_A
```

Two sensing configurations are tracked:

- Full boundary exposure for idealized maximum binding.
- Local sensor exposure for the GFET sensing area used in electrical response.

## Stage M4: GFET Electrical Response

The electrical response is analytically coupled from bound HER2 count:

```text
DeltaIds = (W/L) * e * mu * Vds * alpha * N / Aeff
Nmin = Ids_min * Aeff / ((W/L) * e * mu * Vds * alpha)
```

This avoids forcing graphene into an unsuitable conventional semiconductor model while preserving unit-consistent transduction from bound molecules to current response.

## Output Policy

Every figure used in the report should have a matching CSV file. Results that are not reproducible from CSV should not be used in the final report.
