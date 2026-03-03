#!/bin/bash

sudo avrdude -p atmega2560 -C avrdude_gpio.conf -c 2LabsToGo -v -U lfuse:w:0xff:m -U hfuse:w:0xd8:m -U efuse:w:0xfd:m
sudo avrdude -p atmega2560 -C avrdude_gpio.conf -c 2LabsToGo -v -U flash:w:ArduinoISP.ino.hex:i
sudo avrdude -p atmega2560 -C avrdude_gpio.conf -c 2LabsToGo -v -U flash:w:../firmware_2LabsToGo-Eco.hex:i
