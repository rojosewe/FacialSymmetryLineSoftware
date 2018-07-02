from utils import JsonLoader
from ngui import patient_ui_manager
import easygui as gui
from utils.Messages import messages as ms
from utils.conf import Conf as cf
from workAreas.state_manager import set_patient
from facial_measures.frontal_face_order import *


def select_patient():
    msg = ms["select_patient"]
    title = ms["patients"]
    choices = JsonLoader.getAllPatientsNames()
    choice = gui.choicebox(msg, title, choices)
    if choice is None:
        return None
    else:
        return _open_patient(choice)


def _open_patient(name):
    try:
        patient = JsonLoader.getPatient(name)
        set_patient(patient)
        marked_order_as_completed(patient)
        return patient_ui_manager.load()
    except FileNotFoundError:
        gui.msgbox(ms["error_on_img"].format(patient.photo))
        patient.photo = _load_select_image()
        _open_patient(name)


def _load_select_image():
    img = gui.fileopenbox(ms["select_image"], ms["image_Selection"], default=cf.get("home_file"),
                          filetypes=[["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif", "IMAGE files"]])
    return img
