# coding=utf-8

from __future__ import division
import time
import json
import queue
import threading
import logging
import math
from datetime import datetime

class JsonCmd(object):
    ECHO_SET = 605
    MIDDLE_SET = 502
    LED_CTRL = 114
    TORQUE_SET = 210  
    DYNAMIC_ADAPTATION_SET = 112     
    FEEDBACK_GET = 105
    JOINT_RADIAN_CTRL = 101    
    JOINTS_RADIAN_CTRL = 102 
    JOINT_ANGLE_CTRL = 121
    JOINTS_ANGLE_CTRL = 122   
    GRIPPER_MODE_SET = 222 
    POSE_CTRL = 1041 
    WIFI_ON_BOOT = 401    
    AP_SET = 402
    STA_SET = 403
    APSTA_SET = 404   
    WIFI_CONFIG_CREATE_BY_STATUS = 406 
    WIFI_CONFIG_CREATE_BY_INPUT = 407     
    WIFI_STOP =408
                   
class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()  
        self.s = s         
        self.timeout = 0.1 
        self.frame_start = b'{'
        self.frame_end =  b"}\r\n"
        self.max_frame_length = 512
 
    def readline(self):
        start_time = time.time() 
        while True:
            i = max(1, min(self.max_frame_length, self.s.in_waiting))
            data = self.s.read(i)
            if data:
                self.buf.extend(data)

            end = self.buf.rfind(self.frame_end)

            if end >= 0:  
                start = self.buf.rfind(self.frame_start, 0, end)
                if start >= 0 and start < end:
                    r = self.buf[start:end + len(self.frame_end)] 
                    self.buf = self.buf[end + len(self.frame_end):]
                    return r
                elif start == -1:
                    continue

            if time.time() - start_time > self.timeout:
                break
 
    def clear_buffer(self):
        self.buf = bytearray()
        try:
            self.s.reset_input_buffer()
        except Exception as e:
            print(f"Error resetting input buffer: {e}")
        
class BaseController:
    def __init__(self, roarm_type, port):
        self.log = logging.getLogger('BaseController')
        self.ser = port
        self.type = roarm_type
        self.rl = ReadLine(self.ser)
        self.data_buffer = None
        
        feedback_data_m2 = {"T": 1051, "x": 0, "y": 0, "z": 0, "b": 0, "s": 0, "e": 0, "t": 0, "torB": 0, "torS": 0, "torE": 0, "torH": 0}
        feedback_data_m3 = {"T": 1051, "x": 0, "y": 0, "z": 0, "tit": 0, "b": 0, "s": 0, "e": 0, "t": 0, "r": 0, "g": 0, "tB": 0, "tS": 0, "tE": 0, "tT": 0, "tR": 0, "tG": 0}

        switch_dict = {
            "roarm_m2": feedback_data_m2,
            "roarm_m3": feedback_data_m3,
        }
        self.base_data = switch_dict[self.type]
        
    def feedback_data(self):
        try:
            line = self.rl.readline().decode('utf-8')
            self.data_buffer = json.loads(line)
            self.base_data = self.data_buffer
            self.rl.clear_buffer()   
            return self.base_data                  
        except json.JSONDecodeError as e:
            self.log.error(f"JSON decode error: {e} with line: {line}")
            self.rl.clear_buffer()
        except Exception as e:
            self.log.error(f"[base_ctrl.feedback_data] unexpected error: {e}")
            self.rl.clear_buffer()
    
def handle_echo_or_torque_set(roarm_type,command,command_data):
    command.update({"cmd": command_data[0]})
    return command

def handle_middle_set(roarm_type,command,command_data):
    command.update({"id": command_data[0]})
    return command
    
def handle_led_ctrl(roarm_type,command,command_data):
    command.update({"led": command_data[0]})
    return command

def handle_m2_dynamic_adaptation(command,command_data):
    command.update({"mode": command_data[0], "b": command_data[1],"s": command_data[2],"e": command_data[3],"h": command_data[4]})  
    return command
    
def handle_m3_dynamic_adaptation(command,command_data):
    command.update({"mode": command_data[0], "b": command_data[1],"s": command_data[2],"e": command_data[3],"t": command_data[4],"r": command_data[5],"h": command_data[6]})  
    return command
        
def handle_dynamic_adaptation_set(roarm_type,command,command_data):
    switch_dict = {
        "roarm_m2": handle_m2_dynamic_adaptation,
        "roarm_m3": handle_m3_dynamic_adaptation,
    }
    command = switch_dict[roarm_type](command,command_data)
    return command
            
