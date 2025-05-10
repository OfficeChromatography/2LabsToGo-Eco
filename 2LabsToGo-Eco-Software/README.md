# 2LabsToGo-Eco-Software
## Install
The installation process is really simple. 

2LabsToGo-Eco-Software works fine on a 'Raspberry Pi 4' with 4Gb RAM memory.

As operation system, Raspberry Pi OS (Legacy, 64-bit, Debian Bullseye) is recommended,
installed by the [Raspberry Pi Imager](https://www.raspberrypi.com/software/).

To clone the 2LabsToGo-Eco repository, consult this [README](https://github.com/OfficeChromatography/2LabsToGo-Eco/blob/main/README.md).

### Execute 'install.py'
To install 2LabsToGo-Eco-Software, go to the folder that contains the 2LabsToGo-Eco-Software with

```bash
cd /path/to/your/2LabsToGo-Eco-Software
```
Then execute
```bash
python3 install.py |& tee install-py.log
```

This will install:
```
docker
docker compose
```
After some minutes, 2LabsToGo-Eco-Software is installed in your device.

To start the server execute the run.py file with
```
python3 run.py |& tee run-py.log
```
The log files can be consulted in case of any problem.<a>

To quit the Django server, press
```
Ctrl+c 
```

2LabsToGo-Eco-Software was intensively tested with both Chromium and Firefox as browser.

To use the software consult the 2LabsToGo-Eco-Software Manual (see reference in 
this [README](https://github.com/OfficeChromatography/2LabsToGo-Eco/blob/main/README.md)).

# Useful guides

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
