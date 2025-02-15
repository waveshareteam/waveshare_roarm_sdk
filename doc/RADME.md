# roarm_sdk

**This is python api for Waveshare roarm product**

We support Python2, Python3.5 or later.

[roarm_m2 api 说明](./roarm_m2_zh.md) | [roarm_m2 api Description](./roarm_m2_en.md)

[roarm_m3 api 说明](./roarm_m3_zh.md) | [roarm_m3 api Description](./roarm_m3_en.md)

<details>
<summary>Catalogue:</summary>

<!-- vim-markdown-toc GFM -->

- [roarm_sdk](#roarm_sdk)
    - [roarm](#roarm)
        - [echo_set(cmd)](#echo_setcmd)
        - [middle_set()](#middle_set)
        - [move_init()](#move_init)
        - [led_ctrl(led)](#led_ctrlled)
        - [breath_led(duration,steps)](#breath_ledduration-steps)
        - [torque_set(cmd)](#torque_setcmd)
        - [dynamic_adaptation_set(mode,torques)](#dynamic_adaptationset-mode-torques)
        - [feedback_get()](#feedbackget)
        - [joint_radian_ctrl(joint,radian,speed,acc)](#joint_radian_ctrljointradianspeedacc)
        - [joints_radian_ctrl(radians,speed,acc)](#joints_radian_ctrlradianspeedacc)
        - [joints_radian_get()](#joints_radian_get)
        - [joint_angle_ctrl(joint,angle,speed,acc)](#joint_angle_ctrljointanglespeedacc)
        - [joints_angle_ctrl(angles,speed,acc)](#joints_angle_ctrlanglespeedacc)
        - [joints_angle_get()](#joints_angle_get)
        - [gripper_mode_set(mode)](#gripper_mode_setmode)
        - [gripper_radian_ctrl(radian,speed,acc)](#gripper_radian_ctrlradianspeedacc)
        - [gripper_angle_ctrl(angle,speed,acc)](#gripper_angle_ctrlanglespeedacc)
        - [gripper_radian_get()](#gripper_radian_get)
        - [gripper_angle_get()](#gripper_angle_get)
        - [pose_ctrl(pose)](#pose_ctrlpose)
        - [pose_get()](#pose_get)
        - [drag_teach_start(filename)](#drag_teachstartfilename)
        - [drag_teach_replay(filename)](#drag_teachreplayfilename)
        - [wifi_on_boot(wifi_cmd)](#wifi_on_bootwifi_cmd)
        - [ap_set(ssid,password)](#ap_setssidpassword)
        - [sta_set(ssid,password)](#sta_setssidpassword)
        - [apsta_set(ap_ssid,ap_password,sta_ssid,sta_password)](#apstasetap_ssidap_passwordstassidsta_password)
        - [wifi_info_get()](#wifi_info_get)
        - [wifi_config_creat_by_status()](#wifi_config_creat_by_status)
        - [wifi_config_creat_by_input(ap_ssid,ap_password,sta_ssid,sta_password)](#wifi_config_creat_by_inputap_ssidap_passwordstassidsta_password)
        - [wifi_stop()](#wifi_stop)
        - [disconnect()](#disconnect)

<!-- vim-markdown-toc -->
</details>

# roarm

### echo_set(cmd)

Set echo 
    0 : disable echo
    1  : enable echo
* **Parameters**

  * **cmd** –  : [0,1], type : int

### middle_set()

Set current position to neutral calibration

### move_init()

Move roarm to home position

### led_ctrl(led)

Ctrl led brightness
* **Parameters**

  * **led** –  : [0,255], type : int

        0: darkest
        255: brightest

### breath_led(duration,steps)

Set breath_led
* **Parameters**

  * **duration** –  : breath duration, type : float

  * **steps** –  : breath steps, type : int

### torque_set(cmd)

Set the torque of the robot
* **Parameters**

  * **cmd** –  : [0,1], type : int

        0: disable torque
        1: enable torque

### dynamic_adaptation_set(mode,torques)

Set the dynamic adaptation of the robot
* **Parameters**

  * **mode** –  : [0,1], type : int

        0: disable dynamic adaptation
        1: enable dynamic adaptation

  * **torques** –  : [0,1000], type : list

### feedback_get()

Get the feedback of the robot
* **Returns**

  * **list** –  : a list of roarm feedback, type : List[float]

### joint_radian_ctrl(joint,radian,speed,acc)

Control the joint radian of the robot
* **Parameters**

  * **joint** –  : id, type : int

  * **radian** –  : value, type : float

  * **speed** –  : [1,4096], type : int

  * **acc** –  : [1,254], type : int  

### joints_radian_ctrl(radians,speed,acc)

Control the joints radian of the robot
* **Parameters**

  * **radians** –  : a list of radian, type : List[float]

  * **speed** –  : [1,4096], type : int

  * **acc** –  : [1,254], type : int  

### joints_radian_get()

Get the joints radian of the robot
* **Returns**

  * **list** –  : a list of all radians, type : List[float]

### joint_angle_ctrl(joint,angle,speed,acc)

Control the joint angle of the robot
* **Parameters**

  * **joint** –  : id, type : int

  * **angle** –  : value, type : float

  * **speed** –  : [1,4096], type : int

  * **acc** –  : [1,254], type : int  

### joints_angle_ctrl(angles,speed,acc)

Control the joints angle of the robot
* **Parameters**

  * **angles** –  : a list of angle, type : List[float]

  * **speed** –  : [1,4096], type : int

  * **acc** –  : [1,254], type : int  

### joints_angle_get()

Get the joints angle of the robot
* **Returns**

  * **list** –  : a list of all angles, type : List[float]

### drag_teach_start(filename)

Start the drag teach of the robot
* **Parameters**

  * **filename** –  : filename, type : str

### drag_teach_replay(filename)

Replay the drag teach of the robot
* **Parameters**

  * **filename** –  : filename, type : str
  
### gripper_mode_set(mode)

Set the gripper mode of the robot
* **Parameters**

  * **mode** –  : [0,1], type : int

        0: gripper
        1: wrist

### gripper_radian_ctrl(radian,speed,acc)

Control the gripper radian of the robot
* **Parameters**

  * **radian** –  : value, type : float

  * **speed** –  : [1,4096], type : int

  * **acc** –  : [1,254], type : int  

### gripper_angle_ctrl(angle,speed,acc)

Control the gripper angle of the robot
* **Parameters**

  * **angle** –  : value, type : float

  * **speed** –  : [1,4096], type : int

  * **acc** –  : [1,254], type : int

### gripper_radian_get()

Get the gripper radian of the robot
* **Returns**

  * **float** –  : gripper radian, type : float

### gripper_angle_get()

Get the gripper angle of the robot
* **Returns**

  * **float** –  : gripper angle, type : float

### pose_ctrl(pose)

Control the pose of the robot
* **Parameters**

  * **pose** –  : a list of coords value, type : List[float]

### pose_get()

Get the pose of the robot
* **Returns**

  * **list** –  : a list of coords value, type : List[float]

### wifi_on_boot(wifi_cmd)

Set the wifi on boot of the robot
* **Parameters**

  * **wifi_cmd** –  : [0,3], type : int

        0 : WIFI close
        1 : AP model
        2 : STA model
        3 : AP + STA model

### ap_set(ssid,password)

Set the ap of the robot
* **Parameters**

  * **ssid** –  : ssid, type : str

  * **password** –  : password, type : str

### sta_set(ssid,password)

Set the sta of the robot
* **Parameters**

  * **ssid** –  : ssid, type : str

  * **password** –  : password, type : str

### apsta_set(ap_ssid,ap_password,sta_ssid,sta_password)

Set the apsta of the robot
* **Parameters**

  * **ap_ssid** –  : ap ssid, type : str

  * **ap_password** –  : ap password, type : str

  * **sta_ssid** –  : sta ssid, type : str

  * **sta_password** –  : sta password, type : str

### wifi_config_creat_by_status()

Creat the wifi config by status of the robot

### wifi_config_creat_by_input(ap_ssid,ap_password,sta_ssid,sta_password)

Creat the wifi config by input of the robot

### wifi_stop()

Stop the wifi of the robot

### disconnect()

Disconnect the roarm

# Example

More demo can go to [here](../demo).