def handle_joint_radian_ctrl(roarm_type,command,command_data):
    switch_dict = {
        "roarm_m2": 4,
        "roarm_m3": 6,
    }
    gripper = switch_dict[roarm_type]
    if command_data[0] == gripper: 
        command_data[1] = math.pi - command_data[1]        
    command.update({"joint": command_data[0], "rad": command_data[1], "spd": command_data[2], "acc": command_data[3]})
    return command
    
def handle_m2_joints_radian(command,command_data):
    command_data[3] = math.pi - command_data[3]
    command.update({"base": command_data[0], "shoulder": command_data[1], "elbow": command_data[2], "hand": command_data[3], "spd": command_data[4], "acc": command_data[5]})
    return command
    
def handle_m3_joints_radian(command,command_data):
    command_data[5] = math.pi - command_data[5]  
    command.update({"base": command_data[0], "shoulder": command_data[1], "elbow": command_data[2], "wrist": command_data[3], "roll": command_data[4], "hand": command_data[5], "spd": command_data[6], "acc": command_data[7]})
    return command
        
def handle_joints_radian_ctrl(roarm_type,command,command_data):    
    switch_dict = {
        "roarm_m2": handle_m2_joints_radian,
        "roarm_m3": handle_m3_joints_radian,
    }
    command = switch_dict[roarm_type](command,command_data)
    return command
        
def handle_joint_angle_ctrl(roarm_type,command,command_data):
    switch_dict = {
        "roarm_m2": 4,
        "roarm_m3": 6,
    }
    gripper = switch_dict[roarm_type]
    if command_data[0] == gripper: 
        command_data[1] = 180 - command_data[1]  
    command_data[2] = (command_data[2] * 180) / 2048
    command_data[3] = (command_data[3] * 180) / (254*100)         
    command.update({"joint": command_data[0], "angle": command_data[1], "spd": command_data[2], "acc": command_data[3]})
    return command
    
def handle_m2_joints_angle(command,command_data):
    command_data[3] = 180 - command_data[3]  
    command_data[4] = (command_data[4] * 180) / 2048
    command_data[5] = (command_data[5] * 180) / (254*100)
    command.update({"b": command_data[0],"s": command_data[1],"e": command_data[2],"h": command_data[3], "spd": command_data[4], "acc": command_data[5]})  
    return command
    
def handle_m3_joints_angle(command,command_data):
    command_data[5] = 180 - command_data[5]
    command_data[6] = (command_data[6] * 180) / 2048
    command_data[7] = (command_data[7] * 180) / (254*100)   
    command.update({"b": command_data[0],"s": command_data[1],"e": command_data[2],"t": command_data[3],"r": command_data[4],"h": command_data[5], "spd": command_data[6], "acc": command_data[7]})  
    return command
    
def handle_joints_angle_ctrl(roarm_type,command,command_data):
    switch_dict = {
        "roarm_m2": handle_m2_joints_angle,
        "roarm_m3": handle_m3_joints_angle,
    }
    command = switch_dict[roarm_type](command,command_data)
    return command
            
def handle_gripper_mode_set(roarm_type,command,command_data):
    command.update({"name": "boot", "step": f'{{"T":1,"mode":{command_data[0]}}}'})
    return command

def handle_m2_pose(command,command_data):
    command_data[3] = math.pi - ((command_data[3] * math.pi) / 180)
    command.update({"x": command_data[0], "y": command_data[1], "z": command_data[2], "t": command_data[3]})
    return command
    
def handle_m3_pose(command,command_data):
    command_data[3:5] = [(command_data * math.pi) / 180 for command_data in command_data[3:5]] 
    command_data[5] = math.pi - ((command_data[5] * math.pi) / 180)
    command.update({"x": command_data[0], "y": command_data[1], "z": command_data[2], "t": command_data[3], "r": command_data[4], "g": command_data[5]})
    return command
        
def handle_pose_ctrl(roarm_type,command,command_data):
    switch_dict = {
        "roarm_m2": handle_m2_pose,
        "roarm_m3": handle_m3_pose,
    }
    command = switch_dict[roarm_type](command,command_data)
    return command
    
def handle_wifi_on_boot(roarm_type,command,command_data):
    command.update({"mode":command_data[0]})
    return command

def handle_ap_or_sta_set(roarm_type,command,command_data):
    command.update({"ssid":command_data[0], "password":command_data[1]})
    return command
    
def handle_ap_sta_set(roarm_type,command,command_data):
    command.update({"ap_ssid":command_data[0], "ap_password":command_data[1], "sta_ssid":command_data[2], "sta_password":command_data[3]})
    return command

def handle_m2_feedback(valid_data,data):
    valid_data.append(data['b'])    
    valid_data.append(data['s'])
    valid_data.append(data['e']) 
    data['t'] = math.pi - data['t'] 
    valid_data.append(data['t'])
