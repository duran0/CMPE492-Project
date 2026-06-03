# Model Versions

| Version | Model | Purpose | Status | Notes |
|---|---|---|---|---|
| v0.1 | 0D kinetics | HER2-antibody binding sanity check | Built | `comsol/models/M1_0D_binding/M1_0D_HER2_binding_v01.mph`; CSV and plots exported. |
| v0.2 | 3D transport | Diffusion toward sensing region | Scaffolded | `comsol/models/M2_3D_transport/M2_3D_diffusion_lymphnode_v01.mph`; reduced-order transport outputs exported. |
| v0.3 | Surface binding | Coupled transport and surface occupancy | Scaffolded | `comsol/models/M3_surface_binding/`; Langmuir outputs exported from documented equations. |
| v0.4 | GFET response | Convert bound HER2 to Delta I_DS | Built | `comsol/models/M4_gfet_response/M4_gfet_current_response_v01.mph`; analytical response outputs exported. |
| v1.0 | Final coupled workflow | Final report/poster results | Pending | Use for final submission. |
