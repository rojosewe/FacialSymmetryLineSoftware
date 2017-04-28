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

home = expanduser("~")

#path = gui.fileopenbox("Select the image", "Image selection", default="./images",
#                     filetypes=["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"])
path = os.path.join("images", "1.JPG")
print(path)
command = PatientProcessor.load(pygame, path)
if command == commands.EXIT:
    sys.exit()