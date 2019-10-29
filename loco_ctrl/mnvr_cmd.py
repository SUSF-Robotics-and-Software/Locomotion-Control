from dataclasses import dataclass
from typing import Dict
from .constants import MnvrType

# Manoeuvre Command 
#
#   Encapsulates a single manoeuvre command, identified by an ID (MnvrType.X) 
#   and associated parameters.
@dataclass
class MnvrCmd:
    # Manoeuvre ID
    #
    #   The type of manoeuvre to perform
    mnvr_id: MnvrType

    # Manoeuvre Parameters
    #
    #   Dictionary of parameters for the given manoeuvre.
    mnvr_params: Dict[str, float]