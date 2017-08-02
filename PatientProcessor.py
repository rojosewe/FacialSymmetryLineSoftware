from geometry import Point
from workAreas import Reference, Workspace
from utils.Messages import messages as ms
from utils import Commands, Loader
import easygui as gui
import tkinter as tk

def getPoint(event):
    p = (event.x, event.y)
    return Point(p[0], p[1])        

pos = 0
root = None
patient = None


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
    a = {}
    z = {}
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
- {internal_cant}:   {a_0}
- {external_cant}:   {a_1}
- {trago}:           {a_2}
- {reborde_alar}:   {a_3}
- {mouth}:  {a_4}
- {mandibular_angle}: {a_5}
{angular_proportions}:
- {glabelar} - {internal_cant}:   {a_6}
- {glabelar} - {external_cant}:   {a_7}
- {glabelar} - {trago}:           {a_8}
- {glabelar} - {reborde_alar}:   {a_9}
- {glabelar} - {mouth}:  {a_10}
- {glabelar} - {mandibular_angle}: {a_11}
- {pogonion} - {trago}:           {a_12}
- {pogonion} - {mouth}:  {a_13}
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
    
def load(x_patient, complete=False, loaded=False):
    global pos, root, patient
    patient = x_patient
    
    root = tk.Tk()
    rw, rh = Reference.init()
    ww, wh = Workspace.init(patient)
    if complete:
        pos = 2000
    left = 0
    top = 0
    right = rw + ww
    bottom = max(rh, wh)
    embed = tk.Frame(root, width = right, height = bottom)
    deleteBtn = tk.Button(root, text=ms["delete_last"], command=deleteMark)
    deleteBtn.pack()
    clearBtn = tk.Button(root, text=ms["delete_all"], command=deleteAll)
    clearBtn.pack()
    Workspace.showAnglesUI = tk.BooleanVar(value=True)
    Workspace.showMeasuresUI = tk.BooleanVar(value=True)
    anglesCheckbox = tk.Checkbutton(root, text=ms["show_angles"], variable=Workspace.showAnglesUI, 
                            command=Workspace.toggleAngles)
    anglesCheckbox.pack()
    mesauresCheckbox = tk.Checkbutton(root, text=ms["show_measures"], variable=Workspace.showMeasuresUI,
                            command=Workspace.toggleMeasures)
    mesauresCheckbox.pack()
    propsBtn = tk.Button(root, text=ms["show_props"], command=showProportions)
    propsBtn.pack()
    
    screen = tk.Canvas(embed, width=right, height=bottom)
    screen.pack()
    Reference.load(screen, left, top, rw, rh)
    Workspace.load(screen, rw, 0, right, wh)
    screen.bind("<Button-1>", mouse_up)
    screen.bind("<Motion>", mouse_move)
    embed.pack(side = tk.LEFT) #packs window to the left
    tk.mainloop()
    
# "show_props": "Proportions"