import com.comsol.model.Model;
import com.comsol.model.util.ModelUtil;

public class M1_0D_HER2_binding_v01 {
  public static Model run() {
    Model model = ModelUtil.create("Model");
    model.label("M1_0D_HER2_binding_v01.mph");
    model.modelNode().create("comp1");

    model.param().set("C_pM", "10", "Baseline HER2 concentration in pM");
    model.param().set("Kd_pM", "10", "Dissociation constant in pM");
    model.param().set("kf", "1e7", "Forward binding rate constant in 1/(M*s)");
    model.param().set("kr", "1e-4", "Reverse binding rate constant in 1/s, kr = kf*Kd");
    model.param().set("theta_eq", "C_pM/(Kd_pM+C_pM)", "Equilibrium Langmuir occupancy expression");
    model.param().set("tmax_s", "6000", "Maximum simulated time in seconds");

    return model;
  }

  public static void main(String[] args) {
    run();
  }
}
