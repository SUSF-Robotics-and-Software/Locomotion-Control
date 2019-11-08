from LocomotionControl.loco_ctrl import LocoCtrl

# Test the LocoCtrl module based on the test parameters
def test_get_act_telem():
    # Initialise module
    loco_ctrl = LocoCtrl()

    # get_act_telem returns a named tuple with both the actuator telemetry and 
    # the status report, so we want to ensure we save both
    act_data = loco_ctrl.get_act_telem()

    print(act_data.act_telem)
    print(act_data.status_rpt)
    

# Run test if and only if this file is called directly
if __name__ == '__main__':
    test_get_act_telem()