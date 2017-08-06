
from email.policy import default
import json
import os
import sys 

import PatientProcessor
import easygui as gui
from facial_measures import Face
from facial_measures import Patient
import tkinter as tk
from utils import Commands, Loader, CSV
from utils.Messages import messages as ms
from utils.conf import Conf as cf

patient_name = None

def makeInitialSelection():
    action = gui.indexbox(ms["choose_an_option"], choices=(ms["create_new_patient"], 
                                                           ms["open_patient"],
                                                           ms["export_to_csv"],
                                                           ms["exit"]), 
                        default_choice=ms["create_new_patient"], cancel_choice=ms["exit"])
    if action == 0:
        return Commands.CREATE
    elif action == 1:
        return Commands.OPEN
    elif action == 2:
        return Commands.EXPORT
    else:
        sys.exit()
        
        
def selectImage():
    img = gui.fileopenbox(ms["select_image"], ms["image_Selection"], default=cf.get("home_file"),
                     filetypes= [["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif", "IMAGE files"]])
    return img

def saveFilePathAsHome(file):
    file = os.path.abspath(file)
    cf.set("home_file", file)
    if not cf.isIn("home_dir") or not os.path.isdir(cf.get("home_dir")):
        directory = os.path.abspath(os.path.dirname(file)) + os.sep
        cf.set("home_dir", directory)


def selectPatient():
    msg =ms["select_patient"]
    title = ms["patients"]
    choices = Loader.getAllPatientsNames()
    choice = gui.choicebox(msg, title, choices)
    if choice == None:
        return Commands.START
    else:
        return openPatient(choice)

def savePatient(patient):
    save = gui.boolbox(ms["save_measures"], ms["save_measures"], [ms["save"], ms["cancel"]])
    if save:
        gui.msgbox(ms["patient_saved"], ms["saved"])
        return Commands.START
    else:
        if gui.boolbox(ms["not_save_msg"], ms["cancel_q"], [ms["yes"], ms["no"]]):
            return Commands.START
        else:
            return Commands.SAVE
        
def exportDB():
    location = gui.filesavebox(msg=ms["choose_save_location"], title=ms["save"], 
                               default=cf.get("home_dir") + os.sep + 'db.csv', filetypes=["*.csv"])
    cf.set("home_dir", os.path.abspath(os.path.dirname(location)))
    if location is None:
        return Commands.START
    if not location.endswith(".csv"):
        location += ".csv"
    patients = Loader.getAllPatients()
    CSV.patientsToCSV(patients, location)
    return Commands.START
    
def executeGUICommand(command):
    if command == Commands.START:
        command = makeInitialSelection()
    elif command == Commands.CREATE:
        command = fillPatientInfo()
    elif command == Commands.OPEN:
        command = selectPatient()
    elif command == Commands.SAVE:
        command = savePatient(None)
    elif command == Commands.EXPORT:
        command = exportDB()
    elif command == Commands.EXIT:
        sys.exit()
    return command

def start(home_path=None):
    command = Commands.START
    while 1:
        command = executeGUICommand(command)

def openPatient(name):
    patient = Loader.openPatient(name)
    return loadPatient(patient, True, True)

def loadPatient(patient, complete, loaded):
    retry = True
    while retry:
        try:
            return PatientProcessor.load(patient, complete, loaded)
        except FileNotFoundError:
            gui.msgbox(ms["error_on_img"].format(patient.photo))
            retry = True
            patient.photo = selectImage()
        
def fillPatientInfo():
    global patient_name
    default = ""
    if patient_name is not None:
        default = patient_name
    name = gui.enterbox(ms["enter_info"], ms["patient_info"], default)
    if name is None:
        return Commands.START
    patient_name = name
    patient_age = gui.enterbox(ms["enter_patient_age"], ms["patient_age"], 18)
    if patient_age is None:
        return Commands.START
    patient_age = int(patient_age)
    patient_gender = ms["male"] if gui.indexbox(ms["gender"], choices=(ms["male"], ms["female"])) == 0 else ms["female"]
    if name is None:
        return Commands.START
    image = selectImage()
    saveFilePathAsHome(image)
    if image is None:
        return Commands.CREATE
    patient = Patient(name, patient_age, patient_gender, image, Face())
    return loadPatient(patient, False, False)
