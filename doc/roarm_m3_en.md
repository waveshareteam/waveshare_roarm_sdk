# roarm_m3

## Python API Instructions for use

```python
from roarm_sdk.roarm import roarm
# Serial communication example
roarm = roarm(roarm_type="roarm_m3", port="/dev/ttyUSB0", baudrate=115200)

# Http communication example
# Note: HTTP communication needs to be connected to the same wifi first, and host is the IP address of the robotic arm.
#roarm = roarm(roarm_type="roarm_m3", host="192.168.4.1")

# Get the current angles of all joints
value = roarm.joints_angle_get()
print(value)

# Move joint 1 to 90 degrees, set the speed to 1000 step/s, and set the acceleration to 50 steps/s^2
roarm.joint_angle_ctrl(joint=1,angle=90,speed=1000,acc=50)
```
### 1. Overall operating status

#### `echo_set(cmd)`

- **Function:** Set echo mode

- **Parameters:** 
  - `cmd:` [0, 1], type : int

  - 0: Turn off echo mode
  
  - 1: Turn on echo mode

#### `middle_set()`

- **Function:** Calibrate current position to neutral

#### `move_init()`

- **Function:** Move to initial position

### `led_ctrl(led)`
- **Function:** Ctrl led brightness

- **Parameters:**
  - `led:` [0, 255], type : int
  - 0: darkest
  
  - 255: brightest

#### `torque_set(cmd)`
- **Function:** Set whether the torque of all joints is turned on

- **Parameters:**
  - `cmd:` [0, 1], type : int
  - 0: Turn off all joint moments
  - 1: Turn on torque for all joints

#### `dynamic_adaptation_set(mode, torques)`
- **Function:** Set the torque adaptive mode of all joints

- **Parameters:**
  - `mode:` [0, 1], type : int
  - 0: Turn off torque adaptive mode
  - 1: Turn on torque adaptive mode
  - `torques:` [0, 1000], type : list[int]，unit : 0.1%, which is the percentage of stalled torque. 1000 is 100%.

  -[Joint 1 torque threshold, Joint 2 torque threshold, Joint 3 torque threshold, Joint 4 torque threshold, Joint 5 torque threshold, Joint 6 torque threshold]

  -Torque threshold in torque adaptive mode, beyond which the joint rotates with external force

####  `feedback_get()`
- **Function:** Get feedback from all joints

- **Return:** list[float]
  - [Coordinate x, coordinate y, coordinate z, pitch, joint 1 radian, joint 2 radian, joint 3 radian, joint 4 radian, joint 5 radian, joint 6 radian, joint 1 torque, joint 2 torque, joint 3 torque, joint 4 torque, joint 5 torque, joint 6 torque]

  - coordinate unit : mm, radian unit : rad, torque unit : 0.1%，That is, the percentage of stalled torque, 1000 is 100%

### 2. Joint control

#### `joint_radian_ctrl(joint, radian, speed, acc)`
- **Function:** Move the specified joint to the specified radian

- **Parameters:**
  - `joint:` [1, 4], type : int

  - `radian:` type : float，unit : rad
  - 1: joint 1，[-3.1415926, 3.1415926]
  - 2: joint 2, [-1.5707963, 1.5707963]
  - 3: joint 3，[-0.8726646, 3.1415926]
  - 4: joint 4, [-1.5707963, 1.5707963]
  - 5: joint 5, [-3.1415926, 3.1415926]
  - 6: joint 6, [0, 1.5707963]

  - `speed:` [1, 4096], type : int，unit : step/s

  - `acc:` [1, 254], type : int，unit : step/s^

#### `joints_radian_ctrl(radians, speed, acc)`
- **Function:** Move all joints to a specified radian

- **Parameters:**
  - `radians:` type : list[float]
  - [Joint 1 radians, Joint 2 radians, Joint 3 radiansans, Joint 3 radians, Joint 4 radians]
  - 1: joint 1，[-3.1415926, 3.1415926]
  - 2: joint 2，[-1.5707963, 1.5707963]
  - 3: joint 3，[-0.8726646, 3.1415926]
  - 4: joint 4，[-1.5707963, 1.5707963]
  - 5: joint 5，[-3.1415926, 3.1415926]
  - 6: joint 6，[0, 1.5707963]

  - `speed:` [1, 4096], type : int，unit : step/s

  - `acc:` [1, 254], type : int，unit : step/s^2

#### `joints_radian_get()`
- **Function:** Get the radians of all joints

- **Return:** list[float], unit : rad
  - [Joint 1 radian, Joint 2 radian, Joint 3 radian, Joint 4 radian]

#### `joint_angle_ctrl(joint, angle, speed, acc)`
- **Function:** Move the specified joint to the specified angle

- **Parameters:**
  - `joint:` [1, 4], type : int

  - `angle:` type : float，unit : degree
  - 1: joint 1，[-180, 180]
  - 2: joint 2，[-90, 90]
  - 3: joint 3，[-50, 180]
  - 4: joint 4，[-90, 90]
  - 5: joint 5，[-180, 180]
  - 6: joint 6，[0, 90]

  - `speed:` [1, 4096], type : int，unit : step/s

  - `acc:` [1, 254], type : int，unit : step/s^2

#### `joints_angle_ctrl(angles, speed, acc)`
- **Function:** Move all joints to specified angles

- **Parameters:**
  - `angles:` type : list[float]
  - [joint1 angle, joint2 angle, joint3 angle, joint4 angle]
  - 1: joint 1，[-180, 180]
  - 2: joint 2，[-90, 90]
  - 3: joint 3，[-50, 180]
  - 4: joint 4，[-90, 90]
  - 5: joint 5，[-180, 180]
  - 6: joint 6，[0, 90]

  - `speed:` [1, 4096], type : int，unit : step/s

  - `acc:` [1, 254], type : int，unit : step/s^2

#### `joints_angle_get()`
- **Function:** Get the angles of all joints

- **Return:** list[float], unit : degree
  - [joint1 angle, joint2 angle, joint3 angle, joint4 angle]

#### `drag_teach_start(filename)`
- **Function:** Start dragging tutorial

- **Parameters:**
  - `filename:` filename, type : str

#### `drag_teach_replay(filename)`
- **Function:** Play drag and drop tutorial

- **Parameters:**
  - `filename:` filename, type : str

### 3. Gripper control

#### `gripper_radian_ctrl(radian, speed, acc)`
- **Function:** Move the gripper to a specified radian

- **Parameters:**
  - `radian:` [0, 1.5707963], type : float，unit : rad

  - `speed:` [1, 4096], type : int，unit : step/s

  - `acc:` [1, 254], type : int，unit : step/s^2

#### `gripper_angle_ctrl(angle, speed, acc)`
- **Function:** Move the gripper to a specified angle

- **Parameters:**
  - `angle:` [0, 90], type : float，unit : degree

  - `speed:` [1, 4096], type : int，unit : step/s

  - `acc:` [1, 254], type : int，unit : step/s^2

#### `gripper_radian_get()`
- **Function:** Get the radian of the gripper

- **Return:** float, unit : rad

#### `gripper_angle_get()`
- **Function:** Get the angle of the gripper

- **Return:** float, unit : degree

### 4. Position control

#### `pose_ctrl(pose)`
- **Function:** Move to specified position

- **Parameters:**
  - `pose:` type : list[float]
  - [coordinate x, coordinate y, coordinate z, pitch, roll, gripper angle]

  - coordinate unit: mm, angle unit : degrees 

#### `pose_get()`
- **Function:** Get current position

- **Return:** list[float]
 - [coordinate x, coordinate y, coordinate z, pitch, roll, gripper angle]

 - coordinate unit: mm, angle unit : degrees 

### 5. WiFi control

#### `wifi_on_boot(wifi_cmd)`
- **Function:** Set WiFi mode at startup

- **Parameters:**
  - `wifi_cmd:` [0, 3], type : int
  - 0: Turn off WiFi

  - 1: AP mode
  
  - 2: STA mode
  
  - 3: AP+STA mode

#### `ap_set(ssid, password)`
- **Function:** Set WiFi name and password in AP mode

- **Parameters:**
  - `ssid:` type : str

  - `password:` type : str

#### `sta_set(ssid, password)`
- **Function:** Set WiFi name and password in STA mode
- **Parameters:**
  - `ssid:` type : str
  
  - `password:` type : str

#### `apsta_set(ap_ssid, ap_password, sta_ssid, sta_password)`
- **Function:** Set WiFi name and password in AP+STA mode

- **Parameters:**
  - `ap_ssid:` type : str
  
  - `ap_password:` type : str
  
  - `sta_ssid:` type : str
  
  - `sta_password:` type : str

#### `wifi_config_creat_by_status()`
- **Function:** Generate WiFi configuration file based on current WiFi status

#### `wifi_config_creat_by_input(ap_ssid, ap_password, sta_ssid, sta_password)`
- **Function:** Generate WiFi configuration file based on input

- **Parameters:**
  - `ap_ssid:` type : str

  - `ap_password:` type : str

  - `sta_ssid:` type : str

  - `sta_password:` type : str

#### `wifi_stop()`
- **Function:** Turn off WiFi