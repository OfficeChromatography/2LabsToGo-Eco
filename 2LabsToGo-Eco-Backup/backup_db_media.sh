#!/bin/bash
#mounting backup system
sudo mount mybackupfolder  #name of the hard disk drive, as /media/pi/AAA4B3EBA4B3B7E1
#variables
2LabsToGo_FOLDER="/home/piuser/2LabsToGo-Eco/2LabsToGo-Eco-Software"  #folder of the software
BACKUP_FOLDER="mybackupfolder"
BACKUP_NUMBER="5"  #number of the backups to be kept
BACKUP_NAME="my2LabsToGo_DB"   #keep the extension _DB!!
#backup database and media folder
sudo tar -zcvf ${BACKUP_FOLDER}/${BACKUP_NAME}-$(date +%Y%m%d-%H%M).tar.gz ${2LabsToGo_FOLDER}/app/db.sqlite3 ${2LabsToGo_FOLDER}/app/media > /dev/null
#Delete backups > BACKUP_NUMBER
pushd ${BACKUP_FOLDER}; ls -tr ${BACKUP_FOLDER}/${BACKUP_NAME}* | head -n -${BACKUP_NUMBER} | xargs -r rm; popd
#unmounting backup system
sudo umount mybackupfolder  #name of the hard disk drive, as /media/pi/AAA4B3EBA4B3B7E1
