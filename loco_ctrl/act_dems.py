from typing import List
from .CommsAndCommand.command import command_primative

class ActDems(command_primative):
    """
    Actuator Demands
    
        Defines the demands which shall be issued to each actuator
    
        Shall be initialised as stopping demands (will result in no motion): TODO
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
