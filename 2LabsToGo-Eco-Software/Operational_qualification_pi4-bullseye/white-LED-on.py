#!/usr/bin/env python3
#white-LED-on.py

import serial
import time

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(1)
#white LEDs on
command(ser, "G93R0B0G0W255\r\n")

time.sleep(1)
ser.close()