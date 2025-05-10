#!/usr/bin/env python3
#vial-pos.py

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
command(ser, "G28Z\r\n")      #homing z1
command(ser, "G28X\r\n")      #Homing X
command(ser, "G0X1F1000\r\n")      #x-cart to waste

#print("Insert the vial rack with parcel tape.")
print("")
os.system("aplay --quiet BusinessEcho.wav")
print("First the vial rack will move to the rinsing vial.")
print("")
os.system("aplay --quiet BusinessEcho.wav")
print("In case of problems, terminate the program immediately with Ctrl+c!")
print("")
os.system("aplay --quiet BusinessEcho.wav")
input("Start the vial position test? (ENTER)")

try:
    command(ser, "G0Z145\r\n")
    command(ser, "M400\r\n")
    os.system("aplay --quiet BusinessEcho.wav")
    input("Is the needle guide nearly in the center of the rinsing vial cutout? (ENTER)")
    command(ser, "G0E20\r\n")
    command(ser, "G0E0\r\n")
    command(ser, "M400\r\n")
    
    print("Now the positions of vial 1 to 3 are tested.")
    command(ser, "G0Z169.5\r\n")
    command(ser, "M400\r\n")
    command(ser, "G0E20\r\n")
    command(ser, "G0E0\r\n")
    command(ser, "M400\r\n")
    
    command(ser, "G0Z183.5\r\n")
    command(ser, "M400\r\n")
    command(ser, "G0E20\r\n")
    command(ser, "G0E0\r\n")
    command(ser, "M400\r\n")

    command(ser, "G0Z197.5\r\n")
    command(ser, "M400\r\n")
    command(ser, "G0E20\r\n")
    command(ser, "G0E0\r\n")
    command(ser, "M400\r\n")
    
    command(ser, "G28Z\r\n")      #homing z1
    command(ser, "M400\r\n")
    command(ser, "G28X\r\n")      #homing x
    
except KeyboardInterrupt:  #Ctrl+c
    os.system("aplay --quiet BusinessEcho.wav")
    print("Program terminated manually!")
    command(ser, "G0E0\r\n")      #Needle moves up!
    command(ser, "M400\r\n")      #Wait for neddle.
    command(ser, "G28Z\r\n")      #homing z1
    raise SystemExit 

print("Take out the vial rack and check the needle punctures.")
os.system("aplay --quiet BusinessEcho.wav")
time.sleep(1)
ser.close()
