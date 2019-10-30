from collections import namedtuple

# Get Actuator Telemetry
#
#       __NOT YET IMPLEMENTED__
#
#   Retrieve processed actuator telemetry from the motors.
#
#   Inputs:
#       self: LocoCtrl module state
#
#   Outputs:
#       `namedtuple` with two members
#       act_telem: Actuator telemetry (Contents as per module spec)
#       status_rpt: Status report dictionary, populated with error flags when
#           necessary.
def get_act_telem(self):
    raise Exception('Not yet implemented')

    result = namedtuple('ActData', ['act_telem', 'status_rpt'])

    return result(None, None)