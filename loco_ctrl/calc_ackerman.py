from collections import namedtuple
from .act_dems import ActDems

def calc_ackerman(self, mnvr_params):
    """
    Calculate Ackerman Demands
    
      Calculate demands for the ackerman manoeuvre.
    
      Inputs:
          self: LocoCtrl module state
          mnvr_params: Dictionary of parameters for the manoeuvre, see docs/spec
    
      Outputs:
          `namedtuple` of two members:
          act_dems: Actuator demands, an instance of ActDems
          status_rpt: Status report dictionary, to be populated with error flags
              when necessary.
    """

    # Initialise actuator demands to stopping and empty status report
    act_dems = ActDems()
    status_rpt = {}

    # TODO: Your algorithm here

    # Construct namedtuple result
    result = namedtuple('AckermanData', ['act_dems', 'status_rpt'])

    return result(act_dems, status_rpt)