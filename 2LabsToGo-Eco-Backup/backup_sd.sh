#!/bin/bash
#mounting backup system
sudo mount mybackupfolder  #name of the hard disk drive, as /media/pi/AAA4B3EBA4B3B7E1
#variables
BACKUP_FOLDER="mybackupfolder"
BACKUP_NUMBER="5"  #number of the backups to be kept
BACKUP_NAME="my2LabsToGo_SD"   #keep the extension _SD!!
#backup SD card
sudo dd if=/dev/mmcblk0 of=${BACKUP_FOLDER}/${BACKUP_NAME}-$(date +%Y%m%d).img bs=1MB
#pishrink to clean and compress the image
sudo pishrink.sh -z ${BACKUP_FOLDER}/${BACKUP_NAME}-$(date +%Y%m%d).img
#delete backups > BACKUP_NUMBER
pushd ${BACKUP_FOLDER}; ls -tr ${BACKUP_FOLDER}/${BACKUP_NAME}* | head -n -${BACKUP_NUMBER} | xargs -r rm; popd
#unmounting backup system
sudo umount mybackupfolder  #name of the hard disk drive, as /media/pi/AAA4B3EBA4B3B7E1

