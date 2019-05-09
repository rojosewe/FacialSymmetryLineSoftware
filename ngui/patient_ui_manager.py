from geometry import Point
from workAreas.reference.axial import AxialReference
from workAreas.reference.frontal import FrontalReference
from workAreas.workspace import AxialWorkspace, FrontalWorkspace
from facial_measures.order import AxialOrder, FrontalOrder
from workAreas.proportions_table import AxialProportionsTable, FrontalProportionsTable
from utils.Messages import messages as ms
from utils import JsonLoader
import tkinter as tk
import easygui as gui
import ngui


class PatientManager:

    def load(self):
        rw, rh = self.reference.get_image_size()
        ww, wh = self.workspace.get_image_size()
        embed = tk.Frame(self.root, width=rw, height=wh)
        embed.grid(row=0, column=0)
        next_point_static_label = tk.Label(embed, text=ms.get("next_point") + ":")
        next_point_static_label.grid(sticky=tk.W, padx=10)
        next_point_label_text = tk.StringVar()
        next_point_label = tk.Label(embed, textvariable=next_point_label_text)
        next_point_label.grid(sticky=tk.W, padx=10)
        refscreen = tk.Canvas(embed, width=rw, height=rh)
        refscreen.grid(sticky=tk.N + tk.W)
        screen = self.load_ui_wokspace(embed, self.root, wh, ww)
        self.reference.load_screen(refscreen, 0, 0, rw, rh, next_point_label_text)
        self.workspace.load_screen(screen, 0, 0, ww, wh)
        screen.bind("<Button-1>", self.mouse_up)
        screen.bind("<Motion>", self.mouse_move)
        refscreen.bind("<Button-1>", self.print_ref_point)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.title("Facial Symmetry Analysis")
        tk.mainloop()

    def load_ui_wokspace(self, embed, root, wh, ww):
        deleteBtn = tk.Button(embed, text=ms["delete_last"], command=self.delete_mark, width=15)
        propsBtn = tk.Button(embed, text=ms["show_props"], command=self.show_proportions, width=15)
        clearBtn = tk.Button(embed, text=ms["delete_all"], command=self.delete_all, width=15)
        screen = tk.Canvas(root, width=ww, height=wh)
        screen.grid(row=0, column=1, sticky=tk.W + tk.N)
        propsBtn.grid(sticky=tk.W, padx=6)
        deleteBtn.grid(sticky=tk.W, padx=6)
        clearBtn.grid(sticky=tk.W + tk.S, pady=35, padx=6)
        screen.grid(sticky=tk.W)
        return screen

    def get_point(self, event):
        p = (event.x, event.y)
        return Point(p[0], p[1])

    def delete_mark(self):
        self.workspace.undo_previous_action()
        self.reference.draw()

    def delete_all(self):
        self.workspace.clean()
        self.reference.draw()

    def mouse_move(self, event):
        p = self.get_point(event)
        self.workspace.process_move(p)

    def mouse_up(self, event):
        p = self.get_point(event)
        completed = self.workspace.process_click_return_if_completed(event, p)
        self.reference.process_click()
        if completed:
            JsonLoader.save_patient()

    def print_ref_point(self, event):
        p = self.get_point(event)
        print(p)

    def on_closing(self):
        if not self.order.is_completed():
            if gui.boolbox(ms["on_close"], ms["exit"], [ms["yes"], ms["no"]]):
                self.workspace.restart()
                self.root.destroy()
                ngui.start()
        else:
            self.workspace.restart()
            self.root.destroy()
            ngui.start()


class AxialPatientManager(PatientManager):

    def __init__(self):
        self.root = tk.Tk()
        self.reference = AxialReference()
        self.workspace = AxialWorkspace()
        self.order = AxialOrder

    def show_proportions(self):
        toplevel = tk.Toplevel()
        AxialProportionsTable().showProportions(toplevel, self.order.is_completed())


class FrontalPatientManager(PatientManager):

    def __init__(self):
        self.root = tk.Tk()
        self.reference = FrontalReference()
        self.workspace = FrontalWorkspace()
        self.order = FrontalOrder

    def show_proportions(self):
        toplevel = tk.Toplevel()
        FrontalProportionsTable().showProportions(toplevel, self.order.is_completed())
