#!/usr/bin/env python3

#file micropump.py

import serial
import time
import os


def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(1)

#Marlin settings for autosampler
command(ser, "M92Z400\r\n")   #Set Axis Steps-per-unit
command(ser, "M203Z15\r\n")   #Set Max Feedrate
command(ser, "M42P36S0\r\n")  #Switch 3way-valve
command(ser, "M42P49S0\r\n")  #Switch Z-motor and Z-endstop
command(ser, "G28Z\r\n")      #Homing Z
command(ser, "G28X\r\n")      #Homing X
command(ser, "G0X1F3000\r\n")      #x-cart to 1eft
command(ser, "G0Z145\r\n")    #Rinsing vial

print("First the system will be rinsed, followed by a pressure test.")
print("")
os.system("aplay --quiet BusinessEcho.wav")
print("In case of problems, terminate the program immediately with Ctrl+c and press the RESET button on the mainboard!")
print("")
os.system("aplay --quiet BusinessEcho.wav")
input("Start the rinsing process? (ENTER)")
os.system("aplay --quiet BusinessEcho.wav")
print("")
print("Now the needle is moving into the rinsing vial, and the micropump system will be rinsed. Solvent will be ejected from the dispensing valve into the waste bottle.")
print("")
command(ser, "G0E44\r\n")  #Needle moves down! 44 okay!!
command(ser, "M400\r\n")   #Wait for needle!
command(ser, "G41\r\n")  #open dispensing valve

try:
    for x in range(14):      #rinse system, 15 x pump = 500 µL
        command(ser, "M42P40S255\r\n")  #activate pump
        time.sleep(0.1)
        command(ser, "M42P40S0\r\n")  #deactivate pump
        time.sleep(0.5)
except KeyboardInterrupt:  #Ctrl+c
    os.system("aplay --quiet BusinessEcho.wav")
    print("Program terminated manually!")
    command(ser, "G0E0\r\n")  #Needle moves up!
    command(ser, "M400\r\n")  #Wait for neddle
    command(ser, "G28Z\r\n")  #Homing vial rack
    raise SystemExit 

os.system("aplay --quiet BusinessEcho.wav")
print("Now the dispensing valve will be closed and the micropump builds-up pressure.")
print("")
command(ser, "G40\r\n")  #Close dispensing valve

try:
    for x in range(3):      #build-up pressure, 4 x pump
        command(ser, "M42P40S255\r\n")
        time.sleep(0.1)
        command(ser, "M42P40S0\r\n")
        time.sleep(0.5)
except KeyboardInterrupt:  #Ctrl+c
    os.system("aplay --quiet BusinessEcho.wav")
    print("Program terminated manually!")
    command(ser, "G0E0\r\n")  #Needle moves up!
    command(ser, "M400\r\n") 
    raise SystemExit 

print("Now the dispensing valve will be opened. Solvent will be ejected from the dispensing valve into the waste bottle.")
print("")
command(ser, "G40\r\n")  #open valve
time.sleep(1)

print("The dispensing valve was closed again and the needle is moving up.")
print("")
command(ser, "G0E0\r\n")  #Needle moves up!
command(ser, "M400\r\n")  #Wait for needle!
command(ser, "G28Z\r\n")  #Homing z!

print("Congratulations, the micropump test was successfully passed!!")
print("If there were leakages, tighten the fittings.").

time.sleep(1)
ser.close()
