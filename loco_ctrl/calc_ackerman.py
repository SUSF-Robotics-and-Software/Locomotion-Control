from collections import namedtuple
from .act_dems import ActDems

# Calculate Ackerman Demands
#
#   Calculate demands for the ackerman manoeuvre.
def calc_ackerman(self, mnvr_params):

    # Initialise actuator demands to stopping and empty status report
    act_dems = ActDems()
    status_rpt = {}

    # TODO: Your algorithm here

    # Construct namedtuple result
    result = namedtuple('AckermanData', ['act_dems', 'status_rpt'])

    return result(act_dems, status_rpt)