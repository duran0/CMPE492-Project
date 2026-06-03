# Model Pipeline

```text
HER2 concentration
        |
        v
Transport in solution or lymph-node-inspired medium
        |
        v
Surface binding to immobilized antibody
        |
        v
Bound molecule count or surface density
        |
        v
Surface charge perturbation
        |
        v
GFET carrier density change
        |
        v
Drain-source current modulation, Delta I_DS
```

The pipeline separates transport, binding, and electronics so each modeling layer can be validated independently before coupling the full sensing response.
