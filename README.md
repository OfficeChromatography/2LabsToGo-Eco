# 2LabsToGo-Eco

## 2LabsToGo-Eco combines an analytical (high-performance thin-layer chromatography) and a biological (bioassays) laboratory.

<u>References:</u>  
<a>1. M.C.O. Romero, K. Jakob, J. Schmidt, T. Nimmerfroh, W. Schwack, G.E.
 Morlock, Consolidating two laboratories into the most sustainable lab of the future: 2LabsToGo-Eco,
 Analytica Chimica Acta (2025) 1367, 344103,  https://doi.org/10.1016/j.aca.2025.344103

<a> 2. A. Haase, W. Schwack, G. Morlock, Humidity control for the 2LabsToGo-Eco, Analytica Chimica Acta (2025), in press


This repository contains the folders for the hardware, firmware, and software for 2LabsToGo-Eco.
For details and instructions consult the given references.

### 1. Raspberry Pi operating system (OS)
For the 2LabsToGo-Eco-Software, Debian 11 (bullseye) is the required OS, but not available 
any more on the Raspberry Pi website <br>(https://www.raspberrypi.com/software/operating-systems/). 
However, bullseye can be downloaded from the archive<br> (https://downloads.raspberrypi.com/raspios_arm64/images/raspios_arm64-2023-05-03/).
It is not the "full" version, i.e., without recommended software packages, but required software can easily be installed
later.

<br>The new OS called "trixie" (Debian 13) unfortunately cannot be used for the 2LabsToGo-Eco-Software, 
but we are working on it.


### 2. Clone the 2LabsToGo-Eco repository
The simplest way to clone a git repository is opening a terminal, then go to the directory where you would like to have the 2LabsToGo-Eco folder.

E.g.
```bash
cd ~/Desktop
```
Finally, copy and paste the next command and press enter.
```bash
git clone https://github.com/OfficeChromatography/2LabsToGo-Eco.git
```


