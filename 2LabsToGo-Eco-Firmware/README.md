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
To flash the firmware from the Raspberry Pi onto the Arduino chip of the 2LabsToGo-Eco mainboard, 
use the bash script <b>flash_firmware.sh</b>.

For more details on flashing, consult the 2LabsToGo-Eco Assembly guide 
(see reference in this [README](https://github.com/OfficeChromatography/2LabsToGo-Eco/blob/main/README.md)).
 
## After firmware update
After a firmware update, both PID tunings must be performed again to safe the settings in the firmware.<br>
Consult the 2LabsToGo-Eco Assembly guide.