from .. import LocoCtrl

# Test the LocoCtrl module based on the test parameters
def test_init():
    locoCtrl = LocoCtrl()

    print(locoCtrl.params)

# Run test if and only if this file is called directly
if __name__ == '__main__':
    test_init()