#script to run the operational qualification of 2LabsToGo
#Needle motor must be completly up!!
#show.sh

yes | sudo chmod 666 /dev/ttyAMA1
#yes | sudo chmod +x *.py

aplay --quiet BusinessEcho.wav
echo ""
echo "This is a show presenting the different 2LabToGo activities."
echo ""
echo "Check that there are no tools and anything else inside the instrument!"
echo ""
aplay --quiet BusinessEcho.wav
echo "Place an HPTLC plate silica gel F254 into the plate holder simple and place the plate holder onto the y-cart."
echo ""
echo "You are ready to start (y+ENTER)? Press Ctrl+c to stop this show."
read answer
   if [ "$answer" != "y" ]
     then
	 echo ""
	 echo "The show was stopped by the user."  #script completely ends!
	 aplay --quiet EchoBells.wav
	 exit -1
   fi
echo ""

echo "All axes are going to home."
aplay --quiet BusinessEcho.wav
echo ""
python3 home-all.py

python3 caselight.py
#sleep 1

#test syringe pump
echo "The syringe pump starts to move."
aplay --quiet BusinessEcho.wav
echo ""
python3 syringe-pump.py
sleep 15

echo "The autosampler moves to vial 1 and the needle down to simulate a rinsing process and sample application."
aplay --quiet BusinessEcho.wav
python3 vial-pos1.py #needle in vial 1
echo ""

#aplay --quiet BusinessEcho.wav
python3 application.py #1 band

echo "All axes are going to home."
python3 vial-pos0.py #needle up, x to 90 and z home, then x home
sleep 10
echo ""

aplay --quiet BusinessEcho.wav
echo "This is the simulation of plate development, but the syringe pump is not activated here."
python3 development.py
sleep 10
echo ""
aplay --quiet BusinessEcho.wav

python3 caselight-off.py
#Plate inserted?
echo "Now the camera is going to capture images at white light, UV 265 nm and UV 365 nm."
python3 photo-pos.py
python3 white-LED-on.py
libcamera-still -t 5000 -o vis.jpg #image saved in folder 2LabsToGo-Software/Operational_qualification
python3 white-LED-off.py
echo""

python3 uv265_on.py
libcamera-still -t 5000 -o uv265.jpg
python3 uv265_off.py

python3 uv365_on.py
libcamera-still -t 5000 -o uv365.jpg
python3 uv365_off.py

python3 distort-fisheye.py --file-format jpg --source-folder ~/2LabsToGo/2LabsToGo-Software-Software/Operational_qualification --output-folder ~/2LabsToGo/2LabsToGo-Software/Operational_qualification/corrected

python3 y-home.py

echo "This is a colored light show. Place a white paper onto the rods under the camera cabinet."
aplay --quiet BusinessEcho.wav
sleep 15
python3 rgbw.py


