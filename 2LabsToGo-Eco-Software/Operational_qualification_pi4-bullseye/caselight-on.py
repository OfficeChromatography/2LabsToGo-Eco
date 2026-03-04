#!/usr/bin/env python3
#caselight-on.py

import serial
import time

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(1)

#case light off
command(ser, "M355 S1 P200\r\n")
#time.sleep(1)

time.sleep(1)
ser.close()
