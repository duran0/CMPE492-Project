import com.comsol.model.Model;
import com.comsol.model.util.ModelUtil;

public class M2B_anatomical_flow_lymphnode_v01 {
  public static Model run() {
    Model model = ModelUtil.create("Model");
    model.label("M2B_anatomical_flow_lymphnode_v01.mph");

    model.param().set("R_node_um", "500", "Simplified lymph-node-inspired outer radius");
    model.param().set("R_sinus_inner_um", "430", "Approximate inner boundary of subcapsular sinus");
    model.param().set("R_medulla_um", "250", "Simplified medulla radius");
    model.param().set("patch_radius_um", "40", "Afferent inlet marker radius");
    model.param().set("sensor_radius_um", "30", "Local sensor marker radius");
    model.param().set("Dcortex", "8e-11", "Cortex diffusion coefficient in m^2/s");
    model.param().set("Dsinus", "1.2e-10", "Subcapsular sinus diffusion coefficient in m^2/s");
    model.param().set("r", "0.5", "Dmedulla/Dcortex diffusivity ratio");
    model.param().set("Dmedulla", "r*Dcortex", "Medulla diffusion coefficient");
    model.param().set("v_in", "5e-7", "Prescribed afferent inlet velocity in m/s");
    model.param().set("v_in_low", "1e-7", "Low prescribed inlet velocity in m/s");
    model.param().set("v_in_ref", "5e-7", "Reference prescribed inlet velocity in m/s");
    model.param().set("v_in_high", "1e-6", "High prescribed inlet velocity in m/s");
    model.param().set("c0_mol_m3", "1e-8", "HER2 inlet concentration for 10 pM");
    model.param().set("tmax_s", "6000", "Maximum simulated time in seconds");

    model.component().create("comp1", true);
    model.component("comp1").geom().create("geom1", 3);
    model.component("comp1").geom("geom1").lengthUnit("um");

    model.component("comp1").geom("geom1").create("capsule", "Sphere");
    model.component("comp1").geom("geom1").feature("capsule").label("domain_subcapsular_sinus_and_cortex_outer_node");
    model.component("comp1").geom("geom1").feature("capsule").set("r", "R_node_um");

    model.component("comp1").geom("geom1").create("sinus_inner", "Sphere");
    model.component("comp1").geom("geom1").feature("sinus_inner").label("domain_cortex_inner_sinus_reference");
    model.component("comp1").geom("geom1").feature("sinus_inner").set("r", "R_sinus_inner_um");

    model.component("comp1").geom("geom1").create("medulla", "Sphere");
    model.component("comp1").geom("geom1").feature("medulla").label("domain_medulla");
    model.component("comp1").geom("geom1").feature("medulla").set("r", "R_medulla_um");

    model.component("comp1").geom("geom1").create("aff1", "Sphere");
    model.component("comp1").geom("geom1").feature("aff1").label("boundary_afferent_inlet_1_marker");
    model.component("comp1").geom("geom1").feature("aff1").set("r", "patch_radius_um");
    model.component("comp1").geom("geom1").feature("aff1").set("pos", new String[]{"0", "470", "120"});

    model.component("comp1").geom("geom1").create("aff2", "Sphere");
    model.component("comp1").geom("geom1").feature("aff2").label("boundary_afferent_inlet_2_marker");
    model.component("comp1").geom("geom1").feature("aff2").set("r", "patch_radius_um");
    model.component("comp1").geom("geom1").feature("aff2").set("pos", new String[]{"260", "390", "90"});

    model.component("comp1").geom("geom1").create("aff3", "Sphere");
    model.component("comp1").geom("geom1").feature("aff3").label("boundary_afferent_inlet_3_marker");
    model.component("comp1").geom("geom1").feature("aff3").set("r", "patch_radius_um");
    model.component("comp1").geom("geom1").feature("aff3").set("pos", new String[]{"-260", "390", "90"});

    model.component("comp1").geom("geom1").create("aff4", "Sphere");
    model.component("comp1").geom("geom1").feature("aff4").label("boundary_afferent_inlet_4_marker");
    model.component("comp1").geom("geom1").feature("aff4").set("r", "patch_radius_um");
    model.component("comp1").geom("geom1").feature("aff4").set("pos", new String[]{"0", "360", "-250"});

    model.component("comp1").geom("geom1").create("efferent", "Sphere");
    model.component("comp1").geom("geom1").feature("efferent").label("boundary_efferent_outlet_marker");
    model.component("comp1").geom("geom1").feature("efferent").set("r", "55");
    model.component("comp1").geom("geom1").feature("efferent").set("pos", new String[]{"0", "-475", "0"});

    model.component("comp1").geom("geom1").create("sensor_local", "Sphere");
    model.component("comp1").geom("geom1").feature("sensor_local").label("boundary_sensor_local_marker");
    model.component("comp1").geom("geom1").feature("sensor_local").set("r", "sensor_radius_um");
    model.component("comp1").geom("geom1").feature("sensor_local").set("pos", new String[]{"0", "-225", "120"});

    model.component("comp1").geom("geom1").run();

    model.component("comp1").selection().create("domain_subcapsular_sinus", "Explicit");
    model.component("comp1").selection("domain_subcapsular_sinus").label("domain_subcapsular_sinus");
    model.component("comp1").selection().create("domain_cortex", "Explicit");
    model.component("comp1").selection("domain_cortex").label("domain_cortex");
    model.component("comp1").selection().create("domain_medulla", "Explicit");
    model.component("comp1").selection("domain_medulla").label("domain_medulla");
    model.component("comp1").selection().create("boundary_afferent_inlet_1", "Explicit");
    model.component("comp1").selection("boundary_afferent_inlet_1").label("boundary_afferent_inlet_1");
    model.component("comp1").selection().create("boundary_afferent_inlet_2", "Explicit");
    model.component("comp1").selection("boundary_afferent_inlet_2").label("boundary_afferent_inlet_2");
    model.component("comp1").selection().create("boundary_afferent_inlet_3", "Explicit");
    model.component("comp1").selection("boundary_afferent_inlet_3").label("boundary_afferent_inlet_3");
    model.component("comp1").selection().create("boundary_afferent_inlet_4", "Explicit");
    model.component("comp1").selection("boundary_afferent_inlet_4").label("boundary_afferent_inlet_4");
    model.component("comp1").selection().create("boundary_efferent_outlet", "Explicit");
    model.component("comp1").selection("boundary_efferent_outlet").label("boundary_efferent_outlet");
    model.component("comp1").selection().create("boundary_capsule_no_flow", "Explicit");
    model.component("comp1").selection("boundary_capsule_no_flow").label("boundary_capsule_no_flow");
    model.component("comp1").selection().create("boundary_sensor_local", "Explicit");
    model.component("comp1").selection("boundary_sensor_local").label("boundary_sensor_local");
    model.component("comp1").selection().create("boundary_sensor_full", "Explicit");
    model.component("comp1").selection("boundary_sensor_full").label("boundary_sensor_full");

    model.component("comp1").variable().create("var1");
    model.component("comp1").variable("var1").label("Prescribed porous-flow velocity field");
    model.component("comp1").variable("var1").set("r_node", "sqrt(x^2+y^2+z^2)");
    model.component("comp1").variable("var1").set("D_region", "if(r_node>R_sinus_inner_um*1e-6,Dsinus,if(r_node<R_medulla_um*1e-6,Dmedulla,Dcortex))");
    model.component("comp1").variable("var1").set("u_flow", "-0.15*v_in*x/(R_node_um*1e-6)");
    model.component("comp1").variable("var1").set("v_flow", "-v_in*(0.25+0.75*(y+R_node_um*1e-6)/(2*R_node_um*1e-6))");
    model.component("comp1").variable("var1").set("w_flow", "-0.10*v_in*z/(R_node_um*1e-6)");
    model.component("comp1").variable("var1").set("p_proxy", "10[Pa]*(y+R_node_um*1e-6)/(2*R_node_um*1e-6)");

    model.component("comp1").physics().create("tds", "DilutedSpecies", "geom1");
    model.component("comp1").physics("tds").label("Convection-diffusion scaffold for HER2");
    model.component("comp1").physics("tds").field("concentration").field("c");
    model.component("comp1").physics("tds").field("concentration").component(new String[]{"c"});
    model.component("comp1").physics("tds").feature("cdm1").set("D_c", "D_region");
    model.component("comp1").physics("tds").feature("init1").set("initc", "0");

    model.component("comp1").mesh().create("mesh1");
    model.component("comp1").mesh("mesh1").autoMeshSize(4);
    model.component("comp1").mesh("mesh1").run();

    model.study().create("std1");
    model.study("std1").create("time", "Transient");
    model.study("std1").feature("time").set("tlist", "0 100 500 1000 2000 4000 6000");

    return model;
  }

  public static void main(String[] args) {
    run();
  }
}
