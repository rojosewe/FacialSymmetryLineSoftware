import easygui as gui
from facial_measures import AxialFace
from utils.Messages import messages as ms
from utils.conf import Conf as cf
from workAreas.state_manager import State, get_patient

from ngui.patient_ui_manager import AxialPatientManager
import os
from utils.exceptions import LeftIncompleteException


def new_patient_fill_info():
    State.initialize()
    patient = get_patient()
    _record_name(patient)
    _record_age(patient)
    _record_gender(patient)
    _record_image(patient)
    saveImagePathAsHome(patient)
    patient.axial = AxialFace()
    AxialPatientManager().load()


def _record_name(patient):
    name = gui.enterbox(ms["enter_info"], ms["patient_info"], patient.name)
    if name is None:
        raise LeftIncompleteException
    patient.name = name


def _record_age(patient):
    age = gui.enterbox(ms["enter_patient_age"], ms["patient_age"], patient.age)
    if age is None:
        raise LeftIncompleteException
    patient.age = age


def _record_gender(patient):
    g = gui.indexbox(ms["gender"], choices=(ms["male"], ms["female"]))
    if g is None:
        raise LeftIncompleteException
    elif g == 0:
        gender = ms["male"]
    else:
        gender = ms["female"]
    patient.gender = gender


def _record_image(patient):
    img = gui.fileopenbox(ms["select_image"], ms["image_Selection"], default=cf.get("home_file"),
                          filetypes = [["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif", "IMAGE files"]])
    if img is None:
        raise LeftIncompleteException
    patient.photo = img


def saveImagePathAsHome(patient):
    file = os.path.abspath(patient.photo)
    cf.set("home_file", file)
    if not cf.isIn("home_dir") or not os.path.isdir(cf.get("home_dir")):
        directory = os.path.abspath(os.path.dirname(file)) + os.sep
        cf.set("home_dir", directory)
