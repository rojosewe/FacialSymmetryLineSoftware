import json
from utils import Loader
import os
from base64 import b64encode, b64decode
from facial_measures import Patient
from shutil import copyfile, move
import datetime
from workAreas.state_manager import get_patient

json_filepath = os.path.join("files", "patients.json")
json_filepath_name = os.path.join("files", "patients")
old_dbs_path = os.path.join("files", "old_dbs")
old_old_dbs_path = "old_dbs"


def migrateDB():
    dbpath = os.path.join("files", "patients.db")
    if os.path.exists(old_old_dbs_path):
        move(old_old_dbs_path, old_dbs_path)
    if not os.path.exists(old_dbs_path):
        os.makedirs(old_dbs_path)
    if os.path.isfile(dbpath):
        for patient in Loader.getAllPatients():
            savePatient(patient, False)
        if os.path.isfile(dbpath):
            move(dbpath, os.path.join(old_dbs_path, "patients_old.db"))


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


def savePatient(backup=True):
    patient = get_patient()
    patient_dict = patientToJson(patient)
    patients = loadPatients()
    patients[tokey(patient_dict["name"])] = patient_dict
    if backup and os.path.isfile(json_filepath):
        bkup_file = os.path.join(old_dbs_path, "patients" + "_" + str(datetime.datetime.now()) + ".json")
        copyfile(json_filepath, bkup_file)
    with open(json_filepath, "w+") as f:
        json.dump(patients, f)

def tokey(name):
    return b64encode(bytes(name, 'utf-8')).decode("utf-8")

def fromkey(key):
    return b64decode(key).decode("utf-8")
