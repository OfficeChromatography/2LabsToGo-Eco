#script to run dd and pyshrink

echo " Insert an USB stick (exFat or NTFS formatted with about 100 GB free space into the Raspberry Pi."
echo ""
echo "Open a new Linux terminal, type df -l and press ENTER"
echo ""
echo "Copy the name under which the USB stick is mounted: last line text starting with /media/... ."
echo ""
echo "Paste or type the name of the USB stick (ENTER):" 
read usb

echo "The disk dump is going to start. It will take a while!"

sudo dd bs=4M if=/dev/mmcblk0 of=$usb/2LabsToGo.img status=progress
pid=$!
wait $pid

echo ""
echo "pishrink will now compress the image file to 2LabsToGo.img.gz. It also will take a while."
echo ""

sudo pishrink.sh -z $usb/2LabsToGo.img
pid=$!
wait $pid

echo "The process is finished!"
 
