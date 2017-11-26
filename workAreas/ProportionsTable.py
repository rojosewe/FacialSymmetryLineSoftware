from tkinter.ttk import Treeview
import tkinter as tk
from utils.Messages import messages as ms

def getOrientation(p):
    if p > 1:
        return ms.get("right")
    if p < 1:
        return ms.get("left")
    if p == 0:
        return ""
    
def getMeasurement(m):
    return "%.2f px" % m

def getAngle(a):
    return "%.2fº" % a

def getDifferential(p):
    if p > 1.0:
        d = (p - 1) * 100
        return "%.2f %%" % d
    elif p < 1.0:
        d = (1 - p) * 100
        return "%.2f %%" % d
    else:
        return ""
    

def addLengthTable(tableFrame, p, m, showUpperMeasures, showLowerMeasures):
    measure_label = tk.Label(tableFrame, text=ms.get("measurements"))
    measure_label.grid(sticky=tk.W, padx=10)
    tm = Treeview(tableFrame, height=9)
    tm["columns"] = "left", "right", "differential", "orientation"
    tm.heading("left", text=ms.get("right"))
    tm.heading("right", text=ms.get("left"))
    tm.heading("differential", text=ms.get("differential"))
    tm.heading("orientation", text=ms.get("orientation"))
    if showLowerMeasures:
        tm.insert("", 0, text=ms.get("mandibular_angle"), 
                  values=(getMeasurement(m.mandibleL), getMeasurement(m.mandibleR), 
                          getDifferential(p.mandibleLength), getOrientation(p.mandibleLength)))
        tm.insert("", 0, text=ms.get("mouth"), 
                  values=(getMeasurement(m.lipL), getMeasurement(m.lipR), 
                          getDifferential(p.lipLength), getOrientation(p.lipLength))) 
    if showUpperMeasures:
        tm.insert("", 0, text=ms.get("nasal_point") + " - " + ms.get("external_cant"), 
                  values=(getMeasurement(m.noseCExternalCantL), getMeasurement(m.noseCExternalCantR), 
                          getDifferential(p.NoseCExternalCantLength), getOrientation(p.NoseCExternalCantLength)))
        tm.insert("", 0, text=ms.get("nasal_point") + " - " + ms.get("internal_cant"), 
                  values=(getMeasurement(m.noseCInternalCantL), getMeasurement(m.noseCInternalCantR), 
                          getDifferential(p.NoseCInternalCantLength), getOrientation(p.NoseCInternalCantLength)))
        tm.insert("", 0, text=ms.get("reborde_alar"), 
                  values=(getMeasurement(m.rebordeAlarL), getMeasurement(m.rebordeAlarR), 
                          getDifferential(p.rebordeAlarLength), getOrientation(p.rebordeAlarLength)))
        tm.insert("", 0, text=ms.get("trago"), 
                  values=(getMeasurement(m.tragoL), getMeasurement(m.tragoR), 
                          getDifferential(p.tragoLength), getOrientation(p.tragoLength)))
        tm.insert("", 0, text=ms.get("external_cant"), 
                  values=(getMeasurement(m.externalCantL), getMeasurement(m.externalCantR), 
                          getDifferential(p.externalCantLength), getOrientation(p.externalCantLength)))
        tm.insert("", 0, text=ms.get("internal_cant"), 
                  values=(getMeasurement(m.internalCantL), getMeasurement(m.internalCantR), 
                          getDifferential(p.internalCantLength), getOrientation(p.internalCantLength)))
    tm.grid()
    average_label = tk.Label(tableFrame, 
                             text="{total_length_move_lbl}: {total_length_move}. {side_lbl}: {side}"
                             .format_map({"total_length_move_lbl": ms.get("total_length_move"),
                                          "total_length_move": getDifferential(p.lengthAverage),
                                          "side_lbl": ms.get("orientation"),
                                          "side": getOrientation(p.lengthAverage)}))
    average_label.grid(sticky=tk.W, padx=10)
    
def addMalarTable(tableFrame, p, m, a, showMalarMeasures):
    if showMalarMeasures:
        malar_label = tk.Label(tableFrame, text=ms.get("malar"))
        malar_label.grid(sticky=tk.W, padx=10)
        tm = Treeview(tableFrame, height=4)
        tm["columns"] = "left", "right", "differential", "orientation"
        tm.heading("left", text=ms.get("right"))
        tm.heading("right", text=ms.get("left"))
        tm.heading("differential", text=ms.get("differential"))
        tm.heading("orientation", text=ms.get("orientation"))
        tm.insert("", 0, text=ms.get("malar") + " - " + ms.get("external_cant"), 
                  values=(getMeasurement(m.malarL), getMeasurement(m.malarR), 
                          getDifferential(p.malarLength), getOrientation(p.malarLength)))
        tm.insert("", 0, text=ms.get("nasal_point") + " - " + ms.get("malar"), 
                  values=(getMeasurement(m.noseCMalarL), getMeasurement(m.noseCMalarR), 
                          getDifferential(p.NoseCmalarLength), getOrientation(p.NoseCmalarLength)))
        tm.insert("", 0, text="{nasal_point} - {malar}".format_map(ms),
                  values=(getAngle(a.angleNoseCMalarL), getAngle(a.angleNoseCMalarR), 
                          getDifferential(p.angleNoseCMalarAngle), 
                          getOrientation(p.angleNoseCMalarAngle)))
        tm.grid()
    
