'''
Created on 17 Apr 2017

@author: rweffercifue
'''
from os.path import expanduser
import pygame
import os
import PatientProcessor
import sys
from utils import commands
from  facial_measures import Patient

home = expanduser("~")

#path = gui.fileopenbox("Select the image", "Image selection", default="./images",
#                     filetypes=["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"])
path = os.path.join("images", "1.JPG")
print(path)
command = PatientProcessor.load(pygame, Patient("John doe", path, None))
if command == commands.EXIT:
    sys.exit()