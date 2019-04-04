'''
Created on 17 Apr 2017

@author: rweffercifue
'''

from geometry import Rect
from facial_measures import AxialFace, FrontalFace
from geometry import Point, Line, Mark, distance
from utils import colors as cs
from PIL import Image
from PIL.ImageTk import PhotoImage
from workAreas.state_manager import get_patient
from facial_measures.order import AxialOrder, FrontalOrder

MIN_DIST = 20
MAX_V = 700
MAX_H = 900


class Workspace:

    def __init__(self):
        self.screen = None
        self.rect = None
        self.patient = get_patient()
        self.guideline = None
        self.img_obj = None
        self.show_lines = True
        self.pil_img = Image.open(self.patient.photo)
        self.order = None

    def get_image_size(self):
        w, h = self.pil_img.size
        proportion = w/h
        h = min(MAX_V, h)
        w = int(h * proportion)
        if w > MAX_H:
            w = MAX_H
            h = int(w // proportion)
        return w, h

    def load_screen(self, screen, left, top, right, bottom):
        self.screen = screen
        self.rect = Rect(left, top, right, bottom)
        self.img_obj = Image.open(self.patient.photo)
        self.img_obj = self.img_obj.resize((right - left, bottom - top), Image.ANTIALIAS)
        self.img_obj = PhotoImage(self.img_obj)
        self.screen.create_image(self.rect.left, self.rect.top, image=self.img_obj, anchor="nw")
        self.complete_visuals_if_patient_is_completed(self.patient)

    def in_box(self, p):
        return p.x >= self.rect.left and p.x < self.rect.right \
               and p.y >= self.rect.top and p.y < self.rect.bottom

    def create_line(self, line):
        return self.screen.create_line(line.p1.x, line.p1.y,line.p2.x, line.p2.y,
                                       fill=line.color, width=line.w, dash=line.dash)

    def create_mark(self, mark):
        return self.screen.create_oval(mark.p.x - mark.r, mark.p.y - mark.r, mark.p.x + mark.r,
                                  mark.p.y + mark.r, fill=mark.color)

    def _check_for_too_close_neighbors(self, p):
        for p1 in self.pixel_points:
            if self._check_distance(p1, p) < MIN_DIST:
                return True
        return False

    def _check_distance(self, p1, p2):
        if p1 is not None and p2 is not None:
            return distance(p1, p2)
        else:
            return True

    def create_guideline(self, line):
        self.guideline = self.create_line(line)

    def remove_guideline(self):
        self.screen.delete(self.guideline)
        self.guideline = None

    def process_move(self, p):
        pass

    def restart(self):
        self.clean()

    def undo_previous_action(self):
        self._delete_all_lines()
        self.order.delete_last_processed()
        self._delete_last_mark()
        if self.order.is_empty():
            self.remove_guideline()

    def _delete_all_lines(self):
        for line in self.lines:
            self.screen.delete(line)

    def clean(self):
        self._delete_all_marks()
        self._delete_all_lines()
        self.order.delete_all_processed()
        self.remove_guideline()
        self.patient.values = AxialFace()

    def _delete_all_marks(self):
        for i in range(len(self.green_marks)):
            self._delete_last_mark()

    def _auxAddMark(self, p, r=6, color=cs.GREEN):
        self.green_marks.append(self.create_mark(Mark(p, r=r, color=color)))
        self.pixel_points.append(p)

    def completeWorkspace(self, patient):
        self.addAngles(patient)

    def _delete_last_mark(self):
        if len(self.green_marks) == 0:
            self.pixel_points.clear()
            return None
        self.pixel_points.pop()
        m = self.green_marks.pop()
        self.screen.delete(m)

    def addAngles(self, patient):
        lines = patient.values.angles.get_lines(patient.values, color=cs.BLUE, width=4)
        for line in lines:
            self.lines.append(self.create_line(line))

    def process_click_return_if_completed(self, event, point):
        completed_now = self.assign_point_to_face_pos_and_return_if_completed(point)
        if completed_now:
            self.process_full_patient(self.patient)
        return completed_now

    def process_full_patient(self, patient):
        patient.values.angles.calculate(patient.values)
        patient.values.proportions = patient.values.get_proportions()
        self.completeWorkspace(patient)
        return patient


class AxialWorkspace(Workspace):

    def __init__(self):
        super().__init__()
        self.green_marks = []
        self.lines = []
        self.pixel_points = []
        self.order = AxialOrder

    def assign_point_to_face_pos_and_return_if_completed(self, p):
        complete_before = self.order.is_completed()
        x = self.order.get_next()
        if self.in_box(p) and x and not self._check_for_too_close_neighbors(p):
            color = cs.GREEN
            if x == AxialOrder.CENTRAL_POINT:
                self.create_guideline(Line(Point(p.x, self.rect.top), Point(p.x, p.y), color=cs.RED, w=3, dash=(4, 4)))
                self.patient.values.central_point = p
                color = cs.RED
            elif x == AxialOrder.POINT_NOSE:
                self.patient.values.point_nose = p
                color = cs.YELLOW
            elif x == AxialOrder.BREAK_POINT:
                self.patient.values.break_point = p
                color = cs.BLUE
            elif x == AxialOrder.WALL_LEFT:
                self.patient.values.wall.left = p
            elif x == AxialOrder.WALL_RIGHT:
                self.patient.values.wall.right = p
            elif x == AxialOrder.MAXILAR_LEFT:
                self.patient.values.maxilar.left = p
                color = cs.YELLOW
            elif x == AxialOrder.MAXILAR_RIGHT:
                self.patient.values.maxilar.right = p
                color = cs.YELLOW
            AxialOrder.add_to_processed(x)
            if not AxialOrder.is_empty():
                self._auxAddMark(p, r=8, color=color)
        complete_now = self.order.is_completed()
        if complete_now and not complete_before:
            return True
        else:
            return False

    def complete_visuals_if_patient_is_completed(self, patient):
        if self.order.is_completed():
            self._auxAddMark(patient.values.central_point, 8, cs.RED)
            self._auxAddMark(patient.values.break_point, 8, cs.BLUE)
            self._auxAddMark(patient.values.point_nose, 8, cs.YELLOW)
            self._auxAddMark(patient.values.wall.left, 8)
            self._auxAddMark(patient.values.wall.right, 8)
            self._auxAddMark(patient.values.maxilar.left, 8, cs.YELLOW)
            self._auxAddMark(patient.values.maxilar.right, 8, cs.YELLOW)
            self.process_full_patient(patient)


class FrontalWorkspace(Workspace):

    def __init__(self):
        super().__init__()
        self.green_marks = []
        self.lines = []
        self.pixel_points = []
        self.order = FrontalOrder

    def assign_point_to_face_pos_and_return_if_completed(self, p):
        complete_before = self.order.is_completed()
        x = self.order.get_next()
        if self.in_box(p) and x and not self._check_for_too_close_neighbors(p):
            color = cs.GREEN
            if x == FrontalOrder.HORIZONTAL_LINE:
                self.create_guideline(Line(Point(p.x, self.rect.top), Point(p.x, self.rect.bottom),
                                           color=cs.RED, w=3, dash=(4, 4)))
                self.patient.values
            elif x == FrontalOrder.TOP_HEAD:
                self.patient.values.upper = p
            elif x == FrontalOrder.CHIN:
                self.patient.values.chin = p
            elif x == FrontalOrder.FOREHEAD:
                self.patient.values.middle = p
            elif x == FrontalOrder.EYE_OUTER_LEFT:
                self.patient.values.outer_eye.left = p
            elif x == FrontalOrder.EYE_OUTER_RIGHT:
                self.patient.values.outer_eye.right = p
            elif x == FrontalOrder.EYE_INNER_LEFT:
                self.patient.values.inner_eye.left = p
            elif x == FrontalOrder.EYE_INNER_RIGHT:
                self.patient.values.inner_eye.right = p
            elif x == FrontalOrder.CHEEKBONE_LEFT:
                self.patient.values.cheekbone.left = p
            elif x == FrontalOrder.CHEEKBONE_RIGHT:
                self.patient.values.cheekbone.right = p
            elif x == FrontalOrder.NOSE_LEFT:
                self.patient.values.nose.left = p
            elif x == FrontalOrder.NOSE_CENTER:
                self.patient.values.nose_center = p
            elif x == FrontalOrder.NOSE_RIGHT:
                self.patient.values.nose.right = p
            elif x == FrontalOrder.MOUTH_LEFT:
                self.patient.values.mouth.left = p
            elif x == FrontalOrder.MOUTH_RIGHT:
                self.patient.values.mouth.right = p
            elif x == FrontalOrder.CHEEK_LEFT:
                self.patient.values.cheek.left = p
            elif x == FrontalOrder.CHEEK_RIGHT:
                self.patient.values.cheek.right = p
            FrontalOrder.add_to_processed(x)
            if not FrontalOrder.is_empty():
                self._auxAddMark(p, r=8, color=color)
        complete_now = self.order.is_completed()
        if complete_now and not complete_before:
            return True
        else:
            return False

    def complete_visuals_if_patient_is_completed(self, patient):
        if self.order.is_completed():
            self._auxAddMark(patient.values.upper, 8, cs.RED)
            self._auxAddMark(patient.values.chin, 8, cs.RED)
            self._auxAddMark(patient.values.middle, 8, cs.BLUE)
            self._auxAddMark(patient.values.outer_eye.left, 8, cs.YELLOW)
            self._auxAddMark(patient.values.outer_eye.left, 8, cs.YELLOW)
            self._auxAddMark(patient.values.inner_eye.left, 8, cs.YELLOW)
            self._auxAddMark(patient.values.inner_eye.right, 8, cs.YELLOW)
            self._auxAddMark(patient.values.cheekbone.left, 8, cs.GREEN)
            self._auxAddMark(patient.values.cheekbone.right, 8, cs.GREEN)
            self._auxAddMark(patient.values.nose.left, 8, cs.GREEN)
            self._auxAddMark(patient.values.nose.right, 8, cs.GREEN)
            self._auxAddMark(patient.values.nose_center, 8, cs.GREEN)
            self._auxAddMark(patient.values.mouth.left, 8, cs.ORANGE)
            self._auxAddMark(patient.values.mouth.right, 8, cs.ORANGE)
            self._auxAddMark(patient.values.cheek.left, 8, cs.BLACK)
            self._auxAddMark(patient.values.cheek.right, 8, cs.BLACK)
            self.process_full_patient(patient)