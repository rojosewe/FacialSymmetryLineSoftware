from facial_measures import Patient
from facial_measures.order import AxialOrder, FrontalOrder


def get_patient():
    return State.patient


def set_patient(patient):
    State.patient = patient


class State:

    patient = None

    @classmethod
    def initialize(cls):
        cls.patient = Patient(None, None, 18, None)
        AxialOrder.start_over()
        FrontalOrder.start_over()

    @classmethod
    def clear(cls):
        cls.patient = Patient(None, None, 18, None)
        AxialOrder.start_over()
        FrontalOrder.start_over()
