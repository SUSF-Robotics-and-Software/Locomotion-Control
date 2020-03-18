from collections import namedtuple
from .act_dems import ActDems
from math import pi, tan, isclose, sqrt 


status_rpt = {"act_speed_limit" : 0, "min_rover_speed" : 0}
motor_angle_r = [] #Array containing angle for 6 wheels(radians)
rover_width_m = 0.2 #Width from center to side(m)
rover_length_m = 0.4 #Length from center to front(m)
wheel_radius_m = 0.05 #Radius of wheels(m)
motor_max_speed_rads = 1000 #Motor max turn speed(radians/s)
rov_circle_radius_m = sqrt((rover_length_m/2)**2 + (rover_width_m/2)**2) #Radius of the circle made by the spinning rover
rov_circle_circ_m = 2*pi*rov_circle_radius_m #Circumference of the circle made by the spinning rover
rov_wheel_angle = tan(rover_length_m/rover_width_m) #Angle between the wheel and rover body 


def calc_point_turn(self, mnvr_params):
    """
    Calculate Point Turn Demands
    
      Calculate demands for the point turn manoeuvre.
    
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

    # No need for a seperate function to calculate the angle; always the same for point turn


    def motor_rot_speed_calc(self, mnvr_params):
        """
        Calculate the speed motors will turn based on rover rotation rate.
        """
        # Default calculation 
        motor_rot_speed_rads = rov_circle_circ_m * mnvr_params.rov_rate_rads_Rb /wheel_radius_m

        if (abs(mnvr_params.rov_rate_rads_Rb) > motor_max_speed_rads ):
            motor_rot_speed_rads = motor_max_speed_rads
            status_rpt["act_speed_limit"] = 1

        return motor_rot_speed_rads



    # Construct namedtuple result
    result = namedtuple('SkidSteerData', ['act_dems', 'status_rpt'])

    return result(act_dems, status_rpt)