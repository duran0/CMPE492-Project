# GitHub Milestone and Issue Backlog

## Milestone: CMPE 492 Final Deliverables

Goal: complete the COMSOL-based GFET biosensor simulation workflow, generate reproducible outputs, and prepare the final report, poster, short video, and repository documentation.

Suggested due date: official CMPE 492 final submission deadline.

Milestone description:

```md
This milestone covers the final CMPE 492 deliverables for the project "In-body Antigen Detection via Antibodies on a Transistor." The goal is to complete COMSOL simulation work, document the GFET-based HER2 detection model, generate reproducible simulation outputs, and prepare the final report, poster, short video, and GitHub repository package.
```

Create this manually in GitHub under Issues -> Milestones -> New milestone if API access is unavailable.

## Issue 1: Set up final repository structure

Labels: `documentation`, `repo-setup`, `priority-high`

### Objective
Create a clean repository structure for the final CMPE 492 deliverables.

### Tasks
- Create folders: `/docs`, `/report`, `/poster`, `/video`, `/comsol`, `/results`, `/figures`, `/scripts`, and `/references`.
- Add placeholder README files to empty folders.
- Add `.gitignore` for temporary files, LaTeX build files, COMSOL autosave files, and OS files.
- Add a short project description to the root README.

### Acceptance Criteria
- Repository has a clear structure.
- Each folder has a defined purpose.
- Large or generated files are not dumped into the root directory.

## Issue 2: Rewrite project README for final submission

Labels: `documentation`, `priority-high`

### Objective
Prepare a professional README that explains the project, methodology, tools, and deliverables.

### Tasks
- Add project title, student/advisor information, and short abstract.
- Explain the HER2 detection problem.
- Explain the GFET-based sensing principle.
- Add repository structure.
- Add instructions for accessing COMSOL files and results.
- Add deliverables section for final report, poster, short video, and Git repository.
- Add citation/reference note.

### Acceptance Criteria
- README explains the project without requiring the report.
- A reviewer can understand what the repository contains within 2 minutes.

## Issue 3: Prepare literature and background documentation

Labels: `documentation`, `research`

### Objective
Organize the scientific background used in the final report.

### Tasks
- Summarize HER2 as a breast cancer biomarker.
- Summarize antigen-antibody binding.
- Summarize FET/GFET biosensor principles.
- Add short notes on ISFETs, FET immunosensors, graphene biosensors, and GFET antigen detection.
- Store notes under `/docs/literature_summary.md`.

### Acceptance Criteria
- Literature summary is concise and usable for report writing.
- References are traceable to the bibliography.

## Issue 4: Define COMSOL model assumptions and parameters

Labels: `comsol`, `modeling`, `priority-high`

### Objective
Document all assumptions and parameters used in the COMSOL model.

### Tasks
- Define biological assumptions.
- Define transport assumptions.
- Define electrical assumptions.
- Create `/docs/model_assumptions.md`.
- Create `/comsol/parameters.csv`.

### Acceptance Criteria
- All simulation assumptions are explicitly listed.
- Parameters are consistent with the final report.

## Issue 5: Build baseline 0D HER2-antibody kinetic model

Labels: `comsol`, `simulation`, `kinetics`

### Objective
Implement the 0D antigen-antibody binding model in COMSOL.

### Tasks
- Define HER2 antigen concentration.
- Define antibody binding sites.
- Implement reversible binding with `k_f`, `k_r`, and `[AgAb]`.
- Extract equilibrium behavior and `K_d` relation.
- Export plots of occupancy versus concentration/time.

### Acceptance Criteria
- 0D kinetic model runs successfully.
- Binding behavior reaches expected equilibrium.
- Exported figures are saved under `/results/kinetics`.

## Issue 6: Build 3D transport model for HER2 diffusion

Labels: `comsol`, `simulation`, `transport`, `priority-high`

### Objective
Create the 3D transport model for HER2 diffusion toward the sensing region.

### Tasks
- Define simulation geometry.
- Assign HER2 diffusion coefficient.
- Add inlet/source boundary condition.
- Add no-flux boundaries where appropriate.
- Run time-dependent diffusion simulation.
- Export concentration maps over time.

### Acceptance Criteria
- 3D HER2 transport model runs without solver failure.
- Concentration profiles are exported.
- Results are saved under `/results/transport`.

## Issue 7: Add surface binding boundary to the transport model

Labels: `comsol`, `simulation`, `surface-reaction`

