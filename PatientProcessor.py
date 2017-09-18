from geometry import Point
from workAreas import Reference, Workspace, ProportionsTable
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
    toplevel = tk.Toplevel()
    ProportionsTable.showProportions(toplevel, patient, Workspace.complete, Workspace.showUpperMeasures,
                                             Workspace.showLowerMeasures, Workspace.showUpperAngles,
                                             Workspace.showLowerAngles)

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
    elif command == Commands.REPEAT:
        return
    elif command == Commands.MEASUREMENTS_DONE:
        pos += 1
        patient = Workspace.processFullPatient(patient)
        Loader.savePatient(patient)
    Reference.processClick(p, pos)
    
def on_closing():
    if not Workspace.complete: 
        if gui.boolbox(ms["on_close"], ms["exit"], [ms["yes"], ms["no"]]):
            root.destroy()
            ngui.start()
    else:
        root.destroy()
        ngui.start()
    
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
    Workspace.showUpperMeasuresUI = tk.BooleanVar(value=True)
    Workspace.showLowerMeasuresUI = tk.BooleanVar(value=True)
    Workspace.showUpperAnglesUI = tk.BooleanVar(value=True)
    Workspace.showLowerAnglesUI = tk.BooleanVar(value=True)
    Workspace.showMalarMeasuresUI = tk.BooleanVar(value=True)
    
    upperAnglesCheckbox = tk.Checkbutton(embed, text=ms["show_upper_angles"], variable=Workspace.showUpperAnglesUI,
                                         command=Workspace.toggleUpperAngles)
    lowerAnglesCheckbox = tk.Checkbutton(embed, text=ms["show_lower_angles"], variable=Workspace.showLowerAnglesUI,
                                         command=Workspace.toggleLowerAngles)
    upperMeasuresCheckbox = tk.Checkbutton(embed, text=ms["show_upper_measures"],
                                           variable=Workspace.showUpperMeasuresUI,
                                           command=Workspace.toggleUpperMeasures)
    lowerMeasuresCheckbox = tk.Checkbutton(embed, text=ms["show_lower_measures"],
                                           variable=Workspace.showLowerMeasuresUI,
                                           command=Workspace.toggleLowerMeasures)
    malarMeasuresCheckbox = tk.Checkbutton(embed, text=ms["show_malar_measures"],
                                           variable=Workspace.showMalarMeasuresUI,
                                           command=Workspace.toggleMalarMeasures)
    
    propsBtn = tk.Button(embed, text=ms["show_props"], command=showProportions, width=15)

    clearBtn = tk.Button(embed, text=ms["delete_all"], command=deleteAll, width=15)

    screen = tk.Canvas(root, width=ww, height=wh)
    screen.grid(row=0, column=1, sticky=tk.W+tk.N)
    upperMeasuresCheckbox.grid(sticky=tk.W)
    upperAnglesCheckbox.grid(sticky=tk.W)
    lowerMeasuresCheckbox.grid(sticky=tk.W)
    lowerAnglesCheckbox.grid(sticky=tk.W)
    malarMeasuresCheckbox.grid(sticky=tk.W)
    propsBtn.grid(sticky=tk.W, padx=6)
    deleteBtn.grid(sticky=tk.W, padx=6)
    clearBtn.grid(sticky=tk.W+tk.S, pady=35, padx=6)
    screen.grid(sticky=tk.W)
    Reference.load(refscreen, 0, 0, rw, rh)
    Workspace.load(screen, 0, 0, ww, wh)
    screen.bind("<Button-1>", mouse_up)
    screen.bind("<Motion>", mouse_move)
    if complete:
        pos = len(Order.order)
        patient = Workspace.loadCompletedPatient(patient)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.title("Facial Symmetry Analysis")
    tk.mainloop()
