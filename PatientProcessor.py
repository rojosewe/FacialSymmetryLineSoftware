from geometry import Point
from workAreas import Reference, Workspace
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
        return "{0:.2f}% mas largo hacia la derecha.".format(d)
    elif prop < 1.0:
        d = (1 - prop) * 100
        return "{0:.2f}% mas largo hacia la izquierda.".format(d)
    else:
        return "Ambos lados son de distancia identica"
    
def humanAngleProps(prop):
    if prop > 1.0:
        d = (prop - 1) * 100
        return "{0:.2f}% mas amplio hacia la derecha.".format(d)
    elif prop < 1.0:
        d = (1 - prop) * 100
        return "{0:.2f}% mas amplio hacia la izquierda.".format(d)
    else:
        return "Ambos lados son de angulo identico"
    
def key_up(event):
    global pos
    command = Workspace.processKey(root, event)
    if command == Commands.DELETE_MARK:
        pos = max(pos - 1, 0)
        Workspace.deleteLastMark()
    elif command == Commands.CLEAR_MARKS:
        pos = 0
        Workspace.clean()
    elif command == Commands.START:
        if Workspace.complete:
            return Commands.START
        else:
            if gui.boolbox("Exiting", "You are exiting. All progress in this patient will be lost.", ["OK", "Cancel"]):
                return Commands.START
    elif command == Commands.SHOW_PROPORTIONS:
        if Workspace.complete:
            prop = patient.proportions
            
            msg = """
Proporciones Medida:
    - Canto interno :   %s
    - Canto externo :   %s
    - Trago :           %s
    - Reborder alar :   %s
    - Comisura bucal :  %s
    - Ang. mandibular : %s
Proporciones Angulares:
    - Glabelar - Canto interno :   %s
    - Glabelar - Canto externo :   %s
    - Glabelar - Trago :           %s
    - Glabelar - Reborder alar :   %s
    - Glabelar - Comisura bucal :  %s
    - Glabelar - Ang. mandibular : %s
    - Pogonion - Trago :           %s
    - Pogonion - Comisura bucal :  %s
    - Pogonion - Ang. mandibular : %s
""" % (humanLengthProps(prop.internalCantLength), humanLengthProps(prop.externalCantLength),
       humanLengthProps(prop.tragoLength), humanLengthProps(prop.rebordeAlarLength), 
       humanLengthProps(prop.lipLength), humanLengthProps(prop.mandibleLength),
       humanAngleProps(prop.glabelarCantoIntAngle), humanAngleProps(prop.glabelarCantoExtAngle),
       humanAngleProps(prop.glablearTragoAngle), humanAngleProps(prop.glablearNasalAngle), 
       humanLengthProps(prop.glablearLabialAngle), humanLengthProps(prop.glablearMadibularAngle),
       humanAngleProps(prop.pogonionTragoAngle), humanLengthProps(prop.pogonionLabialAngle), 
       humanLengthProps(prop.pogonionMandibularAngle))
            gui.msgbox(msg, "measurements")                    
    elif command == None:
        if event.char == "q":
            return Commands.EXIT
                
                
def mouse_up(event):
    global pos
    p = getPoint(event)
    command = Workspace.processClick(event, p, pos)
    print(command)
    if command == Commands.NEXT:
        pos += 1
    elif command == Commands.MEASUREMENTS_DONE:
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
    embed.pack(side = tk.LEFT) #packs window to the left
    screen = tk.Canvas(embed, width=right, height=bottom)
    screen.pack()
    Reference.load(screen, left, top, rw, rh)
    Workspace.load(screen, rw, 0, right, wh)
    screen.bind("<Key>", key_up)
    screen.bind("<Button-1>", mouse_up)
    tk.mainloop()