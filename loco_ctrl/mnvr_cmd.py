from typing import Dict
from CommsAndCommand.command import command_primitive
from .constants import MnvrType

class MnvrCmd(command_primitive):
    """
    Manoeuvre Command 

    Encapsulates a single manoeuvre command, identified by an ID (MnvrType.X) 
    and associated parameters.
    """
    
    def __init__(self):

        self.name = 'MnvrCmd'

        # Manoeuvre ID
        #
        #   The type of manoeuvre to perform, one of MnvrType.X.
        self.mnvr_id: MnvrType

        # Manoeuvre Parameters
        #
        #   Dictionary of parameters for the given manoeuvre.
        self.mnvr_params: Dict[str, float]