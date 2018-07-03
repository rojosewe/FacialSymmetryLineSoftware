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


class Reference:

    def __init__(self):
        self.screen = None
        self.rect = None
        self.img_obj = None

    def load_screen(self, screen, left, top, right, bottom):
        self.screen = screen
        self.rect = Rect(left, top, right, bottom)
        self.img_obj = PhotoImage(Image.open(self.img))
        self.screen.create_image(self.rect.left, self.rect.top, image=self.img_obj, anchor="nw")
        screen.create_image(self.rect.left, self.rect.top, image=self.img_obj, anchor="nw")

    def get_image_size(self):
        return self.pil_img.size

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
        print(os.path.isfile(os.path.join("files", "images", "reference.jpeg")))
        self.img = os.path.join("files", "images", "reference.jpeg")
        self.order = AxialOrder
        self.pil_img = Image.open(self.img)
        self.points = {AxialOrder.CENTRAL_POINT: (94, 228), AxialOrder.POINT_NOSE: (94, 56),
                       AxialOrder.BREAK_POINT: (94, 105), AxialOrder.WALL_LEFT: (49, 117),
                       AxialOrder.WALL_RIGHT: (144, 117)}

    def load_screen(self, screen, left, top, right, bottom):
        Reference.load_screen(self, screen, left, top, right, bottom)
        self.draw()

