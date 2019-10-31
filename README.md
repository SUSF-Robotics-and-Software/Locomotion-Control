# Locomotion Control

Repository for storing the Locomotion Control module for the Olympus Rover 
project.

## Team Development Goals

This module is not complete. The current code performs data handling and sets 
up the required boilerplate to allow the control calculations to be performed. 
Each team will take charge of a single control calculation, one of:

* Skid Steering _"tank"_
* Ackerman _"car"_
* Point Turn _"turret"_

__Control Calculation Functions:__

Each control calculation is done by a function, which will be called when that
particular manoeuvre is demanded. The functions have the following prototypes:

```python
def calc_manoeuvre(self, mnvr_params):
    ...
    return result(act_dems, status_rpt)
```

The `mnvr_params` input dictionary gives you access to the parameters required 
for your manouvre (see `docs/spec.md` to see the names and definitions of the
parameters), while `self` gives you access to the module parameters through 
`self.params` (more detail later).

The outputs are a `result` (a named tuple defined in the function itself) of 
`act_dems` and `status_rpt`. The `act_dems` (actuator demands) are defined in 
the `loco_ctrl/act_dems.py` file, and contain the target positions of the 
Rover's steering axes, and the target speeds of the drive and steer axes, and 
the target accelerations of the drive axes (plus PWM demands which do _not_ 
need to be calculated at this stage). Your function must populate these values 
so that the demanded manoeuvres are met, with smooth transitions between the 
current states and target states.

The `status_rpt` is a dictionary that will be used by the module control flow to
decide if something has gone wrong during your calculations. If something goes 
wrong during your calculation (such as a parameter you expect to be non-zero is
equal to zero), you should raise a flag in the status report with a descriptive 
name, and output any information in the report you feel is useful (see 
`loco_ctrl/do_mnvr_ctrl.py` line `71` to see an example of this).

__Use of Parameters:__

Your function should not use "magic numbers" at any point. Instead you should 
define parameters in your specific parameter file, found at 
`params/mnvr_[MNVR NAME].hjson`. For example:

```python
# Bad: where does this number come from?
str_abs_pos_rad_Sk = 12 * rov_spd_mss_Lm

# Good: can go and reference the parameter file to find out how this magic 
# number fits into everything
str_abs_pos_rad_Sk =
    self.params.mnvr_skid_steer.important_constant * rov_spd_mss_Lm
```

You should define your parameters in your own manoeuvre's file. Once the design 
is complete these separate files will be combined into a single parameter file 
(splitting at this stage is to avoid naming conflicts between teams). You can 
use parameter already defined in the `loco_ctrl.hjson` file, and should copy 
the documentation style used there.

__Testing Your Implementation:__

A testing suite has been created which will subject your functions to a veriety
of different parameters. These tests will not tell you if you get the 
calculations right, they only exist to check that your status reports contain 
suitable statements when something is wrong. You can run the tests using the 
`run_test.sh` bash script from the root directory, alternatively look there to 
find the python commands required (for instance if running on Windows without 
bash).

__Git Usage__:

Under no circumstances commit directly to the `master` branch! Three branches 
exist for your active development `dev-skid`, `dev-ack`, and `dev-pt`, please 
commit to those only. Once you think you have a working implementation you 
should open a pull request from your `dev` branch to the `development` branch, 
where we will review your code.

## Non-Standard Dependencies

These should be installed for your python version.

`hjson`: Human-readable JSON, adds comments (!) to JSON

## Scripts

`run_test.sh`: 
Run from bash, if using Windows 10 Git Bash make sure you're using the right 
line (look at the script).