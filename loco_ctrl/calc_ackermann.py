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

    # Construct namedtuple result
    result = namedtuple('AckermannData', ['act_dems', 'status_rpt'])

    return result(act_dems, status_rpt)
