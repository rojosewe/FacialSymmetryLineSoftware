'''
Created on 17 Apr 2017

@author: rweffercifue
'''

import os
from geometry import Rect
from facial_measures.order import AxialOrder
from utils import colors as cs
from PIL import Image
from PIL.ImageTk import PhotoImage

REF_WIDTH = 200
REF_HEIGHT = 250

class Reference:

    def __init__(self):
        self.screen = None
        self.rect = None
        self.img_obj = None

    def load_screen(self, screen, left, top, right, bottom):
        self.screen = screen
        self.rect = Rect(left, top, right, bottom)
        self.img_obj = Image.open(self.img)
        self.img_obj = self.img_obj.resize((REF_WIDTH, REF_HEIGHT), Image.ANTIALIAS)
        self.img_obj = PhotoImage(self.img_obj)
        self.screen.create_image(self.rect.left, self.rect.top, image=self.img_obj, anchor="nw")


    def get_image_size(self):
        return REF_WIDTH, REF_HEIGHT

    def process_click(self):
        self.draw()

    def draw(self):
        next = self.order.get_next()
        if self.point is not None:
            self.screen.delete(self.point)
        if not self.order.is_completed():
            if next in self.points:
                refPoint = self.points[next]
                refPoint = (refPoint[0], refPoint[1])
                self.point = self.screen.create_oval(refPoint[0], refPoint[1],
                                        refPoint[0] + 10, refPoint[1] + 10,
                                        fill=cs.RED, width=0)


class AxialReference(Reference):

    def __init__(self):
        super().__init__()
        self.rect = None
        self.point = None
        self.pil_img = None
        self.order = None
        self.img = os.path.join("files", "images", "ax-ref.JPG")
        self.order = AxialOrder
        self.pil_img = Image.open(self.img)
        self.points = {AxialOrder.CENTRAL_POINT: (96, 194), AxialOrder.POINT_NOSE: (96, 14),
                       AxialOrder.BREAK_POINT: (95, 89), AxialOrder.WALL_LEFT: (62, 103),
                       AxialOrder.WALL_RIGHT: (130, 103)}

    def load_screen(self, screen, left, top, right, bottom):
        Reference.load_screen(self, screen, left, top, right, bottom)
        self.draw()

