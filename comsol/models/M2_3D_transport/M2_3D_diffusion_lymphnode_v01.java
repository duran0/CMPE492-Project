import com.comsol.model.Model;
import com.comsol.model.util.ModelUtil;

public class M2_3D_diffusion_lymphnode_v01 {
  public static Model run() {
    Model model = ModelUtil.create("Model");
    model.label("M2_3D_diffusion_lymphnode_v01.mph");

    model.param().set("R_cortex_um", "500", "Outer lymph-node-inspired radius in um");
    model.param().set("R_medulla_um", "250", "Inner medulla radius in um");
    model.param().set("Dcortex", "8e-11", "Cortex diffusion coefficient in m^2/s");
    model.param().set("r", "0.5", "Dmedulla/Dcortex diffusivity ratio");
    model.param().set("Dmedulla", "r*Dcortex", "Medulla diffusion coefficient");
    model.param().set("c0_mol_m3", "1e-8", "Fixed inlet HER2 concentration in mol/m^3");
    model.param().set("tmax_s", "6000", "Maximum simulated time in seconds");

    model.component().create("comp1", true);
    model.component("comp1").geom().create("geom1", 3);
    model.component("comp1").geom("geom1").lengthUnit("um");
    model.component("comp1").geom("geom1").create("cortex", "Sphere");
    model.component("comp1").geom("geom1").feature("cortex").label("domain_cortex_outer_sphere");
    model.component("comp1").geom("geom1").feature("cortex").set("r", "500");
    model.component("comp1").geom("geom1").create("medulla", "Sphere");
    model.component("comp1").geom("geom1").feature("medulla").label("domain_medulla_inner_sphere");
    model.component("comp1").geom("geom1").feature("medulla").set("r", "250");
    model.component("comp1").geom("geom1").run();
    model.component("comp1").mesh().create("mesh1");
    model.component("comp1").mesh("mesh1").autoMeshSize(4);
    model.component("comp1").mesh("mesh1").run();

    model.component("comp1").selection().create("domain_cortex", "Explicit");
    model.component("comp1").selection("domain_cortex").label("domain_cortex");
    model.component("comp1").selection().create("domain_medulla", "Explicit");
    model.component("comp1").selection("domain_medulla").label("domain_medulla");
    model.component("comp1").selection().create("boundary_inlet", "Explicit");
    model.component("comp1").selection("boundary_inlet").label("boundary_inlet");
    model.component("comp1").selection().create("boundary_wall_no_flux", "Explicit");
    model.component("comp1").selection("boundary_wall_no_flux").label("boundary_wall_no_flux");
    model.component("comp1").selection().create("boundary_sensor_full", "Explicit");
    model.component("comp1").selection("boundary_sensor_full").label("boundary_sensor_full");
    model.component("comp1").selection().create("boundary_sensor_local", "Explicit");
    model.component("comp1").selection("boundary_sensor_local").label("boundary_sensor_local");

    model.component("comp1").physics().create("tds", "DilutedSpecies", "geom1");
    model.component("comp1").physics("tds").label("Transport of Diluted Species - HER2");
    model.component("comp1").physics("tds").field("concentration").field("c");
    model.component("comp1").physics("tds").field("concentration").component(new String[]{"c"});
    model.component("comp1").physics("tds").feature("cdm1").set("D_c", "if(sqrt(x^2+y^2+z^2)<R_medulla_um*1e-6,Dmedulla,Dcortex)");
    model.component("comp1").physics("tds").feature("init1").set("initc", "0");
    model.component("comp1").physics("tds").create("conc1", "Concentration", 2);
    model.component("comp1").physics("tds").feature("conc1").label("Fixed HER2 source concentration");
    model.component("comp1").physics("tds").feature("conc1").selection().all();
    model.component("comp1").physics("tds").feature("conc1").set("c0", "c0_mol_m3");

    model.study().create("std1");
    model.study("std1").create("time", "Transient");
    model.study("std1").feature("time").set("tlist", "0 100 500 1000 2000 4000 6000");

    return model;
  }

  public static void main(String[] args) {
    run();
  }
}
