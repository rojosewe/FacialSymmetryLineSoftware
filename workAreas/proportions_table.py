from tkinter.ttk import Treeview
import tkinter as tk
from utils.Messages import messages as ms
from workAreas.state_manager import get_patient


class Proportions:

    def __init__(self):
        patient = get_patient()
        self.p = patient.values.proportions
        self.a = patient.values.angles

    def getOrientation(self, p):
        if p > 0:
            return ms.get("right")
        if p < 0:
            return ms.get("left")
        if p == 0:
            return ""

    def get_measurement(self, m):
        return "%.2f px" % m

    def get_angle(self, a):
        return "%.2fº" % a

    def get_differential(self, p):
        if p > 1.0:
            d = (p - 1) * 100
            return "%.2f %%" % d
        elif p < 1.0:
            d = (1 - p) * 100
            return "%.2f %%" % d
        else:
            return ""


class AxialProportions(Proportions):

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
        tm.insert("", 0, text="{walls} - {central_point}".format_map(ms),
                  values=(self.get_angle(self.a.central_point_wall_left), self.get_angle(self.a.central_point_wall_right),
                          self.get_differential(self.p.central_point_wall),
                          self.getOrientation(self.p.central_point_wall)))
        tm.insert("", 0, text="{walls} - {nose_point}".format_map(ms),
                  values=(self.get_angle(self.a.nose_point_wall_left), self.get_angle(self.a.nose_point_wall_right),
                          self.get_differential(self.p.nose_point_wall),
                          self.getOrientation(self.p.nose_point_wall)))
        tm.insert("", 0, text="{maxilars} - {nose_point}".format_map(ms),
                  values=(self.get_angle(self.a.nose_point_maxilar_left), self.get_angle(self.a.nose_point_maxilar_right),
                          self.get_differential(self.p.nose_point_maxilar),
                          self.getOrientation(self.p.nose_point_maxilar)))
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
        tm.insert("", 0, text="{break_point}".format_map(ms),
                  values=(self.get_angle(self.a.break_point_nose_point),
                          self.getOrientation(self.p.break_point_nose_point),
                          "", ""))
        tm.grid()


class FrontalProportions(Proportions):

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

        tm.grid()