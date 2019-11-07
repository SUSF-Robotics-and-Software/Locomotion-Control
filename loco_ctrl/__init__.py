import os
from sparam import load_params
from collections import namedtuple

class LocoCtrl:
    """
    Locomotion Control Module
    
      Perform locomotion control, converting from high level manoeuvre commands 
      into lower level actuator commands.
    
      For detailed specification see docs/spec.md
    
      Public functions:
          LocoCtrl.get_act_telem():
              Retrieve actuator telemetry for use in additional data processing.
              See function definition file for more information.
    
          LocoCtrl.do_mnvr_ctrl(mnvr_cmd):
              Command the actuators to perform the given manoeuvre. mnvr_cmd must
              be valid as per the module spec. See function definition file for 
              more information.
    
      Usage:
          LocoCtrl.get_act_telem shall be called in the sensing phase of the 
          software cycle and must be called before LocoCtrl.do_mnvr_ctrl.
    """
    
    # Import public functions
    from .get_act_telem import get_act_telem
    from .do_mnvr_ctrl import do_mnvr_ctrl

    # Import public types
    from .mnvr_cmd import MnvrCmd, MnvrType

    # Module Initialisation Function
    #
    #   Sets up initial state of the module by loading parameters.
    def __init__(self):

        # Get the path to this file, since relative imports are messed up and 
        # are relative to the executing script's path, not the path of this file
        loco_ctrl_dir = os.path.dirname(os.path.realpath(__file__))

        # Load the parameter file using sparam
        self.params = load_params.load_params_from_hjson(
            os.path.join(loco_ctrl_dir, '../params/loco_ctrl.hjson'))