def addAngleTable(tableFrame, p, a, showUpperAngles, showLowerAngles):
    angle_label = tk.Label(tableFrame, text=ms.get("angles"))
    angle_label.grid(sticky=tk.W, padx=10)
    tm = Treeview(tableFrame, height=12)
    tm["columns"] = "left", "right", "differential", "orientation"
    tm.heading("left", text=ms.get("right"))
    tm.heading("right", text=ms.get("left"))
    tm.heading("differential", text=ms.get("differential"))
    tm.heading("orientation", text=ms.get("orientation"))
    if showLowerAngles:
        # --------------------
        tm.insert("", 0, text="{pogonion} - {mandibular_angle}".format_map(ms),
                  values=(getAngle(a.angle13), getAngle(a.angle18), 
                          getDifferential(p.pogonionMandibularAngle), 
                          getOrientation(p.pogonionMandibularAngle)))
        tm.insert("", 0, text="{pogonion} - {mouth}".format_map(ms),
                  values=(getAngle(a.angle15), getAngle(a.angle16), 
                          getDifferential(p.pogonionLabialAngle), 
                          getOrientation(p.pogonionLabialAngle)))
        tm.insert("", 0, text="{pogonion} - {trago}".format_map(ms),
                  values=(getAngle(a.angle14), getAngle(a.angle17), 
                          getDifferential(p.pogonionTragoAngle), 
                          getOrientation(p.pogonionTragoAngle)))
        tm.insert("", 0, text="{glabelar} - {mandibular_angle}".format_map(ms),
                  values=(getAngle(a.angle4), getAngle(a.angle9), 
                          getDifferential(p.glablearMadibularAngle), 
                          getOrientation(p.glablearMadibularAngle)))
        tm.insert("", 0, text="{glabelar} - {mouth}".format_map(ms),
                  values=(getAngle(a.angle6), getAngle(a.angle7), 
                          getDifferential(p.glablearLabialAngle), 
                          getOrientation(p.glablearLabialAngle)))
    if showUpperAngles:
        tm.insert("", 0, text="{nasal_point} - {external_cant}".format_map(ms),
                  values=(getAngle(a.angleNoseCExternalCantL), getAngle(a.angleNoseCExternalCantR), 
                          getDifferential(p.angleNoseCExternalCantAngle), 
                          getOrientation(p.angleNoseCExternalCantAngle)))
        tm.insert("", 0, text="{nasal_point} - {internal_cant}".format_map(ms),
                  values=(getAngle(a.angleNoseCInternalCantL), getAngle(a.angleNoseCInternalCantR), 
                          getDifferential(p.angleNoseCInternalCantAngle), 
                          getOrientation(p.angleNoseCInternalCantAngle)))
        tm.insert("", 0, text="{glabelar} - {reborde_alar}".format_map(ms),
                  values=(getAngle(a.angle5), getAngle(a.angle8), 
                          getDifferential(p.glablearNasalAngle), 
                          getOrientation(p.glablearNasalAngle)))
        tm.insert("", 0, text="{glabelar} - {trago}".format_map(ms),
                  values=(getAngle(a.angle2), getAngle(a.angle11), 
                          getDifferential(p.glablearTragoAngle), 
                          getOrientation(p.glablearTragoAngle)))
        tm.insert("", 0, text="{glabelar} - {external_cant}".format_map(ms),
                  values=(getAngle(a.angle1), getAngle(a.angle12), 
                          getDifferential(p.glabelarCantoExtAngle), 
                          getOrientation(p.glabelarCantoExtAngle)))
        tm.insert("", 0, text="{glabelar} - {internal_cant}".format_map(ms),
                  values=(getAngle(a.angle3), getAngle(a.angle10), 
                          getDifferential(p.glabelarCantoIntAngle), 
                          getOrientation(p.glabelarCantoIntAngle)))
    tm.grid()
    average_label = tk.Label(tableFrame, 
                             text="{total_angle_move_lbl}: {total_angle_move}. {side_lbl}: {side}"
                             .format_map({"total_angle_move_lbl": ms.get("total_angle_move"),
                                          "total_angle_move": getDifferential(p.angleAverage),
                                          "side_lbl": ms.get("orientation"),
                                          "side": getOrientation(p.angleAverage)}))
    average_label.grid(sticky=tk.W, padx=10)

def showProportions(tableFrame, patient, complete, showUpperMeasures, showMalarMeasures,
                    showLowerMeasures, showUpperAngles, showLowerAngles):
    if not complete:
        return
    p = patient.proportions
    m = patient.measurements
    a = patient.angles
    addAngleTable(tableFrame, p, a, showUpperAngles, showLowerAngles)
    addLengthTable(tableFrame, p, m, showUpperMeasures, showLowerMeasures)
    addMalarTable(tableFrame, p, m, a, showMalarMeasures)