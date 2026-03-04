#!/usr/bin/env python3
#syringe-pump.py

import serial
import time

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(1)

#Marlin settings for syringe pump
command(ser, "M92Z1600\r\n")   #Set Axis Steps-per-unit
command(ser, "M203Z5\r\n")   #Set Max Feedrate
command(ser, "M42P36S255\r\n")  #Switch 3way-valve?
command(ser, "M42P49S255\r\n")  #Switch Z-motor and Z-endstop?
command(ser, "G28Z\r\n")      #homing syringe pump
command(ser, "G28X\r\n")      #homing X
command(ser, "G0X1F3000\r\n")      #x-cart to left
command(ser, "M400\r\n")

command(ser, "G0Z270\r\n")
command(ser, "M400\r\n")
command(ser, "G28Z\r\n")
command(ser, "G0Z280\r\n")
command(ser, "M400\r\n")
command(ser, "G28Z\r\n")



time.sleep(1)
ser.close()
