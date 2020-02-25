# Locomotion Control Module Specification

## Public Functions

The `Locomotion-Control` class shall have two public functions in addition to 
the default constructor contained in `__init__.py`:

### Public Function `get_act_telem`

```python
# get_act_telem:
#   Retrieve telemetry from the actuators
def get_act_telem(self):
```

The sensing function `get_act_telem` shall be called at the start of a software 
cycle, and will be used to acquire relevant actuator data for processing by 
other modules.

Note that actuator sensor data is specific to each rover. Currently only sensor 
data for Hercules (Phobos) shall be defined and populated. Handling of different
styles of actuator output is currently __TBD__.

__Inputs__: `self` only

__Outputs__: Actuator sensor data:

```python
# Actuator Sensor Data
#   `namedtuple` containing sensor data for the actuators.
act_sen_data:

    # Drive Incremented Axis Position (from last initialisation)
    #   Unit:  radians
    #   Frame: Wheel bracKet
    drv_inc_pos_rad_Wk[NUM_DRV_AXES]

    # Drive Axis Rate
    #   Unit:  radians / second
    #   Frame: Wheel bracKet
    drv_rate_rads_Wk[NUM_DRV_AXES]

    # Drive Axis Current Draw
    #   Unit:  Amperes
    #   Frame: N/A
    drv_curr_amp[NUM_DRV_AXES]

    # Steer Axis Absolute Position (absolute)
    #   Unit:  radians
    #   Frame: Steering bracKet
    str_abs_pos_rad_Sk[NUM_STR_AXES]

    # Steer Axis Rate
    #   Unit:  radians / second
    #   Frame: Steering bracKet
    str_rate_rads_Wk[NUM_DRV_AXES]

    # Steer Axis Current Draw
    #   Unit:  Amperes
    #   Frame: N/A
    str_curr_amp[NUM_DRV_AXES]
```

### Public Function `do_mnvr_ctrl`

```python
# do_mnvr_ctrl:
#   Perform manouevre control calculations and issue demands to the actuators
def do_mnvr_ctrl(self, mnvr_cmd):
```

The actuating function `do_mnvr_ctrl` shall command the actuators to the correct
positions and speeds required to perform the commanded manoeuvre.

Note that actuator control is specific to each rover. Currently only Hercules 
(Phobos) will be supported, handling of different rover configurations is 
__TBD__.

__Inputs__: `self`, Manoeuvre Command:

```python
# Manoeuvre Command
#   `namedtuple` containing manouvre command from higher level modules.
mnvr_cmd:

    # Manoeuvre ID, as defined by the MnvrId Enum
    #   Unit:  N/A
    #   Frame: N/A
    mnvr_id

    # Manouvre Parameters, `namedtuple` which shall follow the params 
    # definitions given in the module spec.
    #   Unit:  N/A
    #   Frame: N/A
    mnvr_params
```

__Manoeuvre Parameters__:

The below list shows which parameters shall be present in the `mnvr_cmd.params` 
`namedtuple` object when that manoeuvre ID is specified:

```python
# Rover Speed (speed of the Rover Body frame over the Local Map frame)
#   Unit:  metres / (second)
#   Frame: Local Map
#
#   Required for: Skid steering, Ackerman
rov_speed_mss_Lm

# Curvature of Manoeuvre (1 / radius of turn), relative to the Rover Body frame.
#   Unit:  1 / metres
#   Frame: Rover Body
#
#   Required for: Skid steering, Ackerman
curv_m_Rb

# Rover Rotation Rate, rate of turn about the Rover Body Z axis.
#   Unit:  radians / second
#   Frame: Rover Body
#
#   Required for: Point turn
rov_rate_rads_Rb
```

## Private Functions

The `Locomotion-Control` class shall implement the following internal (private)
functions:

### Private Function `calc_skid_steer_mnvr`

