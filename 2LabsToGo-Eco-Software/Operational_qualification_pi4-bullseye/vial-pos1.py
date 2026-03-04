#!/usr/bin/env python3
#vial-pos1.py

import serial
import time
import os

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
#time.sleep(1)

#Marlin settings for autosampler z-axis
command(ser, "M92Z400\r\n")   #Set Axis Steps-per-unit
command(ser, "M203Z15\r\n")   #Set Max Feedrate
command(ser, "M42P36S0\r\n")  #Switch 3way-valve?
command(ser, "M42P49S0\r\n")  #Switch Z-motor and Z-endstop?
command(ser, "M400\r\n")

command(ser, "G28Z\r\n")      #homing z1
command(ser, "G28X\r\n")      #Homing X
command(ser, "G0X1F4000\r\n")      #x-cart to waste
command(ser, "M400\r\n")

command(ser, "G0Z145F2000\r\n") 
command(ser, "M400\r\n")
command(ser, "G0E30F4000\r\n")
command(ser, "M400\r\n")
time.sleep(5)                   #rinsing 5 s

command(ser, "G0E0\r\n")        #needle up
command(ser, "M400\r\n")
    
command(ser, "G0Z169.5F2000\r\n") #pos vial 1
command(ser, "M400\r\n")
command(ser, "G0E30F4000\r\n")  #needle in vial 1
command(ser, "M400\r\n")

time.sleep(1)
ser.close()
