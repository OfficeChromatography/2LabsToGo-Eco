#Script to test the photoposition

#fold=photo-position
#if [[ ! -d "$fold" ]]
#then
#   mkdir $fold
#fi

yes | sudo chmod 666 /dev/ttyAMA1

#Function IMAGE
IMAGE()
{  
   ./photo-pos.py
   ./white-LED-on.py
   sleep 10 #wait for LED
   libcamera-still --quality 100 --width 2028 --height 1520 -n -o photo-pos.jpg
   ./white-LED-off.py
   ./y-home.py
   sleep 2
}
IMAGE
#cd ~/OCLab4/operational-qualification/$fold
./distort-fisheye.py

