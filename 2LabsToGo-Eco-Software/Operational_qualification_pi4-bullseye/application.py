#!/usr/bin/env python3
#application.py

import serial
import time

def command(ser, command):
  ser.write(str.encode(command)) 
  time.sleep(1)

ser = serial.Serial('/dev/ttyAMA1', 115200)
time.sleep(1)

command(ser, "G0Y10F3000\r\n")  #needle is in vial 1!!
time.sleep(2)

#first band
command(ser, "G0X30\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X30.5F3000\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X31F3000\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X31.5F3000\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X32F3000\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X32.5F3000\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X33F3000\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X33.5F3000\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X34F3000\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X34.5F3000\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X35F3000\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X35.5F3000\r\n")
command(ser, "G98F1200\r\n")
command(ser, "G0X36.0F3000\r\n")
command(ser, "G98F1200\r\n")

command(ser, "G0X1\r\n")
command(ser, "M400\r\n")

time.sleep(1)
ser.close()
