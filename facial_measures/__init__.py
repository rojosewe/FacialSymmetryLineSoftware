from facial_measures.axial import AxialFace
from facial_measures.frontal import FrontalFace


class Patient:

    FRONTAL_TYPE = "frontal"
    AXIAL_TYPE = "axial"

    def __init__(self, name, age, gender, photo, type="axial", values=None):
        self.name = name
        self.age = age
        self.gender = gender
        self.photo = photo
        self.type = type
        if self.is_axial_patient():
            self.values = values or AxialFace()
        else:
            self.values = values or FrontalFace()

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'photo': self.photo,
            'type': self.type,
            'values': self.values.to_dict()
        }

    def __str__(self):
        return """
        {'name': %s,g
        'age': %s,
        'gender': %s,
        'face': %s,
        'photo': %s,
        'type': %s,
        'values': %s
        }
        """ % (self.name, self.age, self.gender, self.photo, self.type, self.values)

    def complete_dict(self):
        self.calculate_proportions()
        d = self.to_dict()
        d["values"]["angles"] = self.values.angles.to_dict()
        d["values"]["proportions"] = self.values.angles.get_proportions().to_dict()
        for key in list(d["values"]["proportions"].keys()):
            d["values"]["proportions"][key + "_direction"] = "RIGHT" if d["values"]["proportions"][key] > 0 else "LEFT"
        return d

    def calculate_proportions(self):
        self.values.angles.calculate(self.values)

    def is_axial_patient(self):
        return self.type == Patient.AXIAL_TYPE

    def is_frontal_patient(self):
        return self.type == Patient.FRONTAL_TYPE
