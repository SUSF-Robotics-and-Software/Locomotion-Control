from collections import namedtuple
from .act_dems import ActDems
from math import tan, atan, pi, isclose, sqrt

#Declear variables
status_rpt = {"infinite_radius" : 0, "radius_inside_rover" : 0, "motor_angle_inner_exceeded" : 0, "motor_angle_outer_exceeded" : 0, "act_speed_limit" : 0, "min_rover_speed" : 0}
motor_rot_speed_rads = [] #Array containing speed for 6 wheels(radians/s)
motor_angle_r = [] #Array containing angle for 6 wheels(radians)
min_curv_m_rb = 0.1 #1/max radius(1/m)
rov_speed_min_ms = 0.01 #Min rover speed(m/s)
rover_width_m = 0.2 #Width from center to side(m)
rover_width_margin_m = 0.05 #Margin to set radius outside rover body(m)
rover_length_m = 0.4 #Length from center to front(m)
wheel_radius_m = 0.05 #Radius of wheels(m)
motor_max_speed_rads = 1000 #Motor max turn speed(radians/s)
motor_max_angle_inner_r = pi/4 #Motor max rotation for inner wheels, assume not greater than π/2(radians)
motor_max_angle_outer_r = pi/2 #Motor max rotation for outer wheels, assume not greater than π/2(radians)

def calc_ackermann(self, mnvr_params):
    """
    Initialise program and work out the angle of each motor and speed of each motor
    """

    # Initialise actuator demands to stopping and empty status report
    act_dems = ActDems()
    """status_rpt = {"infinite_radius" : 0, "radius_inside_rover" : 0, "motor_angle_inner_exceeded" : 0, "motor_angle_outer_exceeded" : 0, "act_speed_limit" : 0, "min_rover_speed" : 0}
    motor_rot_speed_rads = [] #Array containing speed for 6 wheels(radians/s)
    motor_angle_r = [] #Array containing angle for 6 wheels(radians)
    min_curv_m_rb = 0.1 #1/max radius(1/m)
    rov_speed_min_ms = 0.01 #Min rover speed(m/s)
    rover_width_m = 0.2 #Width from center to side(m)
    rover_width_margin_m = 0.05 #Margin to set radius outside rover body(m)
    rover_length_m = 0.4 #Length from center to front(m)
    wheel_radius_m = 0.05 #Radius of wheels(m)
    motor_max_speed_rads = 1000 #Motor max turn speed(radians/s)
    motor_max_angle_inner_r = pi/4 #Motor max rotation for inner wheels, assume not greater than π/2(radians)
    motor_max_angle_outer_r = pi/2 #Motor max rotation for outer wheels, assume not greater than π/2(radians)"""

    #Radius > max radius, goto straight function
    if isclose(mnvr_params.curv_m_Rb, 0, abs_tol=min_curv_m_rb):

        motor_angle, motor_rot_speed = params_straight(self, mnvr_params, motor_angle_r, motor_rot_speed_rads)

    #Normal calculation
    else:

        #Convert curv_m_Rb to curve radius(m)
        curv_radius_m = 1 / mnvr_params.curv_m_Rb
        motor_angle = motor_angle_calc(self, mnvr_params, motor_angle_r, curv_radius_m)
        motor_rot_speed = motor_rot_speed_calc(self, mnvr_params, motor_rot_speed, curv_radius_m)

    act_dems = [motor_rot_speed, motor_angle]

    # Construct namedtuple result
    result = namedtuple('AckermannData', ['act_dems', 'status_rpt'])

    return result(act_dems, status_rpt)

def params_straight(self, mnvr_params, motor_angle_r, motor_rot_speed_rads):
    """
    When the radius is large enough to be negligable (> max radius)
    treat it as the rover moving straight so all motors are operating at the same speed.
    """

    motor_angle_r = [0] * 6
    
    #Calc speed of motors
    motor_speed = (mnvr_params.rov_speed_ms_Lm / wheel_radius_m)

    #Check motor speed > max rover speed then limit
    if abs(motor_speed) > motor_max_speed_rads:

        motor_speed = motor_max_speed_rads
        status_rpt["act_speed_limit"] = 1
    
    #Check speed is close to 0 so is min_rover_speed
    if isclose(mnvr_params.rov_speed_ms_Lm, 0, abs_tol=rov_speed_min_ms):

        motor_speed = 0
        status_rpt["min_rover_speed"] = 1
    
    motor_rot_speed_rads = [motor_speed] * 6

    status_rpt["infinite_radius"] = 1

    return motor_rot_speed_rads, motor_angle_r

