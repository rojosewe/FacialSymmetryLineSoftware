import json
from utils import Loader
import os
from base64 import b64encode, b64decode
from facial_measures import Patient
from shutil import copyfile, move
import datetime

json_filepath = "files/patients.json"
json_filepath_name = "files/patients"

def migrateDB(dbpath="./files/patients.db"):
    if not os.path.exists("old_dbs"):
        os.makedirs("old_dbs")
    if os.path.isfile(dbpath):
        for patient in Loader.getAllPatients():
            savePatient(patient, False)
        if os.path.isfile(dbpath):
            move(dbpath, "old_dbs/patients_old.db")


def patientToJson(patient):
    patientinfo = {
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "photo": patient.photo,
        "face": patient.face.toDict()
    }
    return patientinfo

def loadPatients(filepath=json_filepath):
    if os.path.isfile(filepath):
        with open(filepath, "r+") as f:
            return json.load(f)
    else:
        return {}

def getAllPatientsNames():
    return [fromkey(key) for key in loadPatients().keys()]

def getAllPatients():
    return [getPatient(fromkey(key)) for key in loadPatients().keys()]


def getPatient(name):
    patients = loadPatients()
    patient_dict = patients[tokey(name)]
    patient = Patient(patient_dict["name"], patient_dict["age"], patient_dict["gender"], patient_dict["photo"])
    patient.face.fromDict(patient_dict["face"])
    patient.measurements.calculate(patient.face)
    patient.angles.calculate(patient.face)
    patient.face.calculate_additional()
    patient.proportions.calculate(patient.measurements, patient.angles)
    return patient

def savePatient(patient, backup=True):
    patient_dict = patientToJson(patient)
    patients = loadPatients()
    patients[tokey(patient_dict["name"])] = patient_dict
    if backup and os.path.isfile(json_filepath):
        copyfile(json_filepath, "old_dbs/patients" + "_" + str(datetime.datetime.now()) + ".json")
    with open(json_filepath, "w+") as f:
        json.dump(patients, f)

def tokey(name):
    return b64encode(bytes(name, 'utf-8')).decode("utf-8")

def fromkey(key):
    return b64decode(key).decode("utf-8")