### Objective
Couple HER2 transport with antibody binding at the GFET sensing surface.

### Tasks
- Define graphene sensing surface.
- Add surface reaction boundary.
- Couple local HER2 concentration to surface occupancy.
- Export bound HER2 density over time.
- Compare surface concentration and bound molecule count.

### Acceptance Criteria
- Surface binding is coupled to local HER2 concentration.
- Bound antigen density can be extracted from COMSOL.
- Exported data is saved under `/results/surface_binding`.

## Issue 8: Implement GFET electrical response model

Labels: `comsol`, `simulation`, `electrical`, `priority-high`

### Objective
Translate bound HER2 molecules into drain-source current modulation.

### Tasks
- Define GFET geometry parameters: channel width, channel length, carrier mobility, and source-drain voltage.
- Implement a current shift relation where `Delta I_DS` is proportional to bound HER2 count.
- Compute current response for multiple HER2 concentrations.
- Export `Delta I_DS` versus concentration curves.

### Acceptance Criteria
- Electrical response is computed from bound HER2.
- `Delta I_DS` curves are generated.
- Results are saved under `/results/electrical_response`.

## Issue 9: Run parametric sweep over HER2 concentration

Labels: `simulation`, `results`, `priority-high`

### Objective
Evaluate sensor response across biologically relevant HER2 concentrations.

### Tasks
- Select HER2 concentration range.
- Run low, medium, and high concentration cases.
- Extract surface occupancy, bound molecule count, `Delta I_DS`, and response time.
- Generate concentration-response and time-response plots.

### Acceptance Criteria
- Parametric sweep is completed.
- Exported plots are suitable for report/poster.
- Data tables are stored under `/results/parametric_sweeps`.

## Issue 10: Estimate sensitivity and limit of detection

Labels: `analysis`, `results`, `priority-high`

### Objective
Estimate sensitivity and simulated limit of detection for the GFET biosensor.

### Tasks
- Define noise floor assumption.
- Compute sensor sensitivity from `Delta I_DS` versus concentration.
- Estimate LOD using `LOD = 3 sigma / S`.
- Compare result against target LOD `<= 1 pM`.
- Prepare final plot/table for report.

### Acceptance Criteria
- Sensitivity is calculated.
- LOD is estimated and explained.
- Result is included in `/results/lod_analysis`.

## Issue 11: Validate static vs. flow or diffusion-only scenarios

Labels: `validation`, `simulation`, `analysis`

### Objective
Compare baseline diffusion-only results with optional flow/static scenarios.

### Tasks
- Run diffusion-only baseline.
- If feasible, add flow or convection case.
- Compare antigen arrival time, surface concentration, bound HER2 count, and current response.
- Discuss whether flow improves detection speed or complicates interpretation.

### Acceptance Criteria
- At least one baseline and one comparison scenario are analyzed.
- Results are summarized in a table.
- Limitations are clearly stated.

## Issue 12: Prepare final report LaTeX/PDF package

Labels: `report`, `documentation`, `priority-high`

### Objective
Prepare the final CMPE 492 report using the completed simulation results.

### Tasks
- Update introduction and problem definition.
- Refine related work.
- Complete methodology with final COMSOL workflow.
- Add implementation details, results, discussion, limitations, and future work.
- Update references.
- Export final PDF.

### Acceptance Criteria
- Final report PDF is generated.
- Figures and tables are numbered and cited.
- Results are consistent with repository outputs.

## Issue 13: Prepare final poster

Labels: `poster`, `documentation`, `priority-high`

### Objective
Create the final research poster summarizing the project.

### Tasks
- Add title, student, advisors, and university.
- Include motivation, GFET sensing mechanism, COMSOL workflow, key results, LOD/sensitivity, limitations, and future work.
- Use high-resolution figures.
- Export PDF.

### Acceptance Criteria
- Poster is readable and visually coherent.
- Main contribution is understandable in under 60 seconds.
- Poster PDF is stored under `/poster`.

## Issue 14: Prepare 5-minute final video script and assets

Labels: `video`, `documentation`, `priority-high`

### Objective
Prepare the short final project video.

### Tasks
- Write a 5-minute script.
- Prepare slide/visual sequence.
- Include problem, proposed GFET biosensor, COMSOL model, main results, and final conclusion.
- Record voice-over or presentation.
- Export final video.

### Acceptance Criteria
- Video duration is under 5 minutes.
- Main technical contribution is clearly explained.
- Video file or link is added to `/video`.
