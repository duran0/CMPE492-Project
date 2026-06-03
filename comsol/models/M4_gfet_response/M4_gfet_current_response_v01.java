import com.comsol.model.Model;
import com.comsol.model.util.ModelUtil;

public class M4_gfet_current_response_v01 {
  public static Model run() {
    Model model = ModelUtil.create("Model");
    model.label("M4_gfet_current_response_v01.mph");
    model.modelNode().create("comp1");

    model.param().set("W_ch_m", "20e-6", "GFET channel width in meters");
    model.param().set("L_ch_m", "2e-6", "GFET channel length in meters");
    model.param().set("mobility_si", "0.1", "Carrier mobility");
    model.param().set("Vds_si", "0.05", "Drain-source voltage");
    model.param().set("Aeff_si", "4e-11", "Effective sensing area");
    model.param().set("alpha_base", "0.01", "Baseline coupling efficiency");
    model.param().set("noise_floor_A", "10e-12", "Baseline current noise floor");

    return model;
  }

  public static void main(String[] args) {
    run();
  }
}
