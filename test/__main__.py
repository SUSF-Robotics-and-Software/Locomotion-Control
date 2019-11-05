import datetime

from .test_init import test_init
from .test_do_mnvr_ctrl import test_do_mnvr_ctrl

def run_all_tests():
    print('\n---- Locomotion Control Module Tests ----')
    print(str(datetime.datetime.now()))

    print('\nInit:')
    test_init()

    #print('\nGet Actuator Telemetry:')
    #test_get_act_telem()

    print('\nDo Manoeuvre Control:')
    test_do_mnvr_ctrl()

# Run all tests if this file is being executed
if __name__ == '__main__':
    run_all_tests()