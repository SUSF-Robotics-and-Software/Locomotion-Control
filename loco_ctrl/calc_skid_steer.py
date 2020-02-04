# from collections import namedtuple
from CommsAndCommand import command
from .act_dems import ActDems
from .temp_commands import *

def calc_skid_steer(self, mnvr_params):
    """
    Calculate Skid Steer Demands
    
      Calculate demands for the skid steer manoeuvre.
    
      Inputs:
          self: LocoCtrl module state
          mnvr_params: Dictionary of parameters for the manoeuvre, see docs/spec
    
      Outputs:
          `namedtuple` of two members:
          act_dems: Actuator demands, an instance of ActDems
          status_rpt: Status report dictionary, to be populated with error flags
              when necessary.
    """
    
def skid_steer_formula(Vb, K, w, d, omega):
    """
    Function Task: Return the Throttle Commands for Left and Right Wheel Groups.
    Inputs:
        Vb: Demanded Rover Body Speed, metres per second.
        K: Demanded Rover turn Curvature (K = 1/radius of turn), metres^-1.
            A positive curvature K > 0 will result in the rover turning right.
        w: Wheelbase, normal distance between left and right wheel parallel planes, metres.
        d: Wheel diameter of Rover wheels, metres.
        omega: The maximum angular velocity of the rover wheel, radians per second.
    Outputs:
        Throttle_L: The throttle percentage from -1.0 to 1.0 of the wheel servos on the left of the rover.
        Throttle_R: The throttle percentage from -1.0 to 1.0 of the wheel servos on the right of the rover.
    """

    # This function would require flags to identify when a demanded body velocity results in an abs(Throttle) > 1, which is not possible.

    # If K > 0 and the Rover is turning right Vb > 0, the likely constraint is that the left motors will demand Throttle > 1
    if (K > 0 and Vb > 0):

        # Check if the demanded throttle is too great with an inequality
        if ( ((d * omega) / Vb) - 2 < K*w ):

            # The body velocity demanded is too great. Set Vb to an acceptable value that maintains curvature at the highest available throttle.
            Vb = (d * omega) / (2 + K*w)
    
    # If K < 0 and the Rover is turning left Vb > 0, the likely constraint is that  the right motors will demand Throttle > 1
    else if(K < 0 and Vb > 0):

        if ( )


    Throttle_L = ((2 + K*w) * Vb) / (d * omega)
    Throttle_R = ((2 - K*W) * Vb) / (d * omega)

    return(Throttle_L, Throttle_R)


    # Initialise actuator demands to stopping and empty status report
    # act_dems = ActDems()
    # status_rpt = {}

    # TODO: Your algorithm here



    wheel_1_speed.value = None
    wheel_2_speed.value = None

    # Construct namedtuple result
    # result = namedtuple('SkidSteerData', ['act_dems', 'status_rpt'])
    # return result(act_dems, status_rpt)