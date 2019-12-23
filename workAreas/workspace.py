'''
Created on 17 Apr 2017

@author: rweffercifue
'''

from facial_measures import AxialFace, FrontalFace
from geometry import Point, Line, Mark, distance, Rect, intersects
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
        self.marks = []
        self.additional_marks = []

    def get_image_size(self):
        w, h = self.pil_img.size
        proportion = w / h
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

    def in_box(self, p):
        return p.x >= self.rect.left and p.x < self.rect.right and p.y >= self.rect.top and p.y < self.rect.bottom

    def create_line(self, line):
        return self.screen.create_line(line.p1.x, line.p1.y, line.p2.x, line.p2.y,
                                       fill=line.color, width=line.w, dash=line.dash)

    def add_mark_to_screen(self, mark):
        return self.screen.create_oval(mark.p.x - mark.r, mark.p.y - mark.r, mark.p.x + mark.r,
                                       mark.p.y + mark.r, fill=mark.color)

    def _check_for_too_close_neighbors(self, p):
        for m in self.marks:
            if self._check_distance(m.p, p) < MIN_DIST:
                return True
        return False

    def _check_distance(self, p1, p2):
        if p1 is not None and p2 is not None:
            return distance(p1, p2)
        else:
            return True

    def create_guideline(self, face):
        pass

    def remove_guideline(self):
        if self.guideline is not None:
            self.screen.delete(self.guideline.screen_ref)
        self.guideline = None

    def process_move(self, p):
        pass

    def restart(self):
        self.clean()

    def undo_previous_action(self):
        self.order.delete_last_processed()
        self._delete_last_mark()
        self.remove_additional_marks()
        if self.order.is_empty():
            self.remove_guideline()
        self._delete_all_lines()

    def _delete_all_lines(self):
        for line in self.lines:
            self.screen.delete(line.screen_ref)
        self.lines.clear()

    def clean(self):
        self.remove_guideline()
        self.remove_additional_marks()
        self._delete_all_marks()
        self._delete_all_lines()
        self.order.delete_all_processed()
        self.reset_instance()

    def _delete_all_marks(self):
        for i in range(len(self.marks)):
            self._delete_last_mark()

    def _create_visual_mark(self, p, r, color):
        mark = Mark(p, r=r, color=color)
        mark.screen_ref = self.add_mark_to_screen(mark)
        return mark

    def complete_workspace(self):
        self.hide_all_visual_marks()
        self.add_angles()
        self.readd_all_visual_marks()
        self.add_additional_marks()

    def hide_all_visual_marks(self):
        for mark in self.marks:
            self.screen.delete(mark.screen_ref)
            mark.screen_ref = None

    def readd_all_visual_marks(self):
        for mark in self.marks:
            mark.screen_ref = self.add_mark_to_screen(mark)

    def _delete_last_mark(self):
        if len(self.marks) == 0:
            return
        m = self.marks.pop()
        self.screen.delete(m.screen_ref)

    def add_angles(self):
        pass

    def process_point_return_if_completed(self, point):
        completed_now = self.assign_point_to_face_pos_and_return_if_completed(point)
        if completed_now:
            self.process_full_patient()
        return completed_now

    def assign_point_to_face_pos_and_return_if_completed(self):
        pass

    def process_full_patient(self):
        patient = self.patient
        patient.values.calculate_additional()
        patient.values.angles.calculate(patient.values)
        self.complete_workspace()

    def reset_instance(self):
        pass

    def add_additional_marks(self):
        pass

    def remove_additional_marks(self):
        pass


