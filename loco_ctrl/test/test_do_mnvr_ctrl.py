from .. import LocoCtrl
from ..mnvr_cmd import MnvrCmd, MnvrType

# Test the LocoCtrl module based on the test parameters
def test_do_mnvr_ctrl():
    # Initialise module
    loco_ctrl = LocoCtrl()

    # Construct a manouvre command (type of NONE, which has no parameters)
    mnvr_cmd = MnvrCmd(MnvrType.NONE, {})

    # do_mnvr_ctrl returns a status report only
    status_rpt = loco_ctrl.do_mnvr_ctrl(mnvr_cmd)

    print(status_rpt)
    

# Run test if and only if this file is called directly
if __name__ == '__main__':
    test_do_mnvr_ctrl()