#!/usr/bin/env python3

#Renaming the database and the media folder, and deleting 001_initial.py
#This file must be in the folder 2LabsToGo-Eco-Software/app

#import os
import os

#rename the newly creted database
os.rename ("db.sqlite3", "db-new.sqlite3")

#rename the newly created media folder
os.rename ("media", "media-new")

#delete 0001_initial.py in migrations of sampleapp, finecontrol, development, detection
if os.path.exists("./sampleapp/migrations/0001_initial.py"):
  os.remove("./sampleapp/migrations/0001_initial.py")
else:
  print("The file does not exist")
  
if os.path.exists("./finecontrol/migrations/0001_initial.py"):
  os.remove("./finecontrol/migrations/0001_initial.py")
else:
  print("The file does not exist")

if os.path.exists("./development/migrations/0001_initial.py"):
  os.remove("./development/migrations/0001_initial.py")
else:
  print("The file does not exist")
  
if os.path.exists("./detection/migrations/0001_initial.py"):
  os.remove("./detection/migrations/0001_initial.py")
else:
  print("The file does not exist")