class FrontalWorkspace(Workspace):

    def __init__(self):
        super().__init__()
        self.interocular_lines = []
        self.malar_lines = []
        self.chin_lines = []
        self.lines = []
        self.order = FrontalOrder
        self.show_malar_angles = True
        self.show_chin_angles = True
        self.show_interocular_angles = True

    def assign_point_to_face_pos_and_return_if_completed(self, p):
        if self.order.is_completed():
            return False
        next_point = self.order.get_next()
        if self.in_box(p) and next_point and not self._check_for_too_close_neighbors(p):
            self._set_mark_to_facial_value(p, next_point)
            FrontalOrder.add_to_processed(next_point)
        return self.order.is_completed()

    def _set_mark_to_facial_value(self, p, x):
        color = cs.GREEN
        if x == FrontalOrder.CHIN:
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
        self.marks.append(self._create_visual_mark(p, r=4, color=color))

    def add_additional_marks(self):
        face = self.patient.values
        self.additional_marks.append(self._create_visual_mark(face.malar.left, r=4, color=cs.RED))
        self.additional_marks.append(self._create_visual_mark(face.malar.right, r=4, color=cs.RED))
        self.additional_marks.append(self._create_visual_mark(face.middle, r=4, color=cs.RED))

    def remove_additional_marks(self):
        for additonal_mark in self.additional_marks:
            self.screen.delete(additonal_mark.screen_ref)
        self.additional_marks.clear()

    def toggle_malar_angles(self):
        for line in self.malar_lines:
            if not self.show_malar_angles:
                self.screen.itemconfig(line.screen_ref, state="hidden")
            else:
                self.screen.itemconfig(line.screen_ref, state="normal")

    def toggle_chin_angles(self):
        for line in self.chin_lines:
            if not self.show_chin_angles:
                self.screen.itemconfig(line.screen_ref, state="hidden")
            else:
                self.screen.itemconfig(line.screen_ref, state="normal")

    def toggle_interocular_angles(self):
        for line in self.interocular_lines:
            if not self.show_interocular_angles:
                self.screen.itemconfig(line.screen_ref, state="hidden")
            else:
                self.screen.itemconfig(line.screen_ref, state="normal")

    def complete_workspace(self):
        self.hide_all_visual_marks()
        self.add_angles()
        self.readd_all_visual_marks()
        self.add_additional_marks()
        self.toggle_malar_angles()
        self.toggle_interocular_angles()
        self.toggle_chin_angles()

    def add_angles(self):
        self.lines = self.get_collection_of_lines()
        for line in self.lines:
            line.screen_ref = self.create_line(line)

    def get_collection_of_lines(self):
        self.malar_lines = []
        self.interocular_lines = []
        self.chin_lines = []
        face = self.patient.values
        width = 4
        self.create_guideline(face)
        self.interocular_lines += face.angles.outer_eye_middle.get_predominance_lines(width=width)
        self.interocular_lines += face.angles.inner_eye_middle.get_predominance_lines(width=width)
        self.interocular_lines += face.angles.nose_eye_outer.get_predominance_lines(width=width)
        self.interocular_lines += face.angles.nose_eye_inner.get_predominance_lines(width=width)
        self.interocular_lines += face.angles.nose_middle.get_predominance_lines(width=width)
        self.interocular_lines += face.angles.cheekbone_middle.get_predominance_lines(width=width)
        self.interocular_lines += face.angles.nose_nose_point.get_predominance_lines(width=width)
        self.interocular_lines += face.angles.cheek_middle.get_predominance_lines(width=width)
        self.interocular_lines += face.angles.mouth_middle.get_predominance_lines(width=width)

        self.malar_lines += face.angles.malar_internal_cant.get_predominance_lines(width=width)
        self.malar_lines += face.angles.malar_nose.get_predominance_lines(width=width)
        self.malar_lines += face.angles.malar_middle.get_predominance_lines(width=width)
        self.malar_lines += face.angles.malar_nose_point.get_predominance_lines(width=width)

        self.chin_lines += face.angles.cheek_chin.get_predominance_lines(width=width)
        self.chin_lines += face.angles.mouth_chin.get_predominance_lines(width=width)
        self.chin_lines += face.angles.cheekbone_chin.get_predominance_lines(width=width)
        return self.chin_lines + self.interocular_lines + self.malar_lines

    def create_guideline(self, face):
        width = 4
        vertical_line = Line(face.middle, face.chin)
        start_line = Line(Point(-10000, 0), Point(10000, 0))
        top_point = intersects(vertical_line, start_line)
        if top_point is not None:
            self.guideline = Line(top_point, face.chin, color=cs.GREEN, w=width, dash=(4, 4))
        else:
            self.guideline = Line(face.middle, face.chin, color=cs.GREEN, w=width, dash=(4, 4))
        self.guideline.screen_ref = self.create_line(self.guideline)

    def process_move(self, p):
        x = self.order.get_next()
        if x == FrontalOrder.HORIZONTAL_LINE:
            self.remove_guideline()
            self.create_guideline(p)

    def reset_instance(self):
        self.patient.values = FrontalFace()


class AxialWorkspace(Workspace):

    def __init__(self):
        super().__init__()
        self.lines = []
        self.order = AxialOrder

    def assign_point_to_face_pos_and_return_if_completed(self, p):
        if self.order.is_completed():
            return False
        x = self.order.get_next()
        if self.in_box(p) and x and not self._check_for_too_close_neighbors(p):
            color = cs.GREEN
            if x == AxialOrder.CENTRAL_POINT:
                self.patient.values.central_point = p
                self.create_guideline(p)
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
                self.marks.append(self._create_visual_mark(p, r=4, color=color))
        return self.order.is_completed()

    def add_additional_marks(self):
        pass

    def create_guideline(self, p):
        self.guideline = Line(Point(p.x, self.rect.top), Point(p.x, self.rect.bottom), color=cs.YELLOW, w=3, dash=(4, 4))
        self.guideline.screen_ref = self.create_line(self.guideline)

    def add_angles(self):
        self.lines = self.get_collection_of_lines()
        for line in self.lines:
            line.screen_ref = self.create_line(line)

    def get_collection_of_lines(self):
        lines = []
        axial = self.patient.values
        width = 4
        top = Point(axial.central_point.x, 0)
        vertical_line = Line(axial.central_point, top, color=cs.RED, w=width, dash=(4, 4))
        lines.append(vertical_line)
        break_line = Line(axial.break_point, axial.point_nose, color=cs.ORANGE, w=width)
        lines.append(break_line)
        lines += axial.angles.central_point_wall.get_lines(cs.BLUE, width)
        lines += axial.angles.nose_point_wall.get_lines(cs.GREEN, width)
        lines += axial.angles.nose_point_maxilar.get_lines(cs.YELLOW, width)
        return lines

    def reset_instance(self):
        self.patient.values = AxialFace()
