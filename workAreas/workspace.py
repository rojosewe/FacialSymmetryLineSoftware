'''
Created on 17 Apr 2017

@author: rweffercifue
'''

from geometry import Rect
from facial_measures import AxialFace
from geometry import Point, Line, Mark, distance
from utils import colors as cs
from PIL import Image
from PIL.ImageTk import PhotoImage
from workAreas.state_manager import get_patient
from facial_measures.order import AxialOrder

MIN_DIST = 20
MAX_V = 700


class AxialWorkspace:

    def __init__(self):
        self.screen = None
        self.rect = None
        self.patient = get_patient()
        self.green_marks = []
        self.guideline = None
        self.lines = []
        self.pixel_points = []
        self.img_obj = None
        self.show_lines = True
        self.pil_img = Image.open(self.patient.photo)

    def get_image_size(self):
        w, h = self.pil_img.size
        proportion = w/h
        h = min(MAX_V, h)
        w = int(h * proportion)
        return w, h
    
    def load(self, screen_main, left, top, right, bottom):
        self.screen = screen_main
        self.rect = Rect(left, top, right, bottom)
        self.img_obj = Image.open(self.patient.photo)
        self.img_obj = self.img_obj.resize((right - left, bottom - top), Image.ANTIALIAS)
        self.img_obj = PhotoImage(self.img_obj)
        self.screen.create_image(self.rect.left, self.rect.top, image=self.img_obj, anchor="nw")
        self.complete_visuals_if_patient_is_completed(self.patient)
                
    def in_box(self, p):
        return p.x >= self.rect.left and p.x < self.rect.right and p.y >= self.rect.top and p.y < self.rect.bottom

    def create_line(self, line):
        return self.screen.create_line(line.p1.x, line.p1.y,
                                  line.p2.x, line.p2.y, fill=line.color, width=line.w)

    def create_mark(self, mark):
        return self.screen.create_oval(mark.p.x - mark.r, mark.p.y - mark.r, mark.p.x + mark.r,
                                  mark.p.y + mark.r, fill=mark.color)

    def assign_point_to_face_pos_and_return_if_completed(self, p):
        complete_before = AxialOrder.is_completed()
        x = AxialOrder.get_next()
        if self.in_box(p) and x and not self.checkForTooCloseNeightbors(p):
            if x == AxialOrder.CENTRAL_POINT:
                self.createGuideline(Line(Point(p.x, self.rect.top), Point(p.x, p.y), color=cs.RED))
                self.patient.axial.central_point = p
            elif x == AxialOrder.POINT_NOSE:
                self.patient.axial.point_nose = p
            elif x == AxialOrder.BREAK_POINT:
                self.patient.axial.break_point = p
            elif x == AxialOrder.WALL_LEFT:
                self.patient.axial.wall_left = p
            elif x == AxialOrder.WALL_RIGHT:
                self.patient.axial.wall_right = p
            if not AxialOrder.is_empty():
                self._auxAddMark(p)
            AxialOrder.add_to_processed(x)
        complete_now = AxialOrder.is_completed()
        if complete_now and not complete_before:
            return True
        else:
            return False

    def createGuideline(self, line):
        self.guideline = line
        self.create_line(self.guideline)

    def removeGuideline(self):
        self.screen.delete(self.guideline)
        self.guideline = None

    def checkForTooCloseNeightbors(self, p):
        for p1 in self.pixel_points:
            if self._check_distance(p1, p) < MIN_DIST:
                return True
        return False

    def _check_distance(self, p1, p2):
        if p1 is not None and p2 is not None:
            return distance(p1, p2)
        else:
            return True

    def complete_visuals_if_patient_is_completed(self, patient):
        if AxialOrder.is_completed():
            self._auxAddMark(patient.axial.central_point)
            self._auxAddMark(patient.axial.break_point)
            self._auxAddMark(patient.axial.point_nose)
            self._auxAddMark(patient.axial.wall_left)
            self._auxAddMark(patient.axial.wall_right)
            self.processFullPatient(patient)

    def _auxAddMark(self, p):
        self.green_marks.append(self.create_mark(Mark(p, r=4, color=cs.GREEN)))
        self.pixel_points.append(p)

    def addAngles(self, patient):
        lines = patient.axial.angles.getLines(patient.face, color = cs.BLUE, width = 2)
        for line in lines:
            self.lines.append(self.create_line(line))

    def processMove(self, p):
        pass

    def process_click_return_if_completed(self, event, point):
        completed_now = self.assign_point_to_face_pos_and_return_if_completed(point)
        if completed_now:
            self.processFullPatient(self.patient)
        return completed_now


    def completeWorkspace(self, patient):
        self.addAngles(patient)

    def processFullPatient(self, patient):
        patient.angles.calculate(patient.face)
        patient.proportions.calculate(patient.angles)
        self.completeWorkspace(patient)
        return patient


    def undo_previous_action(self):
        if AxialOrder.is_completed():
            AxialOrder.delete_last_processed()
            self._delete_last_mark()
        elif not AxialOrder.is_empty():
            x = AxialOrder.get_next()
            AxialOrder.delete_last_processed()
            if AxialOrder.is_empty():
                self.removeGuideline()
            else:
                self._delete_last_mark()

    def clean(self):
        for i in range(len(self.green_marks)):
            self._delete_last_mark()
        AxialOrder.delete_all_processed()
        self.removeGuideline()
        self.patient.axial = AxialFace()

    def _delete_last_mark(self):
        if len(self.green_marks) == 0:
            return None
        self.pixel_points.pop()
        m = self.green_marks.pop()
        screen.delete(m)

    def restart(self):
        self.clean()
