#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/2labstogo_programmer.conf"

# Check if config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file not found at $CONFIG_FILE"
    exit 1
fi

# Check if avrdude is installed
if ! command -v avrdude &> /dev/null; then
    echo "avrdude is not installed. Please run setup_bookworm.sh first"
    exit 1
fi

# Check if linuxgpio programmer is available
if ! avrdude -c ?type 2>&1 | grep -q "linuxgpio"; then
    echo "Error: avrdude doesn't support linuxgpio programmer"
    echo "Please run: sudo bash setup_bookworm.sh"
    exit 1
fi

echo "Using avrdude version: $(avrdude -? 2>&1 | grep -oP 'version \K[0-9]+\.[0-9]+' | head -1)"
echo "Using config file: $CONFIG_FILE"

# Verify the programmer is defined in the config
if ! grep -q 'id = "2LabsToGo"' "$CONFIG_FILE"; then
    echo "Error: Programmer '2LabsToGo' not found in config file"
    exit 1
fi

echo "Setting fuses..."
avrdude -p atmega2560 -C "+$CONFIG_FILE" -c 2LabsToGo -v -U lfuse:w:0xff:m -U hfuse:w:0xd8:m -U efuse:w:0xfd:m

if [ $? -ne 0 ]; then
    echo "Error: Failed to set fuses"
    exit 1
fi

echo "Flashing bootloader..."
avrdude -p atmega2560 -C "+$CONFIG_FILE" -c 2LabsToGo -v -U flash:w:ArduinoISP.ino.hex:i

if [ $? -ne 0 ]; then
    echo "Error: Failed to flash bootloader"
    exit 1
fi

echo "Flashing firmware..."
avrdude -p atmega2560 -C "+$CONFIG_FILE" -c 2LabsToGo -v -U flash:w:firmware_2LabsToGo-Eco.hex:i

if [ $? -eq 0 ]; then
    echo "Firmware flashed successfully!"
else
    echo "Error: Failed to flash firmware"
    exit 1
fi