def motor_angle_calc(self, mnvr_params, motor_angle_r, curv_radius_m):
    """
    Calculate the angle each motor will be based on the radius of the maneuver.
    If the radius is inside the rover limit the radius to the rover body + margin.
    """

    #Radius within rover body on right
    if abs(curv_radius_m) <= rover_width_m and curv_radius_m < 0:

        curv_radius_m = -rover_width_m - rover_width_margin_m
        motor_angle_left_r = atan(rover_length_m/(curv_radius_m - rover_width_m))
        
        if rover_width_margin_m == 0:

            motor_angle_right_r = -motor_max_angle_inner_r

        else:

            motor_angle_right_r = atan(rover_length_m/(curv_radius_m + rover_width_m))

        status_rpt["radius_inside_rover"] = -1
    
    #Radius within rover body on left
    elif abs(curv_radius_m) <= rover_width_m and curv_radius_m > 0:

        curv_radius_m = rover_width_m + rover_width_margin_m
        motor_angle_right_r = atan(rover_length_m/(curv_radius_m + rover_width_m))

        if rover_width_margin_m == 0:

            motor_angle_left_r = motor_max_angle_inner_r
        
        else:

            motor_angle_left_r = atan(rover_length_m/(curv_radius_m - rover_width_m))
        
        status_rpt["radius_inside_rover"] = 1

    #Normal calculation
    else:

        motor_angle_left_r = atan(rover_length_m/(curv_radius_m - rover_width_m))
        motor_angle_right_r = atan(rover_length_m/(curv_radius_m + rover_width_m))
    
    #Motor angle right greater than the max inner angle on right turn
    if motor_angle_right_r < -motor_max_angle_inner_r and curv_radius_m < 0:
        
        motor_angle_right_r = -motor_max_angle_inner_r
        curv_radius_m = (rover_length_m / tan(motor_angle_right_r)) - rover_width_m
        motor_angle_left_r = atan(rover_length_m/(curv_radius_m - rover_width_m))
        status_rpt["motor_angle_inner_exceeded"] = -1

    #Motor angle left greater than the max inner angle on left turn
    elif motor_angle_left_r > motor_max_angle_inner_r and curv_radius_m > 0:
        
        motor_angle_left_r = motor_max_angle_inner_r
        curv_radius_m = (rover_length_m / tan(motor_angle_left_r)) + rover_width_m
        motor_angle_right_r = atan(rover_length_m/(curv_radius_m + rover_width_m))
        status_rpt["motor_angle_inner_exceeded"] = 1

    #Motor angle right greater than max outer angle on left turn
    if motor_angle_right_r > motor_max_angle_outer_r and curv_radius_m > 0:

        motor_angle_right_r = motor_max_angle_outer_r
        curv_radius_m = (rover_length_m / tan(motor_angle_right_r)) - rover_width_m
        motor_angle_left_r = atan(rover_length_m/(curv_radius_m - rover_width_m))
        status_rpt["motor_angle_outer_exceeded"] = 1

    #Motor angle left greater than max outer angle on right turn
    elif motor_angle_left_r < -motor_max_angle_outer_r and curv_radius_m < 0:

        motor_angle_left_r = -motor_max_angle_outer_r
        curv_radius_m = (rover_length_m / tan(motor_angle_left_r)) + rover_width_m
        motor_angle_right_r = atan(rover_length_m/(curv_radius_m + rover_width_m))
        status_rpt["motor_angle_outer_exceeded"] = -1

    motor_angle_r = [motor_angle_left_r, motor_angle_right_r, 0, 0, -motor_angle_left_r, -motor_angle_right_r]
    
    return motor_angle_r, curv_radius_m

def motor_rot_speed_calc(self, mnvr_params, motor_rot_speed_rads, curv_radius_m):
    """
    Calculate the speed each motor will turn based on the radius of the maneuver.
    If input speed is 
    """

    #Check motor speed is close to zero
    if isclose(mnvr_params.rov_speed_ms_Lm, 0, abs_tol=rov_speed_min_ms):

        mnvr_params.rov_speed_ms_Lm = 0
        status_rpt["min_rover_speed"] = 1

    #Calc motor speeds based on radius
    motor_speed_left_rads = mnvr_params.rov_speed_ms_Lm * abs(sqrt((curv_radius_m - rover_width_m)**2 + rover_length_m**2) / (wheel_radius_m * curv_radius_m))
    motor_speed_right_rads = mnvr_params.rov_speed_ms_Lm * abs(sqrt((curv_radius_m + rover_width_m)**2 + rover_length_m**2) / (wheel_radius_m * curv_radius_m))

    #Motor speed faster than maxiumum
    if abs(motor_speed_left_rads) > motor_max_speed_rads or abs(motor_speed_right_rads) > motor_max_speed_rads:

        #Left at maximum, right reduced based on radius
        if abs(motor_speed_left_rads) > abs(motor_speed_right_rads):
            
            rov_speed_ms_Lm = (rov_speed_ms_Lm / abs(rov_speed_ms_Lm)) * (motor_max_speed_rads * wheel_radius_m * curv_radius_m) / (sqrt((curv_radius_m - rover_width_m)**2 + rover_length_m**2))
            motor_speed_left_rads = (rov_speed_ms_Lm / abs(rov_speed_ms_Lm)) * motor_max_speed_rads
            motor_speed_right_rads = rov_speed_ms_Lm * abs(sqrt((curv_radius_m + rover_width_m)**2 + rover_length_m**2) / (wheel_radius_m * curv_radius_m))
            status_rpt["act_speed_limit"] = 1

        #Right at maximum, left reduced based on radius
        else:

            rov_speed_ms_Lm = (rov_speed_ms_Lm / abs(rov_speed_ms_Lm)) * (motor_max_speed_rads * wheel_radius_m * curv_radius_m) / (sqrt((curv_radius_m + rover_width_m)**2 + rover_length_m**2))
            motor_speed_left_rads = rov_speed_ms_Lm * abs(sqrt((curv_radius_m - rover_width_m)**2 + rover_length_m**2) / (wheel_radius_m * curv_radius_m))
            motor_speed_right_rads = (rov_speed_ms_Lm / abs(rov_speed_ms_Lm)) * motor_max_speed_rads
            status_rpt["act_speed_limit"] = -1
    
    motor_speed_left_mid_rads = rov_speed_ms_Lm * abs((curv_radius_m - rover_width_m) / (wheel_radius_m * curv_radius_m))
    motor_speed_right_mid_rads = rov_speed_ms_Lm * abs((curv_radius_m + rover_width_m) / (wheel_radius_m * curv_radius_m))
    
    motor_rot_speed_rads = [motor_speed_left_rads, motor_speed_right_rads, motor_speed_left_mid_rads, motor_speed_right_mid_rads, motor_speed_left_rads, motor_speed_right_rads]

    return motor_rot_speed_rads

#Separate code
    """#set constants here
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
        # matches that of the desired one for the maneuver"""
