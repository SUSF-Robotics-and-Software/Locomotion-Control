from collections import namedtuple
from .act_dems import ActDems

def calc_ackermann(self, mnvr_params):
    """
    Calculate Ackermann Demands
    
      Calculate demands for the ackermann manoeuvre.
    
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
    '''
    curv_m_Rb is maneuver curvature defined in spec TODO implement inputs from self into methods

    rover body width/2 is ROV_BDY_WDTH, i.e. distance from rover center to centre of middle wheels orthogonally in metres
    curve radius is curve_radius, i.e. 1/curvature, in metres
    desired angular velocity is ang_vel in radians/second
    length between rover centre and front/rear wheels is ROV_HLF_WHLBSE, in metres

    '''
    # TODO: Your algorithm here

    #set constants here
    #TODO: work out what the constants are from real life measurements
    float ROV_BDY_WDTH = 0.45
    float ROV_HLF_WHLBSE = 0.12771271
    
    #calculate curve radius for ease of calculating steering/drive demands
    # relative to the rover body
    def calc_curve_radius_m_Rb():
        #output 1/input param curvature

    
    def calc_act_str_dems_abs_pos_rad_Wb():
        #TODO: output demanded steer axis absolute positions in radians for all wheels as an array referring to each of the wheels
        #front left=[0], front right=[1], rear right=[5]
        # [inner front]=-1*atan(ROV_HLF_WHLBSE/(curve_radius_m_Rb()-ROV_BDY_WDTH))
        # [outer front]=-1*atan(ROV_HLF_WHLBSE/(curve_radius_m_Rb()+ROV_BDY_WDTH))
        # [inner rear] = atan(ROV_HLF_WHLBSE/(curve_radius_m_Rb()-ROV_BDY_WDTH))
        # [outer rear] = atan(ROV_HLF_WHLBSE/(curve_radius_m_Rb()+ROV_BDY_WDTH))

    #with ackermann steering geometry, inner and outer wheel speeds can remain the same as far as drive speed is concerned
    #so long as the steer axis absolute position differs correctly
    def calc_drv_rate_rads_Wb(mnvr_dir, fw_rev):
        #TODO: output desired drive axis rate for the wheels of the rover's turn in rads/sec      
        #inputs : output of cnvrt_ms_to_rads_Lm_to_Wb()
        #output : array of demanded drive rates in rad/s corresponding to each of the wheels

    def calc_drive_pwm_pwm():
        #TODO: convert the desired drive rate in rad/s to a PWM value, and output it into act_dems as the drv_dem_pwm values
        #input : output of calc_drv_rate_rads_Wb()
        #output: PWM demands of the wheels to achieve drive demand
    
    # Either the maneuver is to the right, or to the left. If the steer values for a 
    # turn intended to be to the right are used without checking this, then the rover
    # may turn left even when a right turn is required, since the raw radian values of 
    # the absolute position demanded from the steer axis are signed
    # Thus the directionality of the maneuver must be checked to ensure the right values
    # are outputted.
    def calc_mnvr_dir_rght_lft_Rb():
        #TODO: calculate the direction of the maneuver, output 0 if maneuver is to the left, 1 if to the right
        #calculated from input x and y
    
    # The explanation for this is the same as for calc_mnvr_rght_lft_Rb(), except for 
    # the drive axis. If the directionality isn't checked, then a maneuver intended to 
    # make the rover reverse may instead make it drive further forward.
    def calc_mnvr_fw_rev_Rb():
        #TODO: calculate forwards/backwards directionality of maneuver from input x and y, output 1 if forwards
        # ,-1 if backwards
        #calculated from input x and y

    #required conversion to output a desired pwm width
    def cnvrt_ms_to_rads_Wb():
        #TODO: convert calculated drive wheel speed in m/s into rad/s drive axis relative to the wheel bracket
        #  rates relative to the Wheel bracket
    
    #input x and y will define a desired angular velocity of the maneuver for the rover in the local map frame
    # we need to convert this to a m/s param in the rover body frame to handle the rover body speed requirements
    def cnvrt_rads_Lm_to_ms_Rb():
        #TODO: convert radians per second rover maneuver angular velocity to the m/s required by the rover on the local map frame

    def calc_str_pwm_pwm():
        #TODO: calculate pwm width for steer demand requested, i.e. directionality of steering for each steering bracket and pwm width to demand the turn
        # pwm width should be fixed until the act_sens_data for the absolute position of the steering axis
        # matches that of the desired one for the maneuver

    
    # Construct namedtuple result
    result = namedtuple('AckermannData', ['act_dems', 'status_rpt'])

    return result(act_dems, status_rpt)
