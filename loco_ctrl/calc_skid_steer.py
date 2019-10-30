from collections import namedtuple
from .act_dems import ActDems

# Calculate Skid Steer Demands
#
#   Calculate demands for the skid steer manoeuvre.
#
#   Inputs:
#       self: LocoCtrl module state
#       mnvr_params: Dictionary of parameters for the manoeuvre, see docs/spec
#
#   Outputs:
#       `namedtuple` of two members:
#       act_dems: Actuator demands, an instance of ActDems
#       status_rpt: Status report dictionary, to be populated with error flags
#           when necessary.
def calc_skid_steer(self, mnvr_params):

    # Initialise actuator demands to stopping and empty status report
    act_dems = ActDems()
    status_rpt = {}

    # TODO: Your algorithm here

    # Construct namedtuple result
    result = namedtuple('SkidSteerData', ['act_dems', 'status_rpt'])

    return result(act_dems, status_rpt)