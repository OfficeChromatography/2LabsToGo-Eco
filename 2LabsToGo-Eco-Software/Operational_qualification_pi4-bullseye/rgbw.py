#!/usr/bin/env python3
#rgbw.py

import serial
import time

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)
  

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(2)


#LEDs on and off
command(ser, "G93R50B0G0W0\r\n")
time.sleep(1)
command(ser, "G93R100B0G0W0\r\n")
time.sleep(1)
command(ser, "G93R150B0G0W0\r\n")
time.sleep(1)
command(ser, "G93R200B0G0W0\r\n")
time.sleep(1)
command(ser, "G93R250B0G0W0\r\n")
time.sleep(1)
command(ser, "G93R0B50G0W0\r\n")
time.sleep(1)
command(ser, "G93R0B100G0W0\r\n")
time.sleep(1)
command(ser, "G93R0B150G0W0\r\n")
time.sleep(1)
command(ser, "G93R0B200G0W0\r\n")
time.sleep(1)
command(ser, "G93R0B250G0W0\r\n")
time.sleep(1)
command(ser, "G93R0B0G50W0\r\n")
time.sleep(1)
command(ser, "G93R0B0G100W0\r\n")
time.sleep(1)
command(ser, "G93R0B0G150W0\r\n")
time.sleep(1)
command(ser, "G93R0B0G200W0\r\n")
time.sleep(1)
command(ser, "G93R0B0G250W0\r\n")
time.sleep(1)
command(ser, "G93R0B0G0W50\r\n")
time.sleep(1)
command(ser, "G93R0B0G0W100\r\n")
time.sleep(1)
command(ser, "G93R0B0G0W150\r\n")
time.sleep(1)
command(ser, "G93R0B0G0W200\r\n")
time.sleep(1)
command(ser, "G93R0B0G0W250\r\n")
time.sleep(1)
command(ser, "G93R0B0G0W0\r\n")

time.sleep(2)
ser.close()
