#!/usr/bin/env python3
#y-home.py

import serial
import time

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(2)
command(ser, "G28Y\r\n")

ser.close()
