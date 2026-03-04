#!/usr/bin/env python3
#white-LED-off.py

import serial
import time

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(2)
#white LEDs on
command(ser, "G93R0B0G0W0\r\n")

time.sleep(1)
ser.close()