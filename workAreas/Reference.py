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

points = {Order.TOP_HEAD: (100, 56), Order.CHIN: (100, 228), 
Order.FOREHEAD: (100, 105), Order.EYE_OUTER_LEFT: (55, 123), 
Order.EYE_INNER_LEFT: (92, 119), Order.EYE_INNER_RIGHT: (114, 119), 
Order.EYE_OUTER_RIGHT: (150, 123), Order.CHEEKBONE_LEFT: (30, 140), 
Order.CHEEKBONE_RIGHT: (176, 143), Order.NOSE_LEFT: (80, 151), 
Order.NOSE_RIGHT: (123, 152), Order.MOUTH_LEFT: (78, 181), 
Order.MOUTH_RIGHT: (125, 181), Order.CHEEK_LEFT: (48, 209), 
Order.CHEEK_RIGHT: (155, 207)}

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
    if pos < len(Order.order):
        x = Order.order[pos]
        if x in points:
            refPoint = points[x]
            refPoint = (refPoint[0], refPoint[1])
            point = screen.create_oval(refPoint[0], refPoint[1], 
                         refPoint[0] +4, refPoint[0] + 4, fill=cs.RED)