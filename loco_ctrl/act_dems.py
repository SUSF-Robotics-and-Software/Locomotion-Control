from dataclasses import dataclass
from typing import List

# Actuator Demands
#
#   Defines the demands which shall be issued to each actuator
#
#   Shall be initialised as stopping demands (will result in no motion): TODO
#
@dataclass
class ActDems:
    # Drive Demand
    #   Unit:  PWM width
    #   Frame: N/A
    drv_dem_pwm: List[float] = 0

    # Steer Demand
    #   Unit:  PWM width
    #   Frame: N/A
    str_dem_pwm: List[float] = 0
