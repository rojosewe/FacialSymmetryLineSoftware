from geometry import Point
from workAreas import Reference, Workspace, ProportionsTable
from utils.Messages import messages as ms
from utils import JsonLoader
import tkinter as tk
import easygui as gui
import ngui


root = None


def load():
    global pos, root
    root = tk.Tk()
    rw, rh = Reference.init()
    ww, wh = Workspace.init()
    embed = tk.Frame(root, width=rw, height=wh)
    embed.grid(row=0, column=0)
    refscreen = tk.Canvas(embed, width=rw, height=rh)
    refscreen.grid(sticky=tk.N + tk.W)
    screen = load_ui_wokspace(embed, root, wh, ww)
    Reference.load(refscreen, 0, 0, rw, rh)
    Workspace.load(screen, 0, 0, ww, wh)
    screen.bind("<Button-1>", mouse_up)
    screen.bind("<Motion>", mouse_move)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.title("Facial Symmetry Analysis")
    tk.mainloop()


def load_ui_wokspace(embed, root, wh, ww):
    deleteBtn = tk.Button(embed, text=ms["delete_last"], command=deleteMark, width=15)
    Workspace.showUpperAnglesUI = tk.BooleanVar(value=True)
    Workspace.showLowerAnglesUI = tk.BooleanVar(value=True)
    Workspace.showMalarMeasuresUI = tk.BooleanVar(value=True)
    Workspace.showUpperMeasuresUI = tk.BooleanVar(value=False)
    Workspace.showLowerMeasuresUI = tk.BooleanVar(value=False)
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
    screen.grid(row=0, column=1, sticky=tk.W + tk.N)
    upperAnglesCheckbox.grid(sticky=tk.W)
    lowerAnglesCheckbox.grid(sticky=tk.W)
    malarMeasuresCheckbox.grid(sticky=tk.W)
    upperMeasuresCheckbox.grid(sticky=tk.W)
    lowerMeasuresCheckbox.grid(sticky=tk.W)
    propsBtn.grid(sticky=tk.W, padx=6)
    deleteBtn.grid(sticky=tk.W, padx=6)
    clearBtn.grid(sticky=tk.W + tk.S, pady=35, padx=6)
    screen.grid(sticky=tk.W)
    return screen


def getPoint(event):
    p = (event.x, event.y)
    return Point(p[0], p[1])


def deleteMark():
    Workspace.undo_previous_action()
    Reference.draw()


def deleteAll():
    Workspace.clean()
    Reference.draw()


def showProportions():

    toplevel = tk.Toplevel()
    ProportionsTable.showProportions(toplevel, Workspace.is_completed(), Workspace.showUpperMeasures,
                                             Workspace.showMalarMeasures,
                                             Workspace.showLowerMeasures, Workspace.showUpperAngles,
                                             Workspace.showLowerAngles)


def mouse_move(event):
    p = getPoint(event)
    Workspace.processMove(p)


def mouse_up(event):
    p = getPoint(event)
    completed = Workspace.process_click_return_if_completed(event, p)
    Reference.processClick()
    if completed:
        JsonLoader.savePatient()

    
def on_closing():
    if not Workspace.is_completed():
        if gui.boolbox(ms["on_close"], ms["exit"], [ms["yes"], ms["no"]]):
            Workspace.restart()
            root.destroy()
            ngui.start()
    else:
        Workspace.restart()
        root.destroy()
        ngui.start()




