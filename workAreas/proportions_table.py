from tkinter.ttk import Treeview
import tkinter as tk
from utils.Messages import messages as ms
from workAreas.state_manager import get_patient


# REMINDER: WHEN WE SHOW THE TABLE ALL VALUES ARE MIRRORED LEFT - RIGHT!!!
class SymmetryAngleProportionValue:

    def __init__(self, angle):
        self.angle = angle

    def get_orientation(self):
        # L / R
        p = self.angle.get_proportion()
        if p > 1:
            #code left
            return ms.get("right")
        elif p < 1:
            #code right
            return ms.get("left")

        else:
            return ""

    def get_angle_left(self):
        return "%.2fº" % self.angle.left_angle

    def get_angle_right(self):
        return "%.2fº" % self.angle.right_angle

    def get_differential(self):
        # L / R
        p = self.angle.get_proportion()
        if p > 1.0:
            d = (p - 1) * 100
            return "%.2f %%" % d
        elif p < 1.0:
            d = (1 - p) * 100
            return "%.2f %%" % d
        else:
            return ""

    def get_value(self):
        return self.get_angle_left(), self.get_angle_right(), self.get_differential(), self.get_orientation()


# REMINDER: WHEN WE SHOW THE TABLE ALL VALUES ARE MIRRORED LEFT - RIGHT!!!
class DisplacementAngleProportionValue:

    def __init__(self, angle):
        self.angle = angle

    def get_orientation(self):
        p = self.angle.get_displacement_x()
        if p > 0:
            # code left
            return ms.get("right")
        if p < 0:
            # code right
            return ms.get("left")
        if p == 0:
            return ""

    def get_angle(self):
        return "%.2fº" % self.angle.get_angle()

    def get_value(self):
        return self.get_angle(), self.get_orientation(), "", ""


class ProportionsTable:

    def __init__(self):
        patient = get_patient()
        self.a = patient.values.angles


class AxialProportionsTable(ProportionsTable):

    def showProportions(self, table_frame, complete):
        if not complete:
            return
        self.addAngleTable(table_frame)
        self.add_breaking_point_table(table_frame)

    def addAngleTable(self, table_frame):
        angle_label = tk.Label(table_frame, text=ms.get("angles"))
        angle_label.grid(sticky=tk.W, padx=10)
        tm = Treeview(table_frame, height=3)
        tm["columns"] = "left", "right", "differential", "orientation"
        tm.heading("left", text=ms.get("right"))
        tm.heading("right", text=ms.get("left"))
        tm.heading("differential", text=ms.get("differential"))
        tm.heading("orientation", text=ms.get("orientation"))
        tm.column("#0", width=300)
        central_point_wall_row = SymmetryAngleProportionValue(self.a.central_point_wall)
        tm.insert("", 0, text="{walls} - {central_point}".format_map(ms), values=central_point_wall_row.get_value())
        nose_point_wall_row = SymmetryAngleProportionValue(self.a.nose_point_wall)
        tm.insert("", 0, text="{walls} - {nose_point}".format_map(ms), values=nose_point_wall_row.get_value())
        nose_point_maxilar_row = SymmetryAngleProportionValue(self.a.nose_point_maxilar)
        tm.insert("", 0, text="{maxilars} - {nose_point}".format_map(ms), values=nose_point_maxilar_row.get_value())
        tm.grid()

    def add_breaking_point_table(self, table_frame):
        angle_label = tk.Label(table_frame, text=ms.get("break_point"))
        angle_label.grid(sticky=tk.W, padx=10)
        tm = Treeview(table_frame, height=1)
        tm["columns"] = "angle", "deviation", "", ""
        tm.heading("angle", text=ms.get("angle"))
        tm.heading("deviation", text=ms.get("deviation"))
        tm.heading("", text="")
        tm.heading("", text="")
        tm.column("#0", width=300)
        break_point_row = DisplacementAngleProportionValue(self.a.break_point_nose_point)
        tm.insert("", 0, text="{break_point}".format_map(ms),
                  values=break_point_row.get_value())
        tm.grid()


class FrontalProportionsTable(ProportionsTable):

    def showProportions(self, table_frame, complete):
        if not complete:
            return
        self.addAngleTable(table_frame)
        self.addMalarTable(table_frame)

    def addAngleTable(self, table_frame):
        angle_label = tk.Label(table_frame, text=ms.get("angles"))
        angle_label.grid(sticky=tk.W, padx=10)
        tm = Treeview(table_frame, height=11)
        tm["columns"] = "left", "right", "differential", "orientation"
        tm.heading("left", text=ms.get("right"))
        tm.heading("right", text=ms.get("left"))
        tm.heading("differential", text=ms.get("differential"))
        tm.heading("orientation", text=ms.get("orientation"))
        tm.column("#0", width=300)
        row = SymmetryAngleProportionValue(self.a.outer_eye_middle)
        tm.insert("", 0, text="{eye_outer} - {middle}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.inner_eye_middle)
        tm.insert("", 0, text="{eye_inner} - {middle}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.cheek_middle)
        tm.insert("", 0, text="{cheek} - {middle}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.nose_middle)
        tm.insert("", 0, text="{nose} - {middle}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.mouth_middle)
        tm.insert("", 0, text="{mouth} - {middle}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.cheekbone_middle)
        tm.insert("", 0, text="{cheekbone} - {middle}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.cheek_chin)
        tm.insert("", 0, text="{cheek} - {chin}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.mouth_chin)
        tm.insert("", 0, text="{mouth} - {chin}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.cheekbone_chin)
        tm.insert("", 0, text="{cheekbone} - {chin}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.nose_eye_outer)
        tm.insert("", 0, text="{nose_point} - {eye_outer}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.nose_eye_inner)
        tm.insert("", 0, text="{nose_point} - {eye_inner}".format_map(ms), values=row.get_value())
        tm.grid()

    def addMalarTable(self, table_frame):
        angle_label = tk.Label(table_frame, text=ms.get("malar"))
        angle_label.grid(sticky=tk.W, padx=10)
        tm = Treeview(table_frame, height=4)
        tm["columns"] = "left", "right", "differential", "orientation"
        tm.heading("left", text=ms.get("right"))
        tm.heading("right", text=ms.get("left"))
        tm.heading("differential", text=ms.get("differential"))
        tm.heading("orientation", text=ms.get("orientation"))
        tm.column("#0", width=300)
        row = SymmetryAngleProportionValue(self.a.malar_nose)
        tm.insert("", 0, text="{malar} - {nose}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.malar_vertical)
        tm.insert("", 0, text="{malar} - {vertical}".format_map(ms), values=row.get_value())
        row = SymmetryAngleProportionValue(self.a.malar_internal_cant)
        tm.insert("", 0, text="{malar} - {eye_inner}".format_map(ms), values=row.get_value())
        tm.grid()
