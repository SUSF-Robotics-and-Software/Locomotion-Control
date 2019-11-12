from .constants import MnvrType
from .act_dems import ActDems
from .calc_skid_steer import calc_skid_steer
from .calc_ackermann import calc_ackermann
from .calc_point_turn import calc_point_turn


def do_mnvr_ctrl(self, mnvr_cmd):
    """
    Do Manoeuvre Control
    
          __IMPLEMENTATION NOT COMPLETE__
    
      Command actuators to respond to the given manoeuvre command.
    
      Inputs:
          self: LocoCtrl module state
          mnvr_cmd: Manoeuvre Command (see module spec)
    
      Outputs:
          status_rpt: Status report dictionary, populated with error flags when
              appropriate
    """
    
    # Initialise status report
    status_rpt = {}

    # Initialise actuator demands, will be initialised as stopping
    act_dems = ActDems()

    # If no manouvre demanded set all actuators to STOPPED
    if (mnvr_cmd.mnvr_id == MnvrType.NONE):
        # Nothing to do, actuator demands are initialised to zero
        pass

    elif (mnvr_cmd.mnvr_id == MnvrType.SKID_STEER):
        # Call the skid steer calculation function, which returns a named tuple 
        # with actuator demands and status report content
        skid_steer_data = calc_skid_steer(self, mnvr_cmd.mnvr_params)

        # Add the skid steer report to the function status report
        status_rpt.update(skid_steer_data.status_rpt)

        # Set the actuator demands
        act_dems = skid_steer_data.act_dems

    elif (mnvr_cmd.mnvr_id == MnvrType.ACKERMAN):
        # Call the Ackerman calculation function, which returns a named tuple 
        # with actuator demands and status report content
        ackerman_data = calc_ackermann(self, mnvr_cmd.mnvr_params)

        # Add the skid steer report to the function status report
        status_rpt.update(ackerman_data.status_rpt)

        # Set the actuator demands
        act_dems = ackerman_data.act_dems

    elif (mnvr_cmd.mnvr_id == MnvrType.POINT_TURN):
        # Call the point turn calculation function, which returns a named tuple 
        # with actuator demands and status report content
        point_turn_data = calc_point_turn(self, mnvr_cmd.mnvr_params)

        # Add the skid steer report to the function status report
        status_rpt.update(point_turn_data.status_rpt)

        # Set the actuator demands
        act_dems = point_turn_data.act_dems

    else:
        # Invalid manoeuvre type, we set the corresponding error flag to true.
        # We also would set actuator demands to stopping however these have 
        # already been dealt with since ActDems() shall initialise all values to
        # stop values anyway.
        status_rpt['invalid_mnvr_id'] = True

    # Actuate the demands
    # TODO
    # self.actuate(act_dems)

    return status_rpt