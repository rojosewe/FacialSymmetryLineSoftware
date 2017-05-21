
from email.policy import default
import os
from os.path import expanduser
import sys 
import pygame
import PatientProcessor
import easygui as gui
from facial_measures import Face
from facial_measures import Patient
from utils import Commands, Loader, CSV

home = expanduser("~")
patient_name = None

def makeInitialSelection():
    action = gui.indexbox("Choose an option.", choices=("Create new patient", "Open existing one", "Export the database to csv", "Exit"), 
                        default_choice="Create new patient", cancel_choice="Exit")
    if action == 0:
        return Commands.CREATE
    elif action == 1:
        return Commands.OPEN
    elif action == 2:
        return Commands.EXPORT
    elif action == 3:
        sys.exit()
        
def selectImage():
    return gui.fileopenbox("Select the image", "Image selection", default="./images",
                     filetypes=["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp"])

def selectPatient():
    msg ="Select the patient"
    title = "Patients"
    choices = Loader.getAllPatientsNames()
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
        
def exportDB():
    location = gui.filesavebox(msg="Choose location to save", title="Save file", default='db.csv', filetypes=["*.csv"])
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

def start(home_path):
    global home
    home = home_path
    command = Commands.START
    while 1:
        command = executeGUICommand(command)

def openPatient(name):
    patient = Loader.openPatient(name)
    return PatientProcessor.load(pygame, patient, complete=True, loaded=True)

def fillPatientInfo():
    global patient_name
    default = ""
    if patient_name is not None:
        default = patient_name
    name = gui.enterbox("Enter the patient information", "Patient information", default)
    if name is None:
        return Commands.START
    patient_name = name
    patient_age = gui.enterbox("Enter the patient age", "Patient age", 18)
    if patient_age is None:
        return Commands.START
    patient_age = int(patient_age)
    patient_gender = "Male" if gui.indexbox("Gender.", choices=("Male", "Female")) == 0 else "Female"
    if name is None:
        return Commands.START
    image = selectImage()
    if image is None:
        return Commands.CREATE
    patient = Patient(name, patient_age, patient_gender, image, Face())
    return PatientProcessor.load(pygame, patient)
