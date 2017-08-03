from geometry import Point
from workAreas import Reference, Workspace
from utils.Messages import messages as ms
from utils import Commands, Loader
import tkinter as tk
import easygui as gui
from facial_measures import Order
import ngui

pos = 0
root = None
patient = None

def getPoint(event):
    p = (event.x, event.y)
    return Point(p[0], p[1])

def humanLengthProps(prop):
    if prop > 1.0:
        d = (prop - 1) * 100
        return ms["right_displacement"].format(d)
    elif prop < 1.0:
        d = (1 - prop) * 100
        return ms["left_displacement"].format(d)
    else:
        return ms["no_displacement"]
    
def humanAngleProps(prop):
    if prop > 1.0:
        d = (prop - 1) * 100
        return ms["right_angle_displacement"].format(d)
    elif prop < 1.0:
        d = (1 - prop) * 100
        return ms["left_angle_displacement"].format(d)
    else:
        return ms["no_angle_displacement"]
    
def deleteMark():
    global pos
    Workspace.deleteLastMark(pos)
    pos = max(pos - 1, 0)
    Reference.draw(pos)
    
def deleteAll():
    global pos
    Workspace.clean()
    pos = 0
    Reference.draw(pos)
    
def newPatient():
    if Workspace.complete:
        return Commands.START
    else:
        if gui.boolbox("Exiting", "You are exiting. All progress in this patient will be lost.", ["OK", "Cancel"]):
            return Commands.START

def showProportions():
    if Workspace.complete:
        prop = patient.proportions
    else:
        return
    a = {}
    x = [humanLengthProps(prop.internalCantLength), humanLengthProps(prop.externalCantLength),
    humanLengthProps(prop.tragoLength), humanLengthProps(prop.rebordeAlarLength), 
    humanLengthProps(prop.lipLength), humanLengthProps(prop.mandibleLength),
    humanAngleProps(prop.glabelarCantoIntAngle), humanAngleProps(prop.glabelarCantoExtAngle),
    humanAngleProps(prop.glablearTragoAngle), humanAngleProps(prop.glablearNasalAngle), 
    humanLengthProps(prop.glablearLabialAngle), humanLengthProps(prop.glablearMadibularAngle),
    humanAngleProps(prop.pogonionTragoAngle), humanLengthProps(prop.pogonionLabialAngle), 
    humanLengthProps(prop.pogonionMandibularAngle)]
    for i in range(len(x)):
        a["a_" + str(i)] = x[i]
    z = ms.copy()
    z.update(a)
    
    msg = """
{measurements_props}:
- {internal_cant}: {a_0}
- {external_cant}: {a_1}
- {trago}: {a_2}
- {reborde_alar}: {a_3}
- {mouth}: {a_4}
- {mandibular_angle}: {a_5}
{angular_proportions}:
- {glabelar} - {internal_cant}: {a_6}
- {glabelar} - {external_cant}: {a_7}
- {glabelar} - {trago}: {a_8}
- {glabelar} - {reborde_alar}: {a_9}
- {glabelar} - {mouth}: {a_10}
- {glabelar} - {mandibular_angle}: {a_11}
- {pogonion} - {trago}: {a_12}
- {pogonion} - {mouth}: {a_13}
- {pogonion} - {mandibular_angle}: {a_14}
""".format_map(z) 
    gui.msgbox(msg, "measurements")                    

def mouse_move(event):
    global pos
    p = getPoint(event)
    Workspace.processMove(p, pos)
                
def mouse_up(event):
    global pos, patient
    p = getPoint(event)
    command = Workspace.processClick(event, p, pos)
    print(command)
    if command == Commands.NEXT:
        pos += 1
    elif command == Commands.MEASUREMENTS_DONE:
        pos += 1
        patient = Workspace.processFullPatient(patient)
        Loader.savePatient(patient)
    Reference.processClick(p, pos)
    
def on_closing():
    if not Workspace.complete: 
        if gui.boolbox(ms["on_close"], ms["exit"], [ms["yes"], ms["no"]]):
            root.destroy()
            ngui.start(ngui.home)
    else:
        root.destroy()
        ngui.start(ngui.home)
    
def load(x_patient, complete=False, loaded=False):
    global pos, root, patient
    patient = x_patient
    
    root = tk.Tk()
    rw, rh = Reference.init()
    try:
        ww, wh = Workspace.init(patient)
    except Exception:
        raise FileNotFoundError()
    embed = tk.Frame(root, width=rw, height=wh)
    embed.grid(row=0, column=0)
    refscreen = tk.Canvas(embed, width=rw, height=rh)
    refscreen.grid(sticky=tk.N+tk.W)
    deleteBtn = tk.Button(embed, text=ms["delete_last"], command=deleteMark, width=15)
    Workspace.showAnglesUI = tk.BooleanVar(value=True)
    Workspace.showMeasuresUI = tk.BooleanVar(value=True)
    anglesCheckbox = tk.Checkbutton(embed, text=ms["show_angles"], variable=Workspace.showAnglesUI,
                            command=Workspace.toggleAngles)
    measuresCheckbox = tk.Checkbutton(embed, text=ms["show_measures"], variable=Workspace.showMeasuresUI,
                            command=Workspace.toggleMeasures)
    propsBtn = tk.Button(embed, text=ms["show_props"], command=showProportions, width=15)

    clearBtn = tk.Button(embed, text=ms["delete_all"], command=deleteAll, width=15)

    screen = tk.Canvas(root, width=ww, height=wh)
    screen.grid(row=0, column=1, sticky=tk.W+tk.N)
    anglesCheckbox.grid(sticky=tk.W)
    measuresCheckbox.grid(sticky=tk.W)
    propsBtn.grid(sticky=tk.W)
    deleteBtn.grid(sticky=tk.W)
    clearBtn.grid(sticky=tk.W+tk.S, pady=35)
    screen.grid(sticky=tk.W)
    Reference.load(refscreen, 0, 0, rw, rh)
    Workspace.load(screen, 0, 0, ww, wh)
    screen.bind("<Button-1>", mouse_up)
    screen.bind("<Motion>", mouse_move)
    if complete:
        pos = len(Order.order)
        patient = Workspace.loadCompletedPatient(patient)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    tk.mainloop()
