# coding=utf-8

from __future__ import division
import time
import threading
import serial
import requests
import json

from roarm_sdk.generate import CommandGenerator
from roarm_sdk.common import JsonCmd, write, read
from roarm_sdk.utils import calibration_parameters


class roarm(CommandGenerator):
    """
    Roarm Python API communication class.
    """
    def __init__(self, roarm_type=None, port=None, baudrate=115200, host=None, timeout=0.1, debug=False, thread_lock=True):
        """
        Args:
            roarm_type    : port string
            port          : port string
            baudrate      : baud rate string, default '115200'
            host          : host string
            timeout       : default 0.1
            debug         : whether show debug info
        """
        self.type = roarm_type
        super(roarm, self).__init__(self.type,debug)
        self.calibration_parameters = calibration_parameters
        self.thread_lock = thread_lock
        self.host =None            
        self.stop_flag = False
        self.base_controller = None

        if thread_lock:
            self.lock = threading.Lock()
        if host:
            self.host = host
        else:    
            self._serial_port = serial.Serial()
            self._serial_port.port = port
            self._serial_port.baudrate = baudrate
            self._serial_port.timeout = timeout
            self._serial_port.rts = False
            self._serial_port.open() 

    _write = write
    _read = read

    def _mesg(self, genre, *args):
        """
        Args:
            genre: command type (Command)
            *args: other data.
                   It is converted to octal by default.
                   If the data needs to be encapsulated into hexadecimal,
                   the array is used to include them. (Data cannot be nested)
        """
        real_command = super(roarm, self)._mesg(genre, *args)  
        if self.thread_lock:
            with self.lock:
                return self._res(real_command, genre)
        else:
            return self._res(real_command, genre)

    def _res(self, real_command, genre):
        try_count = 0
        while try_count < 10:     
            if self.host:
                url = f"http://{self.host}/js?json={real_command.decode()}"
                response = requests.get(url)
                if genre != JsonCmd.FEEDBACK_GET:
                    data = real_command
                else:                                
                    data = json.loads(response.text)
            else:
                self._write(real_command)
                if genre != JsonCmd.FEEDBACK_GET:
                    data = real_command
                else:          
                    data = self._read(genre)   
                
            if data is not None and data != b'':
                break
            try_count += 1
        else:
            return -1
              
        res = self._process_received(data, genre)
        if res is None:
            return None
        elif isinstance(res, list) and len(res) == 1:
            return res[0]      
            
    def breath_led(self, duration=1.0, steps=10):
        """Set breath_led
        Args:
            duration: breath duration, type: float
            steps: breath steps, type: int
        """
        for i in range(steps + 1):
            led = int((i / steps) * 255)  
            self.led_ctrl(led=led)
            time.sleep(duration / (2 * steps))  

        for i in range(steps + 1):
            led = int((1 - i / steps) * 255)  
            self.led_ctrl(led=led)
            time.sleep(duration / (2 * steps)) 
        return 1 
        
    def listen_for_input(self):
        input("Press any to stop data collection...\n")
        self.stop_flag = True
        
    def drag_teach_start(self, filename):
        """Start drag teach
        Args:
            filename: file to save data, type: str
        """
        self.torque_set(cmd=0) 
        data = []
        print(f"Starting data collection.")
        input_thread = threading.Thread(target=self.listen_for_input)
        input_thread.daemon = True 
        input_thread.start()
        print("Press any to stop data collection...\n")
        while not self.stop_flag: 
            radians = self.joints_radian_get()
            record = {
                "timestamped": time.time(),
                "radians": radians
            }
            data.append(record)
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            print(f"Data saved. Total {len(data)} records.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def drag_teach_replay(self, filename):
        """Replay drag teach data 
        Args:
            filename: file to save data, type: str
        """
        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: File not found or empty. Ensure data exists in the file.")
            return

        total_steps = len(data)

        if total_steps < 2:
            print("Error: Not enough data to calculate velocity and acceleration.")
            return
        switch_dict = {
        "roarm_m2": [0, 0, 0, 0], 
        "roarm_m3": [0, 0, 0, 0, 0, 0],
        }
        prev_speed = switch_dict[self.type]  

        for i in range(1, total_steps):
            record1 = data[i-1]
            record2 = data[i]

            timestamp1, radians1 = record1["timestamped"], record1["radians"]
            timestamp2, radians2 = record2["timestamped"], record2["radians"]

            time_diff = timestamp2 - timestamp1
            if time_diff == 0:
                print(f"Warning: Zero time difference at step {i}, skipping velocity and acceleration calculation.")
                continue

            radians_diff = [r2 - r1 for r1, r2 in zip(radians1, radians2)]    
            angular_velocity = [r_diff / time_diff for r_diff in radians_diff]
            speed = [abs(int(angular_vel * 2048 / 3.1415926)) for angular_vel in angular_velocity]           
            acceleration = [abs(int((spd - prev_spd) / (100*time_diff))) if time_diff != 0 else 0 for spd, prev_spd in zip(speed, prev_speed)]
            
            for joint, radian, spd, acc in zip(range(1, len(prev_speed)+1), radians2, speed, acceleration):
                if spd != 0:
                    print(f"Speed for joint {joint}: {spd}, Acceleration: {acc}")
                    self.joint_radian_ctrl(joint=joint, radian=radian, speed=spd, acc=acc)
                    time.sleep(time_diff)
            prev_speed = speed

        print(f"Replayed {total_steps} steps from {filename}.")

    def disconnect(self):
        """Disconnect from the roarm 
        """
        self._serial_port.close()
