'''
Created on 17 Apr 2017

@author: rweffercifue
'''

import os
from geometry import Rect
from facial_measures.frontal_face_order import get_next, is_completed
from facial_measures import frontal_face_order
from utils import colors as cs
from PIL import Image
from PIL.ImageTk import PhotoImage


img = None
screen = None
rect = None
point = None
img_obj = None

points = {frontal_face_order.TOP_HEAD: (94, 56), frontal_face_order.CHIN: (94, 228),
          frontal_face_order.FOREHEAD: (94, 105), frontal_face_order.EYE_OUTER_LEFT: (49, 117),
          frontal_face_order.EYE_INNER_LEFT: (86, 113), frontal_face_order.EYE_INNER_RIGHT: (108, 113),
          frontal_face_order.EYE_OUTER_RIGHT: (144, 117), frontal_face_order.CHEEKBONE_LEFT: (24, 134),
          frontal_face_order.CHEEKBONE_RIGHT: (170, 137), frontal_face_order.NOSE_LEFT: (74, 145),
          frontal_face_order.NOSE_CENTER: (95, 145), frontal_face_order.NOSE_RIGHT: (117, 146),
          frontal_face_order.MOUTH_LEFT: (72, 175), frontal_face_order.MOUTH_RIGHT: (119, 176),
          frontal_face_order.CHEEK_LEFT: (42, 203), frontal_face_order.CHEEK_RIGHT: (149, 201)}


def init():
    global img
    img = os.path.join("files", "images", "reference.jpeg")
    pil_img = Image.open(img)
    return pil_img.size


def load(screen_main, left, top, right, bottom):
    global screen, rect, img_obj
    screen = screen_main
    rect = Rect(left, top, right, bottom)
    img_obj = PhotoImage(file=img)
    screen.create_image(rect.left, rect.top, image=img_obj, anchor="nw")


def processClick():
    draw()

def draw():
    next = get_next()
    global point
    if point is not None:
        screen.delete(point)
    if not is_completed():
        if next in points:
            refPoint = points[next]
            refPoint = (refPoint[0], refPoint[1])
            print(refPoint)
            point = screen.create_oval(refPoint[0], refPoint[1],
                                       refPoint[0] + 10, refPoint[1] + 10, 
                                       fill=cs.RED, width=0)