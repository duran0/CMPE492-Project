# Project Management Plan  
**Project Title:** In-Body Antigen Detection via Antibodies on a Transistor  
**Course:** CMPE 492 – Senior Project
**Student:** Duran Kaan Altın  
**Advisors:** Prof. Tuna Tuğcu, Prof. Kutlu Ülgen  
**Institution:** Boğaziçi University  

---

## 1. Project Vision and Goals

### 1.1 Vision
The goal of this project is to develop a **physics-grounded, reproducible simulation framework** that explains how biological transport phenomena and transistor-level electronics jointly determine the performance limits of a graphene field-effect transistor (GFET) biosensor for HER2 antigen detection.

This project is a **simulation and modeling study**, not a fabrication effort. Its value lies in insight generation, design guidance, and validation of sensing limits.

---

### 1.2 Primary Objectives
By the end of the CMPE 492 semester, the project will:

1. Extend the CMPE 491 work into a complete end-to-end sensing pipeline  
2. Quantify **transport-limited vs. electronics-limited** detection regimes  
3. Deliver modular and parameterized **COMSOL Multiphysics models**  
4. Provide sensitivity and robustness analyses for key design parameters  
5. Produce a well-documented, reproducible **GitHub research repository**  

Success is defined by **explainability and reproducibility**, not only numerical results.

---

## 2. Project Scope

### 2.1 In Scope
- Diffusion-based antigen transport modeling  
- Cortex / medulla heterogeneity representation  
- Boundary-condition-based surface binding abstraction  
- GFET electrical response modeling (ΔI<sub>DS</sub>, carrier density shift)  
- Parametric sweeps and sensitivity analysis  
- Visualization, validation, and interpretation of results  
- Full documentation and GitHub Pages deployment  

---

### 2.2 Out of Scope
- Wet-lab experiments or biological assays  
- Antibody chemistry optimization  
- Device fabrication or cleanroom processes  
- RF or antenna co-design  

Explicit scope control is used to prevent feature creep.

---

## 3. Work Breakdown Structure (WBS)

### WP1 — Baseline Model Consolidation
- Clean and refactor CMPE 491 COMSOL models  
- Reproduce baseline figures and trends  
- Lock geometry, physics interfaces, and parameters  

**Deliverable:** Baseline model tagged as `v1.0`

---

### WP2 — Transport Physics Expansion
- Cortex vs. medulla heterogeneous diffusion  
- Parametric sweeps over diffusivity ratios  
- Time-to-threshold and delay metrics  

**Deliverable:** Transport-limited response analysis

---

### WP3 — GFET Electrical Coupling
- Molecular charge → carrier density mapping  
- Drain–source current response estimation  
- Noise floor and minimum detectable signal  

**Deliverable:** Electrical response module

---

### WP4 — System-Level Sensitivity Analysis
- Transport vs. electronics bottleneck comparison  
- Parameter ranking and robustness checks  
- Engineering design interpretation  

**Deliverable:** Sensitivity and trade-off analysis

---

### WP5 — Documentation and Final Delivery
- GitHub Pages project site  
- Reproducibility instructions  
- Final CMPE 492 report and presentation  

**Deliverable:** Public, reproducible research artifact

---

## 4. Milestones and Timeline

### Milestone 1 — Project Setup and Baseline Lock (Weeks 1–2)
- Repository structure finalized  
- Baseline COMSOL model validated  
- GitHub Pages skeleton published  

**Exit Criterion:** Baseline model runs on a clean system.

---

### Milestone 2 — Transport-Limited Analysis (Weeks 3–5)
- Cortex/medulla uptake delay quantified  
- Parametric diffusion sweeps completed  
- Biological interpretation documented  

**Exit Criterion:** Transport limitations clearly demonstrated.

---

### Milestone 3 — Electrical Response Integration (Weeks 6–8)
- GFET current response implemented  
- Detection threshold estimated  
- Noise assumptions justified  

**Exit Criterion:** Molecular-to-electrical signal chain complete.

---

### Milestone 4 — Sensitivity and Design Insights (Weeks 9–11)
- Sensitivity ranking finalized  
- Design trade-offs articulated  
- Engineering implications summarized  

**Exit Criterion:** Non-trivial design conclusions extracted.

---

### Milestone 5 — Finalization and Submission (Weeks 12–14)
- Final report submitted  
- Final presentation prepared  
- Repository cleaned and archived  

**Exit Criterion:** Professional, defensible final submission.

---

## 5. GitHub Issue Management Strategy

Issues are used as **atomic research tasks**, not generic TODOs.

### Example Issue Categories
- **Modeling:**  
  - `TDS-01: Implement heterogeneous diffusion domains`  
  - `TDS-02: Validate inlet boundary conditions`  

- **Electronics:**  
  - `GFET-01: Define Δn → ΔI_DS mapping`  
  - `GFET-02: Estimate noise floor`  

- **Analysis:**  
  - `AN-01: Cortex vs. medulla time-to-threshold metric`  
  - `AN-02: Sensitivity ranking methodology`  

- **Documentation:**  
  - `DOC-01: Reproducibility instructions`  
  - `DOC-02: GitHub Pages figures`  

Each issue includes:
- Clear definition of done  
- Assigned milestone  
- References or assumptions  

---

## 6. Success Criteria

The project is considered successful if:

- All results are reproducible from the repository  
- Every plot has a clear physical interpretation  
- Modeling assumptions are explicit and justified  
- GitHub repository reflects research-grade organization  
- The system-level bottleneck is clearly identified  

---

## 7. Risk Analysis

| Risk | Impact | Mitigation |
|---|---|---|
| COMSOL solver instability | Medium | Incremental model locking |
| Over-complex modeling | High | Physics-first minimalism |
| Time compression near finals | High | Front-loaded modeling |
| Weak engineering insight | Critical | Mandatory interpretation sections |

---

**Note:**  
This project prioritizes **insight, rigor, and reproducibility** over raw numerical complexity. The primary contribution is understanding *why* performance limits arise, not merely observing them.