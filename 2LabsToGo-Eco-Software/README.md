# OC-Manager 4.0
## Install
The installation process is really simple. 

OC-Manager 4.0 works fine on a 'Raspberry Pi 4' with 4Gb RAM memory and [Raspberry Pi OS](https://www.raspberrypi.com/software/) installed on it through Raspberry Pi Imager, which was installed by:
```
sudo apt install rpi-imager
```  

### 0. Install git
Before we begin with the installation, we need to install git.
```bash
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install git
```

### 1. Clone the git repository
The simplest way to clone a git repository is opening a Terminal (`Ctrl+t`), then go to the directory where you would like to have the folder that contains all the configuration files of your OC-LAB **(and between those, it is included the OC-Manager files too)**  

E.g.
```bash
cd ~/Desktop
```
Finally, copy and paste the next command and press enter.

```bash
git clone https://github.com/OfficeChromatography/OC-Manager4.git
```

### 2. Execute 'install.py'
The next step is to execute a bash script which contains, the necessary softwares to run the OC-Manager. If you close the Terminal open it again (remember, `Ctrl+t`). Now go to the folder that contains the OC-Lab files, it is

*cd* follow by the path to the folder.

```bash
cd /path/to/your/OC-files
```
Then execute,
```bash
python3 install.py
```

this will install:
```
docker
docker-compose
```
Now OC-Manager it's installed in your device.

### 3.Before the first execution 

#### With Raspberry Pi
Depending on the OS change on the docker_compose.yml file. To know the kind of architecture, open a terminal and write:

```
uname -a 
```

According to your architecture, change the dockerfile:

```dockerfile
    image: ocmanager/ocmanager:arm64
```

```dockerfile
    image: ocmanager/ocmanager:amd64
``` 

### 4.OC Manager execution 

Navigate to the path where OC-Manager was installed and execute ./run.py file.
```
python3 run.py 
```

OC-Manager supports at the moment only amd64, arm/v7 and arm64 architectures.

OC-Manager3 was intensively tested with Firefox as browser. Therefore, it is recommended to install this browser:

```
sudo apt install firefox-esr
```

# FIRMWARE
Firmware installation 
[OcLab3Firmware](https://github.com/OfficeChromatography/OCLab3-Hardware)

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
