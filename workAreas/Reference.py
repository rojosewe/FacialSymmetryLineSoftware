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

points = {Order.TOP_HEAD: (96, 41), Order.CHIN: (98, 187)
, Order.FOREHEAD: (97, 96), Order.EYE_OUTER_LEFT: (56, 103)
, Order.EYE_INNER_LEFT: (81, 103), Order.EYE_OUTER_RIGHT: (109, 102)
, Order.EYE_INNER_RIGHT: (132, 100), Order.CHEEKBONE_LEFT: (47, 129)
, Order.CHEEKBONE_RIGHT: (149, 127), Order.NOSE_LEFT: (81, 128)
, Order.NOSE_RIGHT: (114, 130), Order.MOUTH_LEFT: (74, 156)
, Order.MOUTH_RIGHT: (121, 153), Order.CHEEK_LEFT: (58, 176)
, Order.CHEEK_RIGHT: (140, 174)}

def init(pygame):
    global  img, size
    img = pygame.image.load(os.path.join("images", "images.jpeg"))
    size = img.get_rect().size
    
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
            d.circle(screen, cs.GREEN, refPoint, 4)