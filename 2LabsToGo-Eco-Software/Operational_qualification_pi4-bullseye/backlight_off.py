#!/usr/bin/env python3
#backlight_off.py

import serial
import time

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(1)

command(ser, "M42P13S0\r\n")

time.sleep(1)
ser.close()
