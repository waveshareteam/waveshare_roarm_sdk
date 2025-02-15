# coding=utf-8

import sys
import logging
import time
import math

from roarm_sdk.logger import setup_logging
from roarm_sdk.utils import calibration_parameters
from roarm_sdk.common import JsonCmd, DataProcessor


class CommandGenerator(DataProcessor):

    def __init__(self, roarm_type=None, debug=False):
        """
        Args:
            roarm_type : "roarm_m2" or "roarm_m3, type : str
            debug : whether show debug info
        """
        self.type = roarm_type
        self.debug = debug
        setup_logging(self.debug)
        self.log = logging.getLogger(__name__)
        self.calibration_parameters = calibration_parameters
                
    def echo_set(self, cmd):
        """Set echo 
        Args:
            cmd : [0,1], type : int
            0 : disable echo
            1  : enable echo
        """
        self.calibration_parameters(roarm_type=self.type, cmd=cmd)
        return self._mesg(JsonCmd.ECHO_SET, cmd)
    
    def middle_set(self):
        """Set current position to neutral calibration 
        """
        return self._mesg(JsonCmd.MIDDLE_SET, 254)
                
    def move_init(self):
        """Move roarm to home position
        """
        switch_dict = {
        "roarm_m2": [0, 0, 1.5708, 0],
        "roarm_m3": [0, 0, 1.5708, 0, 0, 0],
        }
        radians = switch_dict[self.type]
        self.joints_radian_ctrl(radians=radians,speed=100,acc=0)
        return 1  

    def led_ctrl(self, led):
        """Ctrl led brightness
        Args:
            led : [0,255], type : int
            0: darkest
            255: brightest
        """
        self.calibration_parameters(roarm_type=self.type, led=led)
        return self._mesg(JsonCmd.LED_CTRL, led)
                 
    def torque_set(self, cmd):
        """Set torque
        Args:
            cmd : [0,1], type : int
            0 : disable torque
            1  : enable torque
        """
        self.calibration_parameters(roarm_type=self.type, cmd=cmd)        
        return self._mesg(JsonCmd.TORQUE_SET, cmd)
        
    def dynamic_adaptation_set(self, mode, torques):
        """Set dynamic adaptation
        Args:
            mode: [0,1], type : int
            0: disable
            1: enable
            torque : [1,1000], type : list[int]
        """
        self.calibration_parameters(roarm_type=self.type, mode=mode, torques=torques)
        return self._mesg(JsonCmd.DYNAMIC_ADAPTATION_SET, mode, torques)
        
    def feedback_get(self):
        """Get feedback
        Return:
            list: a list of roarm feedback, type : List[float]
        """
        return self._mesg(JsonCmd.FEEDBACK_GET)

    def joint_radian_ctrl(self, joint, radian, speed, acc):
        """Send one radian of joint to robot arm
        Args:
            joint : id, type : int
            radian : value, type : float
            speed : [1,4096], type : int
            acc : [1,254], type : int
        """
        self.calibration_parameters(roarm_type=self.type, joint=joint, radian=radian, speed=speed, acc=acc)
        return self._mesg(JsonCmd.JOINT_RADIAN_CTRL, joint, radian, speed, acc)

    def joints_radian_ctrl(self, radians, speed, acc):
        """Send the radians of all joints to robot arm
        Args:
            radians: a list of radians, type : List[float]
            speed : [1,4096], type : int
            acc : [1,254], type : int
        """
        self.calibration_parameters(roarm_type=self.type, radians=radians, speed=speed, acc=acc)
        return self._mesg(JsonCmd.JOINTS_RADIAN_CTRL, radians, speed, acc)
        
    def joints_radian_get(self):
        """ Get the radian of all joints
        Return:
            list: a list of all radians, type : List[float]
        """
        value = self.feedback_get()
        switch_dict = {
            "roarm_m2": value[3:7],
            "roarm_m3": value[4:10],
        }
        radians = switch_dict[self.type]
        return radians

    def joint_angle_ctrl(self, joint, angle, speed, acc):
        """Send one angle of joint to robot arm
        Args:
            joint : id, type : int
            angle : value, type : float
            speed : [1,4096], type : int
            acc : [1,254], type : int
        """
        self.calibration_parameters(roarm_type=self.type, joint=joint, angle=angle, speed=speed, acc=acc)
        return self._mesg(JsonCmd.JOINT_ANGLE_CTRL, joint, angle, speed, acc)

    def joints_angle_ctrl(self, angles, speed, acc):
        """Send the angles of all joints to robot arm
        Args:
            angles: a list of angles, type : List[float]
            speed : [1,4096], type : int
            acc : [1,254], type : int
        """
        self.calibration_parameters(roarm_type=self.type, angles=angles, speed=speed, acc=acc)
        return self._mesg(JsonCmd.JOINTS_ANGLE_CTRL, angles, speed, acc)

    def joints_angle_get(self):
        """ Get the angle of all joints
        Return:
            list: a list of all angles, type : List[float]
        """
        value = self.feedback_get()
        switch_dict = {
            "roarm_m2": value[3:7],
            "roarm_m3": value[4:10],
        }
        radians = switch_dict[self.type]    
        angles = [(radian * 180 / math.pi) for radian in radians]
        return angles

    def gripper_mode_set(self, mode):
        """Set gripper mode        
        Args:
            mode : [0,1], type : int
            0 : gripper
            1 : wrist
        """
        self.calibration_parameters(roarm_type=self.type, mode=mode)
        return self._mesg(JsonCmd.GRIPPER_MODE_SET, mode) 
        
    def gripper_radian_ctrl(self, radian, speed, acc):
        """Set gripper radian
        Args:
            radian: [0,1.57], type : float
            speed: [1,4096], type : int
            acc: [1,254], type : int
        """
        switch_dict = {
            "roarm_m2": 4,
            "roarm_m3": 6,
        }
        gripper = switch_dict[self.type]
        self.joint_radian_ctrl(joint=gripper,radian=radian,speed=speed,acc=acc) 
        return 1
        
    def gripper_angle_ctrl(self, angle, speed, acc):
        """Set gripper angle
        Args:
            angle: [0,90], type : float
            speed: [1,4096], type : int
            acc: [1,254], type : int
        """
        switch_dict = {
            "roarm_m2": 4,
            "roarm_m3": 6,
        }
        gripper = switch_dict[self.type]        
        self.joint_angle_ctrl(joint=gripper,angle=angle,speed=speed,acc=acc) 
        return 1        
                        
    def gripper_radian_get(self):
        """Get the radian of gripper
        Return:
            gripper radian, type : float
        """
        switch_dict = {
            "roarm_m2": 6,
            "roarm_m3": 9,
        }
        gripper = switch_dict[self.type]        
        value = self.feedback_get()
        radian = value[gripper]
        return radian

    def gripper_angle_get(self):
        """Get the angle of gripper
        Return:
            gripper angle, type : float
        """
        switch_dict = {
            "roarm_m2": 6,
            "roarm_m3": 9,
        }
        gripper = switch_dict[self.type]                 
        value =  self.feedback_get()
        angle = (value[gripper]*180)/math.pi
        return angle
        
    def pose_ctrl(self, pose):
        """Ctrl pose
        Args:
            pose: a list of coords value, type : List[float]
        """
        self.calibration_parameters(roarm_type=self.type, pose=pose)
        return self._mesg(JsonCmd.POSE_CTRL, pose)
        
    def pose_get(self):
        """Get the pose from robot arm, coordinate system based on base
        Return:
            list : a list of coords value, type : List[float] 
        """  
        poses = []               
        value =  self.feedback_get() 
        value.extend([0] * (20 - len(value)))       
        switch_dict = {
            "roarm_m2": value[0:3] + [value[6]],
            "roarm_m3": value[0:4] + [value[8], value[9]],
        }      
        poses = switch_dict[self.type]                    
        poses[3:] = [(pose * 180 / math.pi) for pose in poses[3:]] 
        return poses
        
    def wifi_on_boot(self, wifi_cmd):
        """Set wifi mode        
        Args:
            wifi_cmd : [0,3], type : int
            0 : WIFI close
            1 : AP model
            2 : STA model
            3 : AP + STA model
        """
        self.calibration_parameters(roarm_type=self.type, wifi_cmd=wifi_cmd)
        return self._mesg(JsonCmd.WIFI_ON_BOOT, wifi_cmd) 

    def ap_set(self, ssid, password):
        """Set ap
        Args:
            ssid : wifi ssid, type : str
            password : wifi password, type : str
        """
        self.calibration_parameters(roarm_type=self.type, ssid=ssid, password=password)
        return self._mesg(JsonCmd.AP_SET, ssid, password)

    def sta_set(self, ssid, password):
        """Set sta
        Args:
            ssid : new wifi ssid, type : str
            password : wifi password, type : str
        """
        self.calibration_parameters(roarm_type=self.type, ssid=ssid, password=password)
        return self._mesg(JsonCmd.STA_SET, ssid, password)

    def apsta_set(self, ap_ssid, ap_password, sta_ssid, sta_password):
        """Set ap + sta
        Args:
            ap_ssid : wifi ssid, type : str
            ap_password : wifi password, type : str
            sta_ssid : wifi ssid, type : str
            sta_password : wifi password, type : str          
        """
        self.calibration_parameters(roarm_type=self.type, ssid=ap_ssid, password=ap_password)
        self.calibration_parameters(roarm_type=self.type, ssid=sta_ssid, password=sta_password)
        return self._mesg(JsonCmd.APSTA_SET, ap_ssid, ap_password, sta_ssid, sta_password)                   

    def wifi_config_creat_by_status(self):
        """Save wifi config by status
        """
        return self._mesg(JsonCmd.WIFI_CONFIG_CREATE_BY_STATUS)   
        
    def wifi_config_creat_by_input(self, ap_ssid, ap_password, sta_ssid, sta_password):
        """Save wifi config by input
        Args:
            ap_ssid : wifi ssid, type : str
            ap_password : wifi password, type : str
            sta_ssid : wifi ssid, type : str
            sta_password : wifi password, type : str         
        """
        self.calibration_parameters(roarm_type=self.type, ssid=ap_ssid, password=ap_password)
        self.calibration_parameters(roarm_type=self.type, ssid=sta_ssid, password=sta_password)
        return self._mesg(JsonCmd.WIFI_CONFIG_CREATE_BY_INPUT, ap_ssid, ap_password, sta_ssid, sta_password)        
                        
    def wifi_stop(self):
        """Stop wifi
        """
        return self._mesg(JsonCmd.WIFI_STOP)
                