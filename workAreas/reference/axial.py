import os
from PIL import Image

from facial_measures.order import AxialOrder
from utils.Messages import messages as ms
from workAreas.reference import Reference


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