#    valid_data.append(data['torB'])    
#    valid_data.append(data['torS'])
#    valid_data.append(data['torE'])
#    valid_data.append(data['torH'])     
    return valid_data

def handle_m3_feedback(valid_data,data): 
    valid_data.append(data['tit'])   
    valid_data.append(data['b'])    
    valid_data.append(data['s'])
    valid_data.append(data['e'])  
    valid_data.append(data['t'])
    valid_data.append(data['r'])
    data['g'] = math.pi - data['g']  
    valid_data.append(data['g'])
#    valid_data.append(data['tB'])    
#    valid_data.append(data['tS'])
#    valid_data.append(data['tE'])
#    valid_data.append(data['tT'])
#    valid_data.append(data['tR'])     
    return valid_data
                        
class DataProcessor(object):
    def _mesg(self, genre, *args):
        """
        Args:
            genre: command type (Command)
            *args: other data.
                   It is converted to octal by default.
                   If the data needs to be encapsulated into hexadecimal,
                   the array is used to include them. (Data cannot be nested)
        """
        command_data = self._process_data_command(args)
        switch_dict = {
            JsonCmd.ECHO_SET: handle_echo_or_torque_set,
            JsonCmd.MIDDLE_SET: handle_middle_set,
            JsonCmd.LED_CTRL: handle_led_ctrl,
            JsonCmd.TORQUE_SET: handle_echo_or_torque_set,
            JsonCmd.DYNAMIC_ADAPTATION_SET: handle_dynamic_adaptation_set,
            JsonCmd.JOINT_RADIAN_CTRL: handle_joint_radian_ctrl,
            JsonCmd.JOINTS_RADIAN_CTRL: handle_joints_radian_ctrl,
            JsonCmd.JOINT_ANGLE_CTRL: handle_joint_angle_ctrl,
            JsonCmd.JOINTS_ANGLE_CTRL: handle_joints_angle_ctrl,
            JsonCmd.GRIPPER_MODE_SET: handle_gripper_mode_set,
            JsonCmd.POSE_CTRL: handle_pose_ctrl,
            JsonCmd.WIFI_ON_BOOT: handle_wifi_on_boot,
            JsonCmd.AP_SET: handle_ap_or_sta_set,
            JsonCmd.STA_SET: handle_ap_or_sta_set,
            JsonCmd.APSTA_SET: handle_ap_sta_set,
            JsonCmd.WIFI_CONFIG_CREATE_BY_INPUT: handle_ap_sta_set
        }

        if genre:
            command = {"T": genre}   
                         
        if command_data:
            if genre in switch_dict:
                command = switch_dict[genre](self.type,command,command_data) 
                
        elif not command_data:
            command = command     
                                   
        real_command = self._flatten(command)
        return real_command
        
    def _flatten(self, lst):
        flat_list = json.dumps(lst) + "\n"
        flat_list = flat_list.encode()
        return flat_list
        
    def _process_data_command(self,args):
        if not args:
            return []
        processed_args = []
        for index in range(len(args)):
            if isinstance(args[index], list):
                processed_args.extend(args[index])
            else:
                processed_args.append(args[index])

        return processed_args
    
    def _process_received(self, data, genre): 
        if not data:
            return None
        print(data)  
        switch_dict = {
            "roarm_m2": handle_m2_feedback,
            "roarm_m3": handle_m3_feedback
        }                
        res = []      
        valid_data = []      
        if genre == JsonCmd.FEEDBACK_GET:   
            valid_data.append(data['x'])    
            valid_data.append(data['y'])
            valid_data.append(data['z'])             
            if self.type in switch_dict:
                valid_data = switch_dict[self.type](valid_data,data)                                   
        else: 
            valid_data = data  
        res.append(valid_data)            
        return res

def write(self, command, method=None):
    if method == "http":
        log_command = ""
        for i in command:
            if isinstance(i, str):
                log_command += i
            else:
                log_command += hex(i)[2:] + " "
        # self.log.debug("_write: {}".format(log_command))

        self.sock.sendall(command)
    else:
        self._serial_port.reset_input_buffer()
        command_log = ""
        for i in command:
            if isinstance(i, str):
                command_log += i[2:] + " "
            else:
                command_log += hex(i)[2:] + " "
        #self.log.debug("_write: {}".format(command_log))
        self._serial_port.write(command)
        self._serial_port.flush()

def read(self, genre):
    if genre != JsonCmd.FEEDBACK_GET:
        request_data = json.dumps({'T': 105}) + "\n"      
        self._serial_port.write(request_data.encode())    

    if self.base_controller is None:
        self.base_controller = BaseController(port=self._serial_port, roarm_type=self.type)  

    data = self.base_controller.feedback_data()
    if data:
        # self.log.debug("_read : {}".format(data))
        return data