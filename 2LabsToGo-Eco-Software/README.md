# 2LabsToGo-Eco-Software
## Installation
The installation process is really simple. 

2LabsToGo-Eco-Software works fine on a Raspberry Pi 4B or 5B with 4GB RAM memory.

As operation system, Raspberry Pi OS (Debian 13, trixie, 64-bit) is recommended,
installed by the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) (see reference 3 in 
this [README](https://github.com/OfficeChromatography/2LabsToGo-Eco/blob/main/README.md)).

Before the next steps, consult the [checklist](https://github.com/OfficeChromatography/2LabsToGo-Eco/blob/main/2LabsToGo-Update-History/checklist.pdf).

To clone the 2LabsToGo-Eco repository, consult this [README](https://github.com/OfficeChromatography/2LabsToGo-Eco/blob/main/README.md).

### Execute 'install.py'
To install 2LabsToGo-Eco-Software, go to the folder that contains the 2LabsToGo-Eco-Software with

```bash
cd /path/to/your/2LabsToGo-Eco-Software
```
Then execute
```bash
sudo python3 install.py |& tee install-py.log
```

This will install:
```
docker and some software packages
```
After some minutes, 2LabsToGo-Eco-Software is installed in your device.

To start the server execute the run.py file with
```
sudo python3 run.py |& tee run-py.log
```
This process takes a while, when executed the first time. The log files can be consulted in case of any problem.<a>

To quit the Django server, press
```
Ctrl+c 
```

2LabsToGo-Eco-Software was intensively tested with both Chromium and Firefox as browser.

To use the software consult the 2LabsToGo-Eco-Software Manual (see reference 1 in 
this [README](https://github.com/OfficeChromatography/2LabsToGo-Eco/blob/main/README.md)).

### Useful guides

[Docker Commands](https://towardsdatascience.com/15-docker-commands-you-should-know-970ea5203421)

[Remove Migrations](https://simpleisbetterthancomplex.com/tutorial/2016/07/26/how-to-reset-migrations.html)

All commands must be executed inside the docker-compose. To enter to the docker-compose running instance:

In a running container:
```sh
sudo docker-compose exec -ti app bash
```
To initialize and enter the terminal
```sh
sudo docker-compose run -ti app bash
```
