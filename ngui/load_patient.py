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


def marked_order_as_completed(patient):
    face = patient.face
    add_to_processed(HORIZONTAL_LINE)
    if face.upper is not None:
        add_to_processed(TOP_HEAD)
    if face.middle  is not None:
        add_to_processed(FOREHEAD)
    if face.chin is not None:
        add_to_processed(CHIN)
    if face.cheekboneL is not None:
        add_to_processed(CHEEKBONE_LEFT)
    if face.cheekboneR is not None:
        add_to_processed(CHEEKBONE_RIGHT)
    if face.cheekL is not None:
        add_to_processed(CHEEK_LEFT)
    if face.cheekR is not None:
        add_to_processed(CHEEK_RIGHT)
    if face.mouthL is not None:
        add_to_processed(MOUTH_LEFT)
    if face.mouthR is not None:
        add_to_processed(MOUTH_RIGHT)
    if face.noseL is not None:
        add_to_processed(NOSE_LEFT)
    if face.noseC is not None:
        add_to_processed(NOSE_CENTER)
    if face.noseR is not None:
        add_to_processed(NOSE_RIGHT)
    if face.outer_eyeL is not None:
        add_to_processed(EYE_OUTER_LEFT)
    if face.inner_eyeL is not None:
        add_to_processed(EYE_INNER_LEFT)
    if face.outer_eyeR is not None:
        add_to_processed(EYE_OUTER_RIGHT)
    if face.inner_eyeR is not None:
        add_to_processed(EYE_INNER_RIGHT)


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
