# Waveshare Roarm SDK

![Python 2.7](https://img.shields.io/badge/Python-v2.7%5E-green?logo=python)
![Python 3](https://img.shields.io/badge/Python-v3%5E-green?logo=python)

This is a python API for serial or http communication with waveshare roarm and controlling it.

[Waveshare RoArm-M2 Series](https://www.waveshare.com/roarm-m2-s.htm): **RoArm-M2-S**， **RoArm-M2-Pro**.

[Waveshare RoArm-M3 Series](https://www.waveshare.com/roarm-m3.htm): **RoArm-M3-S**， **RoArm-M3-Pro**.

<a href="https://www.waveshare.com/roarm-m2-s.htm">
    <img src="./images/roarm_m2.png" alt="home" width="300" height="200"/>
</a>
<a href="https://www.waveshare.com/roarm-m3.htm">
    <img src="./images/roarm_m3.png" alt="home" width="300" height="200"/>
</a>

## Installation
### Pip install

```bash
pip install roarm-sdk==0.1.0
```

### Source code

```bash
git clone https://https://github.com/waveshareteam/waveshare_roarm_sdk.git <your-path>
cd <your-path>/waveshare_roarm_sdk
# Install
[sudo] python2 setup.py install
# or
[sudo] python3 setup.py install
```

## Usage:

```python
from roarm_sdk.roarm import roarm

# for roarm_m2 Serial communication example
roarm = roarm(roarm_type="roarm_m2", port="/dev/ttyUSB0", baudrate=115200)

# for roarm_m3 Serial communication example
#roarm = roarm(roarm_type="roarm_m3", port="/dev/ttyUSB0", baudrate=115200)
```

The [`demo`](./demo) directory stores some test case files.

You can find out which interfaces roarm_sdk provides in [`./doc/README.md`](./doc/RADME.md).

![jaywcjlove/sb](https://jaywcjlove.github.io/sb/lang/chinese.svg)   ![jaywcjlove/sb](https://jaywcjlove.github.io/sb/lang/english.svg)

[roarm_m2 api 说明](./doc/roarm_m2_zh.md) | [roarm_m2 api Description](./doc/roarm_m2_en.md)

[roarm_m3 api 说明](./doc/roarm_m3_zh.md) | [roarm_m3 api Description](./doc/roarm_m3_en.md)