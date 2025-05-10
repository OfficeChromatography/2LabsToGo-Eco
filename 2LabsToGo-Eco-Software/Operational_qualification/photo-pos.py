#!/usr/bin/env python3
#photo-pos.py

import serial
import time

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(1)

command(ser, "G28Y\r\n")
command(ser, "G0Y158F3000\r\n")   #photo position???? 
command(ser, "M400\r\n")

ser.close()
