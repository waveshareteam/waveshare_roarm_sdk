# coding=utf-8
class RoarmDataException(Exception):
    pass

def check_value_type(param_type, value_type, _type):
    if value_type is not _type:
        raise RoarmDataException(
            "The acceptable parameter {} should be an {}, but the received {}".format(param_type, _type, value_type))
            
def check_cmd_or_mode(param_type, value, range_data, value_type):
    check_value_type(param_type, value_type, int)
    if value not in range_data:
        error = "The data supported by parameter {} is ".format(param_type)
        lens = len(range_data)
        for idx in range(lens):
            error += str(range_data[idx])
            if idx != lens - 1:
                error += " or "
        error += ", but the received value is {}".format(value)
        raise RoarmDataException(error)

def check_wifi_cmd(param_type, value, range_data, value_type):
    check_value_type(param_type, value_type, int)
    if value not in range_data:
        error = "The data supported by parameter {} is ".format(param_type)
        lens = len(range_data)
        for idx in range(lens):
            error += str(range_data[idx])
            if idx != lens - 1:
                error += " or "
        error += ", but the received value is {}".format(value)
        raise RoarmDataException(error)
                
def check_joint(value, valid_joints):
    if value not in valid_joints:
        raise RoarmDataException(
            f"The id not right, should be in {valid_joints}, but received {value}"
        )

def check_joint_robot_limit(value, param_type, kwargs, roarm_type, param_name, robot_limit):
    joint = kwargs.get('joint', None)
    index = robot_limit[roarm_type]['joint'][joint - 1] - 1
    limit_min = robot_limit[roarm_type][f"{param_type}_min"][index]
    limit_max = robot_limit[roarm_type][f"{param_type}_max"][index]

    if value < limit_min or value > limit_max:
        raise RoarmDataException(f"{param_name} value not right, should be {limit_min} ~ {limit_max}, but received {value}")
            
def check_joints_robot_limit(values, param_type, roarm_type, robot_limit):
    if not isinstance(values, list):
        raise RoarmDataException(f"{param_type} must be a list.")
    
    values_len = len(robot_limit[roarm_type]["joint"])
    if len(values) != values_len:
        raise RoarmDataException("The length of {param_type} must be {values_len}.")
    for index, value in enumerate(values):
        limit_min = robot_limit[roarm_type][f"{param_type}_min"][index]
        limit_max = robot_limit[roarm_type][f"{param_type}_max"][index]
        if not limit_min <= value <= limit_max:
            raise RoarmDataException(
                f"Has invalid {param_type} value, error on index {index}. "
                f"Received {value} but {param_type} should be {limit_min} ~ {limit_max}."
            )
                        
def check_joint_speed_acc(param_type, value, valid_range, value_type):
    check_value_type(param_type, value_type, int)
    min_value, max_value = valid_range
    if not min_value <= value <= max_value:
        print(
            f"{param_type} value not right, should be between {min_value} ~ {max_value}, "
            f"but received {value}."
        )   
        if value < min_value:
            value = min_value + 10
        elif value > max_value:
            value = max_value - 10
                             
def calibration_parameters(**kwargs):
    robot_limit = {
        "roarm_m2": {
            "joint": [1, 2, 3, 4],            
            "radians_min": [-3.3, -1.9, -1.2, -0.2],
            "radians_max": [3.3, 1.9, 3.3, 1.9],            
            "angles_min": [-190, -110, -70, -10],
            "angles_max": [190, 110, 190, 100],
            "positions_min": [-500, -500, 0, 0],
            "positions_max": [500, 500, 600, 90],
            "torques_min": [1, 1, 1, 1],
            "torques_max": [1000, 1000, 1000, 1000],
        },     
        "roarm_m3": {
            "joint": [1, 2, 3, 4, 5, 6],            
            "radians_min": [-3.3, -1.9, -1.2, -1.9, -3.3, -0.2],
            "radians_max": [3.3, 1.9, 3.3, 1.9, 3.3, 1.9],            
            "angles_min": [-190, -110, -70, -110, -190, -10],
            "angles_max": [190, 110, 190, 110, 190, 100],
            "positions_min": [-500, -500, 0, -90,-180, 0],
            "positions_max": [500, 500, 600, 90, 180, 90],
            "torques_min": [1, 1, 1, 1, 1, 1],
            "torques_max": [1000, 1000, 1000, 1000, 1000, 1000],
        },          
    }

    parameter_validations = {
        "cmd": lambda value, value_type, roarm_type, kwargs: check_cmd_or_mode("cmd", value, [0, 1], value_type),
        "mode": lambda value, value_type, roarm_type, kwargs: check_cmd_or_mode("mode", value, [0, 1], value_type), 
        "wifi_cmd": lambda value, value_type, roarm_type, kwargs: check_wifi_cmd("wifi_cmd", value, [0, 1, 2, 3], value_type),           
        "joint": lambda value, value_type,  roarm_type, kwargs: check_joint(value, robot_limit[roarm_type]["joint"]),   
        "radian": lambda value, value_type,  roarm_type, kwargs: check_joint_robot_limit(value, "radians", kwargs, roarm_type, "radian", robot_limit),
        "angle": lambda value, value_type,  roarm_type, kwargs: check_joint_robot_limit(value, "angles", kwargs, roarm_type, "angle", robot_limit), 
        "position": lambda value, value_type,  roarm_type, kwargs: check_joint_robot_limit(value, "positions", kwargs, roarm_type, "position", robot_limit),                
        "radians": lambda value, value_type,  roarm_type, kwargs: check_joints_robot_limit(value, "radians", roarm_type, robot_limit),
        "angles": lambda value, value_type,  roarm_type, kwargs: check_joints_robot_limit(value, "angles",  roarm_type, robot_limit),
        "pose": lambda value, value_type,  roarm_type, kwargs: check_joints_robot_limit(value, "positions", roarm_type, robot_limit), 
        "torques": lambda value, value_type,  roarm_type, kwargs: check_joints_robot_limit( value, "torques", roarm_type, robot_limit),       
        "speed": lambda value, value_type,  roarm_type, kwargs: check_joint_speed_acc("speed", value, [0, 4096], value_type),
        "acc": lambda value, value_type,  roarm_type, kwargs: check_joint_speed_acc("acc", value, [0, 254], value_type),
        "ssid": lambda value, value_type, roarm_type, kwargs: check_value_type("ssid", value_type, str),   
        "password": lambda value, value_type, roarm_type, kwargs: check_value_type("password", value_type, str)   
    }

    roarm_type = kwargs.get("roarm_type", None)
    if roarm_type not in robot_limit:
        raise RoarmDataException(f"Unknown roarm_type: {roarm_type}")

    for parameter, value in kwargs.items():
        if parameter == "roarm_type":
            continue
        
        if parameter in parameter_validations:
            try:
                value_type = type(value)
                parameter_validations[parameter](value, value_type, roarm_type, kwargs)
            except RoarmDataException as e:
                print(f"Error in parameter {parameter}: {str(e)}")
                raise e  
     
