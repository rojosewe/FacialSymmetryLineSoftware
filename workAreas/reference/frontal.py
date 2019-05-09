'''
Created on 17 Apr 2017

@author: rweffercifue
'''

import os
from facial_measures.order import FrontalOrder
from PIL import Image
from utils.Messages import messages as ms
from workAreas.reference import Reference


class FrontalReference(Reference):

    def __init__(self):
        super().__init__()
        self.point = None
        self.pil_img = None
        self.order = None
        self.img = os.path.join("files", "images", "reference.png")
        self.order = FrontalOrder
        self.pil_img = Image.open(self.img)
        self.points = {FrontalOrder.CHIN: (94, 228),
                       FrontalOrder.FOREHEAD: (94, 105), FrontalOrder.EYE_OUTER_LEFT: (49, 117),
                       FrontalOrder.EYE_INNER_LEFT: (86, 113), FrontalOrder.EYE_INNER_RIGHT: (108, 113),
                       FrontalOrder.EYE_OUTER_RIGHT: (144, 117), FrontalOrder.CHEEKBONE_LEFT: (24, 134),
                       FrontalOrder.CHEEKBONE_RIGHT: (170, 137), FrontalOrder.NOSE_LEFT: (74, 145),
                       FrontalOrder.NOSE_CENTER: (95, 145), FrontalOrder.NOSE_RIGHT: (117, 146),
                       FrontalOrder.MOUTH_LEFT: (72, 175), FrontalOrder.MOUTH_RIGHT: (119, 176),
                       FrontalOrder.CHEEK_LEFT: (42, 203), FrontalOrder.CHEEK_RIGHT: (149, 201)}
        self.text_keys = {FrontalOrder.HORIZONTAL_LINE: "horizontal_line",
                          FrontalOrder.CHIN: "chin",
                          FrontalOrder.FOREHEAD: "forehead", FrontalOrder.EYE_OUTER_LEFT: "eye_outer_left",
                          FrontalOrder.EYE_INNER_LEFT: "eye_inner_left",
                          FrontalOrder.EYE_INNER_RIGHT: "eye_outer_right",
                          FrontalOrder.EYE_OUTER_RIGHT: "eye_inner_right",
                          FrontalOrder.CHEEKBONE_LEFT: "cheekbone_left",
                          FrontalOrder.CHEEKBONE_RIGHT: "cheekbone_right", FrontalOrder.NOSE_LEFT: "nose_left",
                          FrontalOrder.NOSE_CENTER: "nose_center", FrontalOrder.NOSE_RIGHT: "nose_right",
                          FrontalOrder.MOUTH_LEFT: "mouth_left", FrontalOrder.MOUTH_RIGHT: "mouth_right",
                          FrontalOrder.CHEEK_LEFT: "cheek_left", FrontalOrder.CHEEK_RIGHT: "cheek_right"}

    def load_screen(self, screen, left, top, right, bottom, next_point_label):
        Reference.load_screen(self, screen, left, top, right, bottom, next_point_label)
        self.next_point_label = next_point_label
        self.draw()

    def get_next_point_name(self, p):
        if p is not None:
            return ms[self.text_keys.get(p, "")]
        else:
            return ""
