from enum import Enum

# Manoeuvre Type Enumeration
#   Defines manoeuvre type as an enum so it can be used like MnvrType.ACKERMAN
class MnvrType(Enum):
    NONE        = 0
    SKID_STEER  = 1
    ACKERMAN    = 2
    POINT_TURN  = 3

# Number of Drive Axes
#   Defined for Phobos only, there are 6 drive axes, all of which can be 
#   addressed.
NUM_DRV_AXES = 6

# Number of Steer Axes
#   Defined for Phobos only, there are 4 steer axes, but we set 6 available so
#   that they can easily be indexed in combination with the drive axes, and to 
#   allow software to easily be modified in case additional steer axes are added.
NUM_STR_AXES = 6