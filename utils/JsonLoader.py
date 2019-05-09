import json
import os
from base64 import b64encode, b64decode
from facial_measures import Patient
from shutil import copyfile
import datetime
from workAreas.state_manager import get_patient

db_json_filepath = os.path.join("files", "patients_db.json")
json_filepath = os.path.join("files", "patients.json")
json_filepath_name = os.path.join("files", "patients")
old_dbs_path = os.path.join("files", "old_dbs")
old_old_dbs_path = "old_dbs"


def patient_to_json(patient):
    patient_info = {
        "key": patient.name + " - " + patient.type,
        "name": patient.name,
        "age": patient.age,
        "type": patient.type,
        "gender": patient.gender,
        "photo": patient.photo,
        "values": patient.values.to_dict()
    }
    return patient_info


def load_patients(filepath=db_json_filepath):
    if os.path.isfile(filepath):
        with open(filepath, "r+") as f:
            return json.load(f)
    else:
        return {}


def get_all_patients_names():
    patient_list = [from_key(key) for key in load_patients().keys()]
    patient_list.sort()
    return patient_list


def get_all_patients():
    return [get_patient_by_name(from_key(key)) for key in load_patients().keys()]


def get_patient_by_name(name):
    patients = load_patients()
    patient_dict = patients[to_key(name)]
    patient = Patient(patient_dict["name"], patient_dict["age"], patient_dict["gender"], patient_dict["photo"],
                      patient_dict["type"])
    try:
        patient.values.from_dict(patient_dict.get("values", None))
    except KeyError:
        pass
    return patient


def save_patient(backup=True):
    patient = get_patient()
    patient_dict = patient_to_json(patient)
    patients = load_patients()
    patients[to_key(patient_dict["key"])] = patient_dict
    if backup and os.path.isfile(db_json_filepath):
        str_date = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
        bkup_file = os.path.join(old_dbs_path, "patients" + "_" + str_date + ".json")
        copyfile(db_json_filepath, bkup_file)
    with open(db_json_filepath, "w+") as f:
        json.dump(patients, f)


def to_key(name):
    return b64encode(bytes(name, 'utf-8')).decode("utf-8")


def from_key(key):
    return b64decode(key).decode("utf-8")
