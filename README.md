# HPMA115S0 library in Python


This library is used to interface the HPMA115S0 sensor with a Python script running on a Raspberry Pi.

we use multipe i2c devices defined with i2c-gpio in /boot/config.txt
i2cdetect can be slow:
```
pi@raspberrypi:~ $ sudo raspi-gpio set 23 pu
pi@raspberrypi:~ $ sudo raspi-gpio set 24 pu
pi@raspberrypi:~ $ sudo i2cdetect -y 3
```
