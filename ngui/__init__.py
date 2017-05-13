
import easygui as gui
import sys 
from utils import commands
from facial_measures import Patient
from facial_measures import Face
from os.path import expanduser
import os
import PatientProcessor
from email.policy import default

home = expanduser("~")
pygame = None
patient_name = None

def makeInitialSelection():
    action = gui.indexbox("Choose an option.", choices=("Create new patient", "Open existing one", "Exit"), 
                        default_choice="Create new patient", cancel_choice="Exit")
    if action == 0:
        return commands.CREATE
    elif action == 1:
        return commands.OPEN
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
        return commands.START
    else:
        return openPatient(choice)

def savePatient(patient):
    text = "Hola"
    save = gui.boolbox(text, "Patient measures save?", ["Save", "Cancel"])
    if save:
        gui.msgbox("The patient has been saved", "Saved")
        return commands.START
    else:
        if gui.boolbox("You said not to save, this will delete the progress for this patient. Are you sure?", 
                    "Cancel?", ["Yes", "No"]):
            return commands.START
        else:
            return commands.SAVE
    
def executeGUICommand(command):
    if command == commands.START:
        command = makeInitialSelection()
    elif command == commands.CREATE:
        command = fillPatientInfo()
    elif command == commands.OPEN:
        command = selectPatient()
    elif command == commands.SAVE:
        command = savePatient(None)
    elif command == commands.EXIT:
        sys.exit()
    return command

def start(home_path, pygame_x):
    global home, pygame
    home = home_path
    pygame = pygame_x
    command = commands.START
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
        return commands.START
    image = selectImage()
    if image is None:
        return commands.CREATE
    patient = Patient(name, image, Face())
    PatientProcessor.load(pygame, patient)
