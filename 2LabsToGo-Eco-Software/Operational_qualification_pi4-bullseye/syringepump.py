#!/usr/bin/env python3

#file syringepump.py

import serial
import time
import os

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
#time.sleep(1)

#Marlin settings for syringe pump
command(ser, "M92Z1600\r\n")   #Set Axis Steps-per-unit
command(ser, "M203Z5\r\n")     #Set Max Feedrate
#z-switch
command(ser, "M42P36S255\r\n") #Switch 3way-valve
command(ser, "M42P49S255\r\n") #Switch Z-motor and Z-endstop
command(ser, "G28Z\r\n")       #Homing syringe pump

command(ser, "G28X\r\n")       #Homing X
command(ser, "G0X1F3000\r\n")  #x-axis to waste bottle

os.system("aplay --quiet BusinessEcho.wav")
print("Fill a 2-mL syringe with 2 mL ethanol, connect the Luer-lock adapter to the tip, and insert it into the syringe pump.")
print("")
command(ser, "G0Z274.67F200\r\n") #Move to position for syringe 2 mL

print("Connect the PTFE tube to the Luer-lock adapter and tighten it with the Lee torque wrench (min. torque).")
print("")
print("First the system will be rinsed, followed by a pressure test.")
print("")
os.system("aplay --quiet BusinessEcho.wav")
print("In case of problems, terminate the program immediately with Ctrl+c!")
print("")

input("Ready to start the rinsing process? (ENTER)")
#time.sleep(1)
print("")
os.system("aplay --quiet BusinessEcho.wav")
print("Now the fluidic system will be rinsed with 500 µL. The solvent will be ejected from the dispensing valve into the waste bottle.")
print("")

try:
    command(ser, "G41\r\n") #open dispensing valve
    command(ser, "G0Z281.34F200\r\n") #Move to position to rinse 500 µL (+6.67 mm)
    command(ser, "G40\r\n") #close dispensing valve
    os.system("aplay --quiet BusinessEcho.wav")
    print("Now the dispensing valve was closed, and the syringe pump will build-up a pressure of 5 psi.")
    print("")
    command(ser, "G97P5\r\n") #5 psi
    command(ser, "M400\r\n")  #Wait for pressure    command(ser, "G95P\r\n")  #Report pressure, is not possible
    time.sleep(1)
    
    os.system("aplay --quiet BusinessEcho.wav")
    print("The pressure will be increased to 10 psi. Also check the 3-way valve!")
    print("")
    command(ser, "G97P10\r\n") #10 psi
    command(ser, "GM400\r\n")  #Wait for pressure
    command(ser, "G95P\r\n")  #Report pressure.
    time.sleep(1)
    
    os.system("aplay --quiet BusinessEcho.wav")
    #print("The pressure will be increased to 15 psi.")
    print("")
    command(ser, "G97P15\r\n") #15 psi
    command(ser, "GM400\r\n")  #Wait for pressure
    command(ser, "G95P\r\n")  #Report pressure
    time.sleep(1)
    
    os.system("aplay --quiet BusinessEcho.wav")
    print("Now the pressure will be increased to 20 psi.")
    print("")
    command(ser, "G97P20\r\n") #20 psi
    command(ser, "GM400\r\n")  #Wait for pressure
    command(ser, "G95P\r\n")  #Report pressure
    time.sleep(1)
    os.system("aplay --quiet BusinessEcho.wav")
    print("The dispensing valve will be opened to leave the pressure. Solvent will be ejected from the dispensing valve into the waste bottle.")
    print("")
    command(ser, "G40\r\n")  #Open valve
    time.sleep(1)
except KeyboardInterrupt:  #Ctrl+c
    os.system("aplay --quiet BusinessEcho.wav")
    print("Program terminated manually!")
    command(ser, "G40\r\n")  #Open valve to leave the pressure!
    command(ser, "M400\r\n") 
    raise SystemExit 
    
#Marlin re-settings for autosampler
command(ser, "M92Z400\r\n")   #Set Axis Steps-per-unit
command(ser, "M203Z15\r\n")   #Set Max Feedrate
command(ser, "M42P36S0\r\n")  #Switch 3way-valve
command(ser, "M42P49S0\r\n")  #Switch Z-motor and Z-endstop

os.system("aplay --quiet BusinessEcho.wav")
print("Congratulations, the syringe pump test was successfully passed!!")
print("If there were leakages, tighten the fittings.")

time.sleep(1)
ser.close()
