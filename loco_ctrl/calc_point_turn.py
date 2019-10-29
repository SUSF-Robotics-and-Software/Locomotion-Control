from collections import namedtuple
from .act_dems import ActDems

# Calculate Point Turn Demands
#
#   Calculate demands for the point turn manoeuvre.
def calc_point_turn(self, mnvr_params):

    # Initialise actuator demands to stopping and empty status report
    act_dems = ActDems()
    status_rpt = {}

    # TODO: Your algorithm here

    # Construct namedtuple result
    result = namedtuple('SkidSteerData', ['act_dems', 'status_rpt'])

    return result(act_dems, status_rpt)