# roarm_m2

## Python API 使用说明

```python
from roarm_sdk.roarm import roarm

# 串口通信示例
roarm = roarm(roarm_type="roarm_m2", port="/dev/ttyUSB0", baudrate=115200)

# Http通信示例
# 注意：http通信需要先连接在同一个wifi下，host为机械臂的ip地址
#roarm = roarm(roarm_type="roarm_m2", host="192.168.4.1")

# 获取所有关节当前的角度
value = roarm.joints_angle_get()
print(value)

# 将 关节1 移动到 90度，速度设置为 1000步/s，加速度设置为 50步/s^2
roarm.joint_angle_ctrl(joint=1,angle=90,speed=1000,acc=50)
```
### 1. 整体运行状态

#### `echo_set(cmd)`

- **功能:** 设置回声模式

- **参数:**
  - `cmd:` [0, 1], type : int
  - 0: 关闭回声模式

  - 1: 开启回声模式

#### `middle_set()`

- **功能:** 将当前位置校准为中位

#### `move_init()`

- **功能:** 移动到初始位置

### `led_ctrl(led)`
- **功能:** 设置LED灯的状态

- **参数:**
  - `led:` [0, 255], type : int
  - 0: 最暗
  
  - 255: 最亮

#### `torque_set(cmd)`
- **功能:** 设置所有关节的力矩是否开启

- **参数:**
  - `cmd:` [0, 1], type : int
  - 0: 关闭所有关节的力矩

  - 1: 开启所有关节的力矩

#### `dynamic_adaptation_set(mode, torques)`
- **功能:** 设置所有关节的力矩自适应模式

- **参数:**
  - `mode:` [0, 1], type : int
  - 0: 关闭力矩自适应模式

  - 1: 开启力矩自适应模式

  - `torques:` [0, 1000], type : list[int]，unit : 0.1%，即堵转扭矩的百分比，1000是100%
  - [关节1力矩阈值, 关节2力矩阈值, 关节3力矩阈值, 关节4力矩阈值]

  - 力矩自适应模式下的力矩阈值，超过这个阈值关节随外力转动

####  `feedback_get()`
- **功能:** 获取所有关节的反馈信息

- **返回值:** list[float]
  - [坐标x, 坐标y, 坐标z,关节1弧度, 关节2弧度, 关节3弧度, 关节4弧度, 关节1力矩, 关节2力矩, 关节3力矩, 关节4力矩]

  - 坐标unit : mm，弧度unit : rad，力矩unit : 0.1%，即堵转扭矩的百分比，1000是100%

### 2. 关节控制

#### `joint_radian_ctrl(joint, radian, speed, acc)`
- **功能:** 将指定关节移动到指定弧度

- **参数:**
  - `joint:` [1, 4], type : int
  - `radian:` type : float，unit : rad
  - 1: 关节1 ，[-3.1415926, 3.1415926]
  - 2: 关节2，[-1.5707963, 1.5707963]
  - 3: 关节3，[-0.8726646, 3.1415926]
  - 4: 关节4，[0, 1.5707963]

  - `speed:` [1, 4096], type : int，unit : 步/s
  - `acc:` [1, 254], type : int，unit : 步/s^

#### `joints_radian_ctrl(radians, speed, acc)`
- **功能:** 将所有关节移动到指定弧度

- **参数:**
  - `radians:` type : list[float]
  - [关节1弧度, 关节2弧度, 关节3弧度, 关节4弧度]
  - 1: 关节1 ，[-3.1415926, 3.1415926]
  - 2: 关节2，[-1.5707963, 1.5707963]
  - 3: 关节3，[-0.8726646, 3.1415926]
  - 4: 关节4，[0, 1.5707963]

  - `speed:` [1, 4096], type : int，unit : 步/s
  - `acc:` [1, 254], type : int，unit : 步/s^2

#### `joints_radian_get()`
- **功能:** 获取所有关节的弧度

- **返回值:** list[float], unit : rad
  - [关节1弧度, 关节2弧度, 关节3弧度, 关节4弧度]

#### `joint_angle_ctrl(joint, angle, speed, acc)`
- **功能:** 将指定关节移动到指定角度

- **参数:**
  - `joint:` [1, 4], type : int
  - `angle:` type : float，unit : 度
  - 1: 关节1，[-180, 180]
  - 2: 关节2，[-90, 90]
  - 3: 关节3，[-50, 180]
  - 4: 关节4，[0， 90]

  - `speed:` [1, 4096], type : int，unit : 步/s
  - `acc:` [1, 254], type : int，unit : 步/s^2

#### `joints_angle_ctrl(angles, speed, acc)`
- **功能:** 将所有关节移动到指定角度

- **参数:**
  - `angles:` type : list[float]
  - [关节1角度, 关节2角度, 关节3角度, 关节4角度]
  - 1: 关节1，[-180, 180]
  - 2: 关节2，[-90, 90]
  - 3: 关节3，[-50, 180]
  - 4: 关节4，[0， 90]

  - `speed:` [1, 4096], type : int，unit : 步/s
  - `acc:` [1, 254], type : int，unit : 步/s^2

#### `joints_angle_get()`
- **功能:** 获取所有关节的角度

- **返回值:** list[float], unit : 度
  - [关节1角度, 关节2角度, 关节3角度, 关节4角度]

#### `drag_teach_start(filename)`
- **功能:** 开始拖拽教学

- **参数:**
  - `filename:` filename, type : str

#### `drag_teach_replay(filename)`
- **功能:** 播放拖拽教学

- **参数:**
  - `filename:` filename, type : str

### 3. 夹爪控制

#### `gripper_mode_set(mode)`
- **功能:** 设置夹爪模式

- **参数:**
  - `mode:` [0, 1], type : int
  - 0: 夹爪模式
  - 1: 手腕模式

#### `gripper_radian_ctrl(radian, speed, acc)`
- **功能:** 将夹爪移动到指定弧度

- **参数:**
  - `radian:` [0, 1.5707963], type : float，unit : rad

  - `speed:` [1, 4096], type : int，unit : 步/s

  - `acc:` [1, 254], type : int，unit : 步/s^2

#### `gripper_angle_ctrl(angle, speed, acc)`
- **功能:** 将夹爪移动到指定角度

- **参数:**
  - `angle:` [0, 90], type : float，unit : 度

  - `speed:` [1, 4096], type : int，unit : 步/s

  - `acc:` [1, 254], type : int，unit : 步/s^2

#### `gripper_radian_get()`
- **功能:** 获取夹爪的弧度

- **返回值:** float，unit : rad

#### `gripper_angle_get()`
- **功能:** 获取夹爪的角度

- **返回值:** float，unit : 度

### 4. 位置控制

#### `pose_ctrl(pose)`
- **功能:** 移动到指定位置

- **参数:**
  - `pose:` type : list[float]

  - [坐标x, 坐标y, 坐标z, 夹爪角度]

  - 坐标unit : mm，角度unit : 度

#### `pose_get()`
- **功能:** 获取当前位置

- **返回值:** list[float]
  - [坐标x, 坐标y, 坐标z, 夹爪角度]
  - 坐标unit : mm，角度unit : 度

### 5. WiFi控制

#### `wifi_on_boot(wifi_cmd)`
- **功能:** 设置启动时WiFi模式

- **参数:**
  - `wifi_cmd:` [0, 3], type : int
  - 0: 关闭WiFi

  - 1: AP模式

  - 2: STA模式

  - 3: AP+STA模式

#### `ap_set(ssid, password)`
- **功能:** 设置AP模式下的WiFi名称和密码

- **参数:**
  - `ssid:` type : str

  - `password:` type : str

#### `sta_set(ssid, password)`
- **功能:** 设置STA模式下的WiFi名称和密码
- **参数:**
  - `ssid:` type : str

  - `password:` type : str

#### `apsta_set(ap_ssid, ap_password, sta_ssid, sta_password)`
- **功能:** 设置AP+STA模式下的WiFi名称和密码

- **参数:**
  - `ap_ssid:` type : str

  - `ap_password:` type : str

  - `sta_ssid:` type : str

  - `sta_password:` type : str

#### `wifi_config_creat_by_status()`
- **功能:** 根据当前WiFi状态生成WiFi配置文件

#### `wifi_config_creat_by_input(ap_ssid, ap_password, sta_ssid, sta_password)`
- **功能:** 根据输入生成WiFi配置文件

- **参数:**
  - `ap_ssid:` type : str

  - `ap_password:` type : str

  - `sta_ssid:` type : str

  - `sta_password:` type : str

#### `wifi_stop()`
- **功能:** 关闭WiFi