from typing import List
from CommsAndCommand.command import command_primitive


class ActDems(command_primitive):
    """
    Actuator Demands
    
        Defines the demands which shall be issued to each actuator
    
        TODO - Shall be initialised as stopping demands (will result in no
        motion):
    """

    def __init__(self):

        self.name = 'ActDems'

        # Drive Demand
        #   Unit:  PWM width
        #   Frame: N/A
        self.drv_dem_pwm: List[float] = 0

        # Steer Demand
        #   Unit:  PWM width
        #   Frame: N/A
        self.str_dem_pwm: List[float] = 0
