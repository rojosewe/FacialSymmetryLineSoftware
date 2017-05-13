
from email.policy import default
import os
from os.path import expanduser
import sys 

import PatientProcessor
import easygui as gui
from facial_measures import Face
from facial_measures import Patient
from utils import Commands


home = expanduser("~")
pygame = None
patient_name = None

def makeInitialSelection():
    action = gui.indexbox("Choose an option.", choices=("Create new patient", "Open existing one", "Exit"), 
                        default_choice="Create new patient", cancel_choice="Exit")
    if action == 0:
        return Commands.CREATE
    elif action == 1:
        return Commands.OPEN
    elif action == 2:
        sys.exit()
        
def selectImage():
    return gui.fileopenbox("Select the image", "Image selection", default="./images",
                     filetypes=["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"])

def selectPatient():
    msg ="Select the patient"
    title = "Patients"
    choices = ["Vanilla", "Chocolate", "Strawberry", "Rocky Road"]
    choice = gui.choicebox(msg, title, choices)
    if choice == None:
        return Commands.START
    else:
        return openPatient(choice)

def savePatient(patient):
    text = "Hola"
    save = gui.boolbox(text, "Patient measures save?", ["Save", "Cancel"])
    if save:
        gui.msgbox("The patient has been saved", "Saved")
        return Commands.START
    else:
        if gui.boolbox("You said not to save, this will delete the progress for this patient. Are you sure?", 
                    "Cancel?", ["Yes", "No"]):
            return Commands.START
        else:
            return Commands.SAVE
    
def executeGUICommand(command):
    if command == Commands.START:
        command = makeInitialSelection()
    elif command == Commands.CREATE:
        command = fillPatientInfo()
    elif command == Commands.OPEN:
        command = selectPatient()
    elif command == Commands.SAVE:
        command = savePatient(None)
    elif command == Commands.EXIT:
        sys.exit()
    return command

def start(home_path, pygame_x):
    global home, pygame
    home = home_path
    pygame = pygame_x
    command = Commands.START
    while 1:
        command = executeGUICommand(command)

def openPatient(name):
    patient = Patient(name, "images/1.JPG", Face())
    PatientProcessor.load(pygame, patient)

def fillPatientInfo():
    global patient_name
    default = ""
    if patient_name is not None:
        default = patient_name
    name = gui.enterbox("Enter the patient information", "Patient information", default)
    patient_name = name
    if name is None:
        return Commands.START
    image = selectImage()
    if image is None:
        return Commands.CREATE
    patient = Patient(name, image, Face())
    PatientProcessor.load(pygame, patient)
