from math import tan, atan, pi, isclose, sqrt

#Declear variables
motor_rot_speed_rads = [] #Array containing speed for 6 wheels(radians/s)
motor_angle_r = [] #Array containing angle for 6 wheels(radians)
status_rpt = {"infinite_radius" : 0, "radius_inside_rover" : 0, "motor_angle_inner_exceeded" : 0, "motor_angle_outer_exceeded" : 0, "act_speed_limit" : 0, "stationary" : 0}
curv_m_Rb = 4 #Input 1/curve radius(1/m)
min_curv_m_rb = 0.1 #1/max radius(1/m)
rov_speed_ms_Lm = 1000 #Input rover speed(m/s)
rov_speed_min_ms = 0.01 #Min rover speed(m/s)
rover_width_m = 0.2 #Width from center to side(m)
rover_width_margin_m = 0.05 #Margin to set radius outside rover body(m)
rover_length_m = 0.4 #Length from center to front(m)
wheel_radius_m = 0.05 #Radius of wheels(m)
motor_max_speed_rads = 1000 #Motor max turn speed(radians/s)
motor_max_angle_inner_r = pi/4 #Motor max rotation for inner wheels, assume not greater than π/2(radians)
motor_max_angle_outer_r = pi/2 #Motor max rotation for outer wheels, assume not greater than π/2(radians)

def params_straight(motor_angle_r, motor_rot_speed_rads):
    """
    When the radius is large enough to be negligable (> max radius)
    treat it as the rover moving straight so all motors are operating at the same speed.
    """

    motor_angle_r = [0] * 6
    
    #Calc speed of motors
    motor_speed = (rov_speed_ms_Lm / wheel_radius_m)

    #Check motor speed > max rover speed then limit
    if abs(motor_speed) > motor_max_speed_rads:

        motor_speed = motor_max_speed_rads
        status_rpt["act_speed_limit"] = 1
    
    #Check speed is close to 0 so is stationary
    if isclose(rov_speed_ms_Lm, 0, abs_tol=rov_speed_min_ms):

        motor_speed = 0
        status_rpt["stationary"] = 1
    
    motor_rot_speed_rads = [motor_speed] * 6

    status_rpt["infinite_radius"] = 1

    return motor_rot_speed_rads, motor_angle_r

def motor_angle_calc(motor_angle_r, curv_radius_m):
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

def motor_rot_speed_calc(motor_rot_speed_rads, rov_speed_ms_Lm):
    """
    Calculate the speed each motor will turn based on the radius of the maneuver.
    If input speed is 
    """

    #Check motor speed > max rover speed then limit
    if isclose(rov_speed_ms_Lm, 0, abs_tol=rov_speed_min_ms):

        rov_speed_ms_Lm = 0
        status_rpt["stationary"] = 1

    #Calc motor speeds based on radius
    motor_speed_left_rads = rov_speed_ms_Lm * abs(sqrt((curv_radius_m - rover_width_m)**2 + rover_length_m**2) / (wheel_radius_m * curv_radius_m))
    motor_speed_right_rads = rov_speed_ms_Lm * abs(sqrt((curv_radius_m + rover_width_m)**2 + rover_length_m**2) / (wheel_radius_m * curv_radius_m))

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

#Radius > max radius, goto straight function
if isclose(curv_m_Rb, 0, abs_tol=min_curv_m_rb):

    motor_angle_r, motor_rot_speed_rads = params_straight(motor_angle_r, motor_rot_speed_rads)

#Normal calculation
else:

    curv_radius_m = 1 / curv_m_Rb
    motor_angle_r, curv_radius_m = motor_angle_calc(motor_angle_r, curv_radius_m)
    motor_rot_speed_rads = motor_rot_speed_calc(motor_rot_speed_rads, rov_speed_ms_Lm)

#Test results
print ("Speed: ", motor_rot_speed_rads, "\nPosition: ", motor_angle_r, "\nReport: ", status_rpt)