'''
Created on 17 Apr 2017

@author: rweffercifue
'''
from os.path import expanduser
import pygame
import PatientProcessor 
import tkinter as tk
import os

home = expanduser("~")

root = tk.Tk()
embed = tk.Frame(root)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())

#path = gui.fileopenbox("Select the image", "Image selection", default="./images",
#                     filetypes=["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"])
# print(path)
#PatientProcessor.load(pygame, "")