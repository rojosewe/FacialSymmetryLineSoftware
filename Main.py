'''
Created on 17 Apr 2017

@author: rweffercifue
'''
from os.path import expanduser
import pygame
import ngui

pygame.init()
home = expanduser("~")
ngui.start(home, pygame)