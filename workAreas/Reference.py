'''
Created on 17 Apr 2017

@author: rweffercifue
'''

import os
from geometry import Rect
from facial_measures import Order
from utils import colors as cs
from PIL import Image
from PIL.ImageTk import PhotoImage


img = None
screen = None
rect = None
point = None
img_obj = None

points = {Order.TOP_HEAD: (94, 56), Order.CHIN: (94, 228), 
Order.FOREHEAD: (94, 105), Order.EYE_OUTER_LEFT: (49, 117), 
Order.EYE_INNER_LEFT: (86, 113), Order.EYE_INNER_RIGHT: (108, 113), 
Order.EYE_OUTER_RIGHT: (144, 117), Order.CHEEKBONE_LEFT: (24, 134), 
Order.CHEEKBONE_RIGHT: (170, 137), Order.NOSE_LEFT: (74, 145),
Order.NOSE_CENTER: (95, 145), Order.NOSE_RIGHT: (117, 146), 
Order.MOUTH_LEFT: (72, 175), Order.MOUTH_RIGHT: (119, 176), 
Order.CHEEK_LEFT: (42, 203), Order.CHEEK_RIGHT: (149, 201)}

def init():
    global  img
    img = os.path.join("images", "reference.jpeg")
    pil_img = Image.open(img)
    return pil_img.size
    
def load(screen_main, left, top, right, bottom):
    global screen, rect, img_obj
    screen = screen_main
    rect = Rect(left, top, right, bottom)
    img_obj = PhotoImage(file=img)
    screen.create_image(rect.left, rect.top, image=img_obj, anchor="nw")

def processClick(p, pos):
    draw(pos)

def draw(pos):
    global point
    if point is not None:
        screen.delete(point)
    x = Order.getPos(pos)
    if pos:
        if x in points:
            refPoint = points[x]
            refPoint = (refPoint[0], refPoint[1])
            print(refPoint)
            point = screen.create_oval(refPoint[0], refPoint[1],
                                       refPoint[0] + 10, refPoint[1] + 10, 
                                       fill=cs.RED, width=0)