from facial_measures import Patient
from facial_measures.frontal_face_order import start_over

def get_patient():
    return State.patient


def set_patient(patient):
    State.patient = patient


class State:

    patient = None

    @classmethod
    def initialize(cls):
        cls.patient = Patient(None, None, 18, None)
        start_over()

    @classmethod
    def clear(cls):
        cls.patient = Patient(None, None, 18, None)
        start_over()