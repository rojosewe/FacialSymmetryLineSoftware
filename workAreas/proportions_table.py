from tkinter.ttk import Treeview
import tkinter as tk
from utils.Messages import messages as ms
from workAreas.state_manager import get_patient


class AxialProportions:

    def __init__(self):
        patient = get_patient()
        self.p = patient.axial.proportions
        self.a = patient.axial.angles

    def showProportions(self, tableFrame, complete):
        if not complete:
            return
        self.addAngleTable(tableFrame)

    def addAngleTable(self, tableFrame):
        angle_label = tk.Label(tableFrame, text=ms.get("angles"))
        angle_label.grid(sticky=tk.W, padx=10)
        tm = Treeview(tableFrame, height=12)
        tm["columns"] = "left", "right", "differential", "orientation"
        tm.heading("left", text=ms.get("right"))
        tm.heading("right", text=ms.get("left"))
        tm.heading("differential", text=ms.get("differential"))
        tm.heading("orientation", text=ms.get("orientation"))
        tm.insert("", 0, text="{wall_left} - {central_point} - {wall_right}".format_map(ms),
                  values=(self.getAngle(self.a.central_point_wall_left), self.getAngle(self.a.central_point_wall_right),
                          self.getDifferential(self.p.central_point_wall),
                          self.getOrientation(self.p.central_point_wall)))
        tm.insert("", 0, text="{nose_point} - {nasal_point} - {wall_left}".format_map(ms),
                  values=(self.getAngle(self.a.nose_point_wall_left), self.getAngle(self.a.nose_point_wall_right),
                          self.getDifferential(self.p.nose_point_wall),
                          self.getOrientation(self.p.nose_point_wall)))
        tm.insert("", 0, text="{break_point}".format_map(ms),
                  values=(self.getAngle(self.a.break_point_nose_point), self.getAngle(self.a.break_point_nose_point),
                          "0", ""))
        tm.grid()

    def getOrientation(self, p):
        if p > 1:
            return ms.get("right")
        if p < 1:
            return ms.get("left")
        if p == 0:
            return ""

    def getMeasurement(self, m):
        return "%.2f px" % m

    def getAngle(self, a):
        return "%.2fº" % a

    def getDifferential(self, p):
        if p > 1.0:
            d = (p - 1) * 100
            return "%.2f %%" % d
        elif p < 1.0:
            d = (1 - p) * 100
            return "%.2f %%" % d
        else:
            return ""
