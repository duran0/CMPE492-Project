---
title: In-body Antigen Detection via Antibodies on a Transistor (HER2–GFET)
---

# In-body Antigen Detection via Antibodies on a Transistor (HER2–GFET)

**Course:** CMPE 492 – Senior Design Project II  
**Student:** Duran Kaan Altın  
**Advisors:** Prof. Tuna Tuğcu, Prof. Kutlu Ülgen  
**Institution:** Boğaziçi University

---

## Abstract
Early cancer diagnostics depend on detecting tumor-associated biomarkers before macroscopic disease progression. This project investigates a **graphene field-effect transistor (GFET)** biosensor concept for **label-free detection of HER2**, a clinically important breast cancer biomarker. The central hypothesis is that detection performance is not defined by transistor sensitivity alone: **antigen transport inside tissue (and lymph-node-like structures) can dominate response time and availability at the sensing region**. We develop a **reproducible multiphysics simulation framework** that combines (i) diffusion-driven transport in a compartmentalized lymph-node-inspired geometry and (ii) a GFET signal transduction model mapping surface charge modulation to measurable drain–source current shifts. The deliverable is a research-grade repository with parameterized models, sensitivity analysis, and design insights.

---

## Motivation
- **HER2** overexpression is associated with aggressive breast cancer subtypes and is used clinically for prognosis and therapy selection.  
- Standard clinical assays (e.g., ELISA/IHC) are powerful but **not designed for continuous in-body monitoring**.  
- GFET biosensors offer a path to **rapid, label-free electrical readout**, but practical sensing can be **transport-limited** (the biomarker must physically reach the sensing surface).

**Engineering takeaway:** even a highly sensitive GFET can respond slowly if biomarker transport is delayed by tissue heterogeneity.

---

## What We Built
### 1) Lymph-node-inspired 3D transport model (COMSOL)
We model diffusion-only transport in a simplified lymph-node-like geometry:
- Outer domain: **cortex**
- Inner domain: **medulla**
- Inlet boundaries: model antigen inflow
- Heterogeneous diffusivity: **D_cortex ≠ D_medulla**

**Key goal:** quantify cortex vs. medulla exposure delay and identify transport bottlenecks.

### 2) GFET electrical response module
We map bound/near-surface charge modulation to GFET current response:
- Antigen–antibody binding perturbs local electrostatics near graphene
- Effective carrier density shift → **ΔI_DS** measurable at the readout

**Key goal:** link *molecules → electrical signal* and estimate detectability under realistic assumptions.

### 3) System-level sensitivity & bottleneck analysis
We compare:
- **transport-limited regime:** response dominated by diffusion/geometry
- **electronics-limited regime:** response dominated by device sensitivity/noise

**Key goal:** produce non-trivial design guidance (what matters most, what doesn’t).

---

## Key Results (Current Snapshot)
### Cortex–Medulla Uptake Delay
- Volume-averaged concentration rises rapidly in the cortex.
- Medulla uptake is delayed due to lower effective diffusivity.
- The delay persists even at longer observation times.

### Parametric Sweep: Diffusivity Ratio
We sweep the diffusivity ratio:

\[
r = \frac{D_{\text{medulla}}}{D_{\text{cortex}}} \in [0.1, 1]
\]

**Observation:** decreasing \( r \) increases cortex–medulla uptake delay, strengthening the conclusion that **internal heterogeneity imposes a fundamental transport limit** on biosensor response time.

---
