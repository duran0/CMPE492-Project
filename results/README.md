# Results

This directory stores exported COMSOL data, post-processed tables, and analysis outputs.

| Folder | Contents |
|---|---|
| `kinetics/` | 0D binding model outputs and occupancy plots. |
| `transport/` | HER2 concentration maps and transport metrics. |
| `surface_binding/` | Bound HER2 surface density and molecule-count exports. |
| `electrical_response/` | GFET current response curves. |
| `parametric_sweeps/` | Concentration sweep tables and comparison plots. |
| `lod_analysis/` | Sensitivity, noise, and LOD calculations. |

Use consistent CSV column names when possible: `time_s`, `concentration_pM`, `bound_count`, `occupancy`, and `delta_ids_A`.
