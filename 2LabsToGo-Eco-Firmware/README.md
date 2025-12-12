# 2LabsToGo-Eco Firmware 
A Marlin 2.0 3D Printer based Firmware

## Marlin 2.0

Marlin 2.0 takes this popular RepRap firmware to the next level by adding support for much faster 32-bit and ARM-based boards while improving support for 8-bit AVR boards. Read about Marlin's decision to use a "Hardware Abstraction Layer" below.


## Building 2LabsToGo-Eco Firmware

To build the firmware, [PlatformIO](http://docs.platformio.org/en/latest/ide.html#platformio-ide) is preferred. 
Detailed instructions are also available in Instruction Visual Studio Code.pdf.

For building the firmware open the folder 2LabsToGo-Eco-Marlin in Visual Studio Code.
The built firmware.hex file is then saved in 2LabsToGo-Eco-Firmware/2LabsToGo-Eco-Marlin/.pio/build/mega2560.

<b>However, building the firmware is only required, if the Marlin codes have been modified.</b><a>

A pre-built firmware file (firmware_2LabsToGo-Eco.hex) is available in this folder, including files for setting the fuses and flashing the bootloader.

## Flashing Firmware on Raspberry Pi OS Bookworm

The firmware flashing process has been updated to work with Raspberry Pi OS Bookworm Lite, which uses the new `gpiod` interface instead of the legacy `sysfs` GPIO.

### First-time Setup (Bookworm)

Before flashing firmware for the first time on Bookworm, run the setup script:

```bash
sudo bash setup_bookworm.sh
```

This script will:
- Install required packages (avrdude with gpiod support)
- Configure GPIO access permissions
- Set up the system for firmware flashing

**Note:** After running the setup script, you may need to log out and back in for group permission changes to take effect.

### Flashing the Firmware

To flash the firmware from the Raspberry Pi onto the Arduino chip of the 2LabsToGo-Eco mainboard, use the bash script:

```bash
sudo bash flash_firmware.sh
```

### Compatibility Notes

- **Bookworm (recommended)**: Uses `linuxgpiod` driver - fully supported
- **Bullseye and older**: Uses `linuxgpio` driver - legacy support

If you're using an older Raspberry Pi OS version, the original configuration will still work.

For more details on flashing, consult the 2LabsToGo-Eco Assembly guide 
(see reference 1 in this [README](https://github.com/OfficeChromatography/2LabsToGo-Eco/blob/main/README.md)).
 
## After firmware update
<b>After a firmware update, both PID tunings must be performed again to safe the settings in the firmware.<br>
Consult the 2LabsToGo-Eco Assembly guide.</b>

## Troubleshooting

### GPIO Access Issues
If you encounter "Permission denied" errors:
1. Ensure you're running with `sudo`
2. Check that `/dev/gpiochip0` exists: `ls -l /dev/gpiochip*`
3. Verify GPIO group membership: `groups`

### avrdude Version Issues
If flashing fails, check your avrdude version:
```bash
avrdude -? 2>&1 | grep version
```

Version 7.0 or higher is required for Bookworm compatibility. The setup script will attempt to install a compatible version.