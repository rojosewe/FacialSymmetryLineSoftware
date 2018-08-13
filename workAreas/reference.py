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
from utils.Messages import messages as ms

REF_WIDTH = 200
REF_HEIGHT = 250


class Reference:

    def __init__(self):
        self.screen = None
        self.rect = None
        self.img_obj = None
        self.next_point_label = None
        self.point = None

    def load_screen(self, screen, left, top, right, bottom, next_point_label):
        self.screen = screen
        self.rect = Rect(left, top, right, bottom)
        self.img_obj = Image.open(self.img)
        self.img_obj = self.img_obj.resize((REF_WIDTH, REF_HEIGHT), Image.ANTIALIAS)
        self.img_obj = PhotoImage(self.img_obj)
        self.screen.create_image(self.rect.left, self.rect.top, image=self.img_obj, anchor="nw")
        self.next_point_label = next_point_label

    def get_image_size(self):
        return REF_WIDTH + 30, REF_HEIGHT

    def process_click(self):
        self.draw()

    def draw(self):
        next = self.order.get_next()
        if self.point is not None:
            self.screen.delete(self.point)
        if not self.order.is_completed():
            if next in self.points:
                ref_point = self.points[next]
                ref_point = (ref_point[0], ref_point[1])
                self.point = self.screen.create_oval(ref_point[0], ref_point[1],
                                                     ref_point[0] + 10, ref_point[1] + 10,
                                                     fill=cs.RED, width=0)
        self.next_point_label.set(self.get_next_point_name(next))


class AxialReference(Reference):

    def __init__(self):
        super().__init__()
        self.point = None
        self.pil_img = None
        self.order = None
        self.img = os.path.join("files", "images", "ax-ref.JPG")
        self.order = AxialOrder
        self.pil_img = Image.open(self.img)
        self.points = {AxialOrder.CENTRAL_POINT: (96, 194), AxialOrder.POINT_NOSE: (96, 14),
                       AxialOrder.BREAK_POINT: (95, 89), AxialOrder.WALL_LEFT: (62, 103),
                       AxialOrder.WALL_RIGHT: (130, 103), AxialOrder.MAXILAR_LEFT: (21, 118),
                       AxialOrder.MAXILAR_RIGHT: (167, 118)
                       }
        self.text_keys = {
            AxialOrder.CENTRAL_POINT: "central_point", AxialOrder.POINT_NOSE: "nose_point",
            AxialOrder.BREAK_POINT: "break_point", AxialOrder.WALL_LEFT: "wall_left",
            AxialOrder.WALL_RIGHT: "wall_right", AxialOrder.MAXILAR_LEFT: "maxilar_left",
            AxialOrder.MAXILAR_RIGHT: "maxilar_right"
        }

    def load_screen(self, screen, left, top, right, bottom, next_point_label):
        Reference.load_screen(self, screen, left, top, right, bottom, next_point_label)
        self.next_point_label = next_point_label
        self.draw()

    def get_next_point_name(self, p):
        if p is not None:
            return ms[self.text_keys.get(p, "")]
        else:
            return ""
