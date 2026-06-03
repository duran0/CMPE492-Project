import com.comsol.model.Model;
import com.comsol.model.util.ModelUtil;

public class M3_surface_binding_local_sensor_v01 {
  public static Model run() {
    Model model = ModelUtil.create("Model");
    model.label("M3_surface_binding_local_sensor_v01.mph");

    model.param().set("Kd_pM", "10", "Dissociation constant in pM");
    model.param().set("kf", "1e7", "Forward binding rate constant in 1/(M*s)");
    model.param().set("kr", "1e-4", "Reverse binding rate constant in 1/s");
    model.param().set("Gamma_max", "8.30e-12", "Effective antibody site density in mol/m^2");
    model.param().set("Aeff", "4e-11", "Local GFET sensing area in m^2");
    model.param().set("c_surface_pM", "10", "Representative surface HER2 concentration in pM");
    model.param().set("Gamma", "Gamma_max*c_surface_pM/(Kd_pM+c_surface_pM)", "Equilibrium surface binding expression");

    model.component().create("comp1", true);
    model.component("comp1").geom().create("geom1", 3);
    model.component("comp1").geom("geom1").lengthUnit("um");
    model.component("comp1").geom("geom1").create("sensor", "Block");
    model.component("comp1").geom("geom1").feature("sensor").label("local_gfet_sensor_placeholder");
    model.component("comp1").geom("geom1").feature("sensor").set("size", new String[]{"20", "2", "1"});
    model.component("comp1").geom("geom1").run();
    model.component("comp1").selection().create("boundary_sensor_local", "Explicit");
    model.component("comp1").selection("boundary_sensor_local").label("boundary_sensor_local");

    return model;
  }

  public static void main(String[] args) {
    run();
  }
}
