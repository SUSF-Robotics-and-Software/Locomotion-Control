import os
import json
from collections import namedtuple

# Locomotion Control Module
#
#   Perform locomotion control, converting from high level manoeuvre commands 
#   into lower level actuator commands.
#
#   For detailed specification see docs/spec.md
#
#   Public functions:
#       LocoCtrl.get_act_telem():
#           Retrieve actuator telemetry for use in additional data processing.
#           See function definition file for more information.
#
#       LocoCtrl.do_mnvr_ctrl(mnvr_cmd):
#           Command the actuators to perform the given manoeuvre. mnvr_cmd must
#           be valid as per the module spec. See function definition file for 
#           more information.
class LocoCtrl:

    # Import public functions
    from .get_act_telem import get_act_telem
    from .do_mnvr_ctrl import do_mnvr_ctrl

    # Module Initialisation Function
    #
    #   Sets up initial state of the module by loading parameters.
    def __init__(self):
        # Get the path to this file, since relative imports are messed up and 
        # are relative to the executing script's path, not the path of this file
        loco_ctrl_dir = os.path.dirname(os.path.realpath(__file__))

        # Load the parameter file to a string
        with open(os.path.join(loco_ctrl_dir, '../params/loco_ctrl.json'), 
                mode='r') as params_file:
            params_string = params_file.read()

        # Parse the JSON string into a named tuple (object), uses trick given at
        # https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object
        self.params = json.loads(params_string, 
            object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))