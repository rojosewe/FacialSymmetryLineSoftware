'''
Created on 17 Apr 2017

@author: rweffercifue
'''

import os
from geometry import Rect
from facial_measures import Order
from utils import colors as cs
from pygame import draw as d

img = None
size = None
screen = None
rect = None

points = {Order.TOP_HEAD: (100, 56), Order.CHIN: (100, 228), 
Order.FOREHEAD: (100, 105), Order.EYE_OUTER_LEFT: (55, 123), 
Order.EYE_INNER_LEFT: (92, 119), Order.EYE_OUTER_RIGHT: (114, 119), 
Order.EYE_INNER_RIGHT: (150, 123), Order.CHEEKBONE_LEFT: (30, 140), 
Order.CHEEKBONE_RIGHT: (176, 143), Order.NOSE_LEFT: (80, 151), 
Order.NOSE_RIGHT: (123, 152), Order.MOUTH_LEFT: (78, 181), 
Order.MOUTH_RIGHT: (125, 181), Order.CHEEK_LEFT: (48, 209), 
Order.CHEEK_RIGHT: (155, 207)}

def init(pygame):
    global  img, size
    img = pygame.image.load(os.path.join("images", "reference.jpeg"))
    size = img.get_rect().size
    return (size[0], size[1])
    
def load(screen_main, left, top, right, bottom):
    global screen, rect
    screen = screen_main
    rect = Rect(left, top, right, bottom)

def processClick(event, p, pos):
    print(p)

def draw(p, pos):
    screen.blit(img, (rect.left, rect.top))
    if pos < len(Order.order):
        x = Order.order[pos]
        if x in points:
            refPoint = points[x]
            refPoint = (refPoint[0], refPoint[1])
            d.circle(screen, cs.RED, refPoint, 4)