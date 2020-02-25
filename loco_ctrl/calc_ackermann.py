from collections import namedtuple
from .act_dems import ActDems
from math import atan
from math import pi
from math import isclose

def calc_ackermann(self, mnvr_params):

    # Initialise actuator demands to stopping and empty status report
    act_dems = ActDems()
    status_rpt = {"infinite_radius" : 0, "radius_inside_rover" : 0, "act_speed_limit" : 0, "reverse" : 0, "stationary" : 0}
    motor_rot_speed = [] #Array containing speed for 6 wheels(m/s)
    motor_angle = [] #Array containing angle for 6 wheels(rads)
    rover_width = 0.2 #Width from center to side(m)
    rover_length = 0.4 #Length from center to front(m)
    wheel_radius = 0.05 #Radius of wheels(m)
    motor_max = 1000 #Motor max turn speed(rads/s)
    motor_max_angle = pi/2 #Motor max rotation(rads)
    min_curv_m_rb = 0.1 #1/max radius(1/m)
    rov_speed_min = 0.01 #Min rover speed

    #Radius > max radius, rover goes straight
    def params_straight(motor_angle, motor_rot_speed):

        motor_angle.append(0)
        motor_angle.append(0)
        motor_angle.append(0)
        motor_angle.append(0)
        motor_angle.append(0)
        motor_angle.append(0)  
        
        #Calc speed of motors
        motor_speed = (mnvr_params.rov_speed_mss_Lm / wheel_radius)

        #Check motor speed > max rover speed then limit
        if abs(motor_speed) > motor_max:

            motor_speed = motor_max
            status_rpt["act_speed_limit"] = 1
        
        #Check speed is close to 0 so is stationary
        if isclose(mnvr_params.rov_speed_mss_Lm, 0, abs_tol = rov_speed_min):

            status_rpt["stationary"] = 1
            motor_speed = 0

        #Check Rover is reversing
        elif mnvr_params.rov_speed_mss_Lm < 0:

            status_rpt["reverse"] = 1
        
        motor_rot_speed.append(motor_speed)
        motor_rot_speed.append(motor_speed)
        motor_rot_speed.append(motor_speed)
        motor_rot_speed.append(motor_speed)
        motor_rot_speed.append(motor_speed)
        motor_rot_speed.append(motor_speed)

        status_rpt["infinite_radius"] = 1

        return motor_rot_speed, motor_angle
    
    #Calculate motor angle
    def motor_angle_calc(motor_angle):

        #Radius within rover body on right
        if abs(curv_radius) <= rover_width and curv_radius < 0:

            curv_radius = -rover_width
            motor_angle_left = atan(rover_length/(curv_radius - rover_width))
            motor_angle_right = -motor_max_angle

            status_rpt["radius_inside_rover"] = -1
        
        #Radius within rover body on left
        elif abs(curv_radius) <= rover_width and curv_radius > 0:

            curv_radius = rover_width
            motor_angle_left = motor_max_angle
            motor_angle_right = atan(rover_length/(curv_radius + rover_width))
            
            status_rpt["radius_inside_rover"] = 1

        #Normal calculation
        else:

            motor_angle_left = atan(rover_length/(curv_radius - rover_width))
            motor_angle_right = atan(rover_length/(curv_radius + rover_width))

        motor_angle.append(-motor_angle_left)
        motor_angle.append(-motor_angle_right)
        motor_angle.append(0)
        motor_angle.append(0)
        motor_angle.append(motor_angle_left)
        motor_angle.append(motor_angle_right)

        return motor_angle

    #Calculate motor speed
    def motor_rot_speed_calc(motor_rot_speed):

        #Calc motor speeds based on radius
        motor_speed_left = mnvr_params.rov_speed_mss_Lm * abs((curv_radius - rover_width) / (wheel_radius * curv_radius))
        motor_speed_right = mnvr_params.rov_speed_mss_Lm * abs((curv_radius + rover_width) / (wheel_radius * curv_radius))

        #Check motor speed > max rover speed then limit
        if isclose(mnvr_params.rov_speed_mss_Lm, 0, abs_tol = rov_speed_min):

            status_rpt["stationary"] = 1
            motor_speed_left = 0
            motor_speed_right = 0

        #Check Rover is reversing
        elif mnvr_params.rov_speed_mss_Lm < 0:

            status_rpt["reverse"] = 1
        
        #Motor speed faster than maxiumum
        if motor_speed_left > motor_max or motor_speed_right > motor_max:

            #Left at maximum, right reduced based on radius
            if motor_speed_left > motor_speed_right:

                motor_speed_left = motor_max
                motor_speed_right = motor_max * abs((curv_radius + rover_width) / (curv_radius - rover_width))

            #Right at maximum, left reduced based on radius
            else:

                motor_speed_right = motor_max
                motor_speed_left = motor_max * abs((curv_radius - rover_width) / (curv_radius + rover_width))
        
            status_rpt["act_speed_limit"] = 1
            
        motor_rot_speed.append(motor_speed_left)
        motor_rot_speed.append(motor_speed_right)
        motor_rot_speed.append(motor_speed_left)
        motor_rot_speed.append(motor_speed_right)
        motor_rot_speed.append(motor_speed_left)
        motor_rot_speed.append(motor_speed_right)

        return motor_rot_speed

    #Radius > max radius, goto straight function
    if isclose(mnvr_params.curv_m_Rb, 0, abs_tol = min_curv_m_rb):

        params_straight(motor_angle, motor_rot_speed)

    #Normal calculation
    else:

        curv_radius = 1 / mnvr_params.curv_m_Rb
        motor_angle_calc(motor_angle)
        motor_rot_speed_calc(motor_rot_speed)

    act_dems.append(motor_rot_speed, motor_angle)

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

    
    # Construct namedtuple result
    result = namedtuple('AckermannData', ['act_dems', 'status_rpt'])

    return result(act_dems, status_rpt)
