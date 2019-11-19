from CommsAndCommand.command import single_value_command, command_set

wheel_1_speed = single_value_command(name="wheel_1_speed")
wheel_2_speed = single_value_command(name="wheel_2_speed")

wheel_set = command_set(
    wheel_1_speed,
    wheel_2_speed,
    name="wheel_set"
)
