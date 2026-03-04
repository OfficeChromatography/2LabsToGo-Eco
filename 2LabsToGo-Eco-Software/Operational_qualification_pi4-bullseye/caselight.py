#!/usr/bin/env python3
#caselight.py

import serial
import time

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(1)

#case light increasing and then off
#command(ser, "M355 S0 P100\r\n")
#time.sleep(1)
#command(ser, "M355 S1 P100\r\n")
#time.sleep(1)
command(ser, "M355 S0 P150\r\n")
#time.sleep(1)
command(ser, "M355 S1 P150\r\n")
#time.sleep(1)
command(ser, "M355 S0 P200\r\n")
#time.sleep(1)
command(ser, "M355 S1 P250\r\n")
#time.sleep(1)
#command(ser, "M355 S1 P250\r\n")

time.sleep(1)
ser.close()
