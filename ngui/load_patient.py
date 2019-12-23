from utils import JsonLoader
from ngui.patient_ui_manager import AxialPatientManager, FrontalPatientManager
import easygui as gui
from utils.Messages import messages as ms
from utils.conf import Conf as cf
from workAreas.state_manager import set_patient
from facial_measures.order import AxialOrder, FrontalOrder


def select_patient():
    msg = ms["select_patient"]
    title = ms["patients"]
    choices = JsonLoader.get_all_patients_names()
    choice = gui.choicebox(msg, title, choices)
    if choice is None:
        return None
    else:
        return _open_patient(choice)


def _open_patient(name):
    patient = JsonLoader.get_patient_by_name(name)
    set_patient(patient)
    _aux_open(patient)


def _aux_open(patient):
    try:
        if patient.is_axial_patient():
            order = AxialOrder
            patient_manager = AxialPatientManager()
        else:
            order = FrontalOrder
            patient_manager = FrontalPatientManager()
        patient_manager.load()
        map = order._return_face_map(patient)
        complete = False
        for pos in order.order.copy():
            point = map[pos]
            if point is not None:
                complete |= patient_manager.workspace.process_point_return_if_completed(point)
                patient_manager.reference.process_click()
        patient_manager.start()
    except FileNotFoundError:
        gui.msgbox(ms["error_on_img"].format(patient.photo))
        patient.photo = _load_select_image()
        _aux_open(patient)


def _load_select_image():
    img = gui.fileopenbox(ms["select_image"], ms["image_Selection"], default=cf.get("home_file"),
                          filetypes=[["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif", "IMAGE files"]])
    return img
