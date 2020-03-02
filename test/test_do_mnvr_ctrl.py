import hjson
import os

from LocomotionControl.loco_ctrl import LocoCtrl
from LocomotionControl.loco_ctrl.mnvr_cmd import MnvrCmd, MnvrType

# Test the LocoCtrl module based on the test parameters
def test_do_mnvr_ctrl():
    # Initialise module
    loco_ctrl = LocoCtrl()

    # Get the directory of this file, since python will attempt to import 
    # relative to the executing script directory.
    test_dir = os.path.dirname(os.path.realpath(__file__))

    # Load test commands from the hjson file
    with open(os.path.join(test_dir, 'mnvr_cmds.hjson'), mode='r') as cmds_file:
        test_cmds = hjson.loads(cmds_file.read())

    # Test each command
    for cmd in test_cmds:

        # Parse the command
        mnvr_cmd = MnvrCmd.from_structure(cmd)

        # Log the command issued, by printing the command type, followed the 
        # parameters passed in, or 'No parameters' if none exist
        print(f'  {mnvr_cmd.mnvr_id}:')
        if mnvr_cmd.mnvr_params:
            for (param_name, param_value) in mnvr_cmd.mnvr_params.items():
                print(f'    {param_name}: {param_value}')
        else:
            print('    No parameters')

        # Get the response from loco_ctrl
        status_rpt = loco_ctrl.do_mnvr_ctrl(mnvr_cmd)

        # Print the output, this will print either the keys and values in the 
        # status report dictionary, or 'Empty' if there's nothing there 
        # (shouldn't happen)
        print('  status_rpt:')
        if status_rpt:
            for (key, val) in status_rpt.items():
                print(f'    {key}: {val}')
        else:
            print('    Empty')
        
        print()
    

# Run test if and only if this file is called directly
if __name__ == '__main__':
    test_do_mnvr_ctrl()