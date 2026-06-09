# 0:00-0:30 Problem and Motivation

This project studies a simulation workflow for HER2 antigen detection using an antibody-functionalized graphene field-effect transistor, or GFET. HER2 is a clinically important biomarker, but this work does not claim clinical detection or device validation. The goal is narrower: calculate whether HER2 transport, surface binding, and transistor response could plausibly produce a measurable signal under modeled assumptions.

# 0:30-1:15 GFET Sensing Principle

The sensing concept is that HER2 molecules bind to antibodies immobilized near the graphene channel. Bound molecules change the local electrostatic environment, which changes the effective carrier density and produces a drain-source current shift, Delta I DS. The model separates this into three steps: first, antigen reaches the sensor surface; second, HER2 binds to the antibody layer; third, the bound molecule count is converted into a GFET current response. This separation is important because a strong transistor response is not useful if antigen transport or electrostatic coupling fails.

# 1:15-2:15 COMSOL Transport and Lymph-Node Flow Model

The transport model starts with M2, a diffusion-only Transport of Diluted Species baseline in a simplified cortex and medulla geometry. The extension, M2B, adds a partially anatomical lymph-node-inspired convection-diffusion model. It includes afferent inlet regions, a hilum-side efferent outlet, local and full sensor regions, and a prescribed velocity field coupled to HER2 transport.

The M2B verification checks showed that the zero-flow case behaves like diffusion-only transport, and increasing inlet velocity changes sensor exposure. For the reference case at 10 pM HER2 and `v_in = 5e-7 m/s`, the sensor concentration at 6000 seconds increases from 4.98 pM under diffusion-only transport to 8.73 pM under directional flow. The time to 50 percent exposure decreases from about 6038 seconds to about 1839 seconds.

# 2:15-3:15 Surface Binding and Current Response

After transport, surface binding is calculated using Langmuir-style occupancy. The local surface concentration determines occupancy, surface-bound density, and bound HER2 molecule count. That bound molecule count is then converted to a current response using the analytical GFET relation.

The placement sweep checks whether the sensor position matters. Three placements were evaluated: subcapsular or cortical, cortex-medulla transition, and medulla or hilum-side. In the model, the subcapsular/cortical placement gives the fastest and strongest response under reference flow. This means sensor placement is not a cosmetic detail; it changes exposure time and current response.

# 3:15-4:20 Results and Scientific Conclusion

The final experiment campaign has five main results.

First, directional flow improves HER2 exposure at the sensor compared with diffusion-only transport.

Second, placement matters. A sensor closer to favorable transport paths responds faster and more strongly in the modeled sweep.

Third, electrical detectability is conditional. In the detectability envelope, 99 parameter combinations are detectable, but 36 fail. The best reported M4 LOD case is approximately 0.78 pM under the alpha = 0.03 and 10 pA noise assumption. Detection is favored by higher HER2 concentration, stronger coupling, lower noise, and tighter binding affinity. Weak coupling, high noise, or poor affinity can make the signal fall below threshold.

Fourth, Debye screening is the strongest feasibility barrier. With PBS-like physiological screening and effective charge distance of at least 5 nanometers, zero out of 60 screened cases remain detectable. That is the main negative result.

Fifth, Experiment E converts that negative screening result into design requirements. For example, with Kd = 10 pM, 10 pA noise, and PBS-like screening at 1 nanometer, required alpha0 is about 0.0326 at 1 pM HER2 and about 0.00561 at 10 pM HER2.

The main scientific conclusion is: Directional flow and sensor placement improve HER2 exposure, but electrostatic screening and electronics noise dominate practical GFET detectability.

# 4:20-5:00 Limitations and Future Work

This project is simulation-only. It does not prove clinical feasibility, it does not build an in-body detector, and it does not show sub-pM detection in all cases. The flow model is partially anatomical and uses a prescribed velocity field rather than a validated Darcy-flow pressure solution. The GFET response is analytical, and Debye lengths are feasibility assumptions.

Experiment E moves part of that future work into the project by calculating design requirements for receptor distance, coupling efficiency, Debye screening, and electronics noise. Future work should experimentally validate these design requirements, replace prescribed flow with validated Darcy/Brinkman flow, automate direct COMSOL field exports, and test surface chemistries/electronics that can achieve the required distance, coupling, and noise values.
