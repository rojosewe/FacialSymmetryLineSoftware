'''
Created on 17 Apr 2017

@author: rweffercifue
'''
from os.path import expanduser
import pygame
import os
import PatientProcessor
import sys
from utils import Commands
from  facial_measures import Patient, Face

home = expanduser("~")

#path = gui.fileopenbox("Select the image", "Image selection", default="./images",
#                     filetypes=["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"])

path = os.path.join("images", "1.JPG")
patient = {
    "name": "John doe",
    "photo-path": path,
    "face": None
}

print(path)
command = PatientProcessor.load(pygame, Patient("John doe", path, Face()))
if command == Commands.EXIT:
    sys.exit()