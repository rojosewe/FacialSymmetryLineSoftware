import json
from utils import Loader
import os
from base64 import b64encode, b64decode
from facial_measures import Patient
from shutil import copyfile, move
import datetime
from workAreas.state_manager import get_patient

axial_json_filepath = os.path.join("files", "axial.json")
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
        "axial": patient.axial.toDict()
    }
    return patientinfo


def loadPatients(filepath=axial_json_filepath):
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
    try:
        patient.axial.fromDict(patient_dict.get("axial", None))
        patient.axial.angles.calculate(patient.axial)
        patient.axial.proportions.calculate(patient.axial, patient.axial.angles)
    except KeyError:
        pass
    return patient


def savePatient(backup=True):
    patient = get_patient()
    patient_dict = patientToJson(patient)
    patients = loadPatients()
    patients[tokey(patient_dict["name"])] = patient_dict
    if backup and os.path.isfile(axial_json_filepath):
        str_date = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
        bkup_file = os.path.join(old_dbs_path, "axial_patients" + "_" + str_date + ".json")
        copyfile(axial_json_filepath, bkup_file)
    with open(axial_json_filepath, "w+") as f:
        json.dump(patients, f)

def tokey(name):
    return b64encode(bytes(name, 'utf-8')).decode("utf-8")

def fromkey(key):
    return b64decode(key).decode("utf-8")
