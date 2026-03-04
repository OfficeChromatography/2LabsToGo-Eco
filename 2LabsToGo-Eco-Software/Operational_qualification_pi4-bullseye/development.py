#!/usr/bin/env python3
#development.py

import serial
import time

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(1)

command(ser, "G28XY\r\n")
command(ser, "G0X1F3000\r\n")
command(ser, "G0Y8F2000\r\n")
time.sleep(2)

command(ser, "G0X20\r\n")
time.sleep(2)
command(ser, "M400\r\n")
command(ser, "G0X131F1200\r\n")
time.sleep(2)
command(ser, "M400\r\n")
command(ser, "G0X20F1200\r\n")
time.sleep(2)
command(ser, "M400\r\n")
command(ser, "G0X131F1200\r\n")
time.sleep(2)
command(ser, "M400\r\n")
command(ser, "G0X20F1200\r\n")
time.sleep(2)
command(ser, "M400\r\n")
command(ser, "G0X131F1200\r\n")

command(ser, "G28X\r\n")
command(ser, "M400\r\n")

time.sleep(1)
ser.close()
