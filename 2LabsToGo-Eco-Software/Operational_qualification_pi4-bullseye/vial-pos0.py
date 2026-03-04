#!/usr/bin/env python3
#vial-pos0.py

import serial
import time
import os

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(1)

#Marlin settings for autosampler z-axis
command(ser, "M92Z400\r\n")   #Set Axis Steps-per-unit
command(ser, "M203Z15\r\n")   #Set Max Feedrate
command(ser, "M42P36S0\r\n")  #Switch 3way-valve?
command(ser, "M42P49S0\r\n")  #Switch Z-motor and Z-endstop?
command(ser, "M400\r\n")

command(ser, "G0E0F4000\r\n")  #needle up
command(ser, "M400\r\n")
command(ser, "G0X90\r\n")

command(ser, "G28Z\r\n")      #homing z1
command(ser, "M400\r\n")
command(ser, "G28X\r\n")      #Homing X

time.sleep(1)
ser.close()
