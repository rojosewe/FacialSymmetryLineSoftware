'''
Created on May 14, 2017

@author: root
'''

import csv

headers = ['name', 'age', 'gender', 'axial.central_point', 'axial.break_point', 'axial.point_nose',
           'axial.wall_left', 'axial.wall_right', 'axial.angles.central_point_wall_left',
           'axial.angles.central_point_wall_right', 'axial.angles.break_point_nose_point',
           'axial.angles.nose_point_wall_left',
           'axial.angles.nose_point_wall_right', 'axial.proportions.central_point_wall',
           'axial.proportions.central_point_wall_direction',
           'axial.proportions.nose_point_wall', 'axial.proportions.nose_point_wall_direction',
           'axial.proportions.break_point_nose_point', 'axial.proportions.break_point_nose_point_direction']

human_headers = {
    'name': "Nombre",
    'age': "Edad",
    'gender': "Genero",
    'axial.central_point': "punto septal posterior [x,y]",
    'axial.break_point': "punto de quiebre [x,y]",
    'axial.point_nose': "punta nasal [x,y]",
    'axial.wall_left': "punto ducto naso-lagrimal izquierdo [x,y]",
    'axial.wall_right': "punto ducto naso-lagrimal derecho [x,y]",
    'axial.angles.central_point_wall_left': "angulo punto septal posterior - ducto naso-lagrimal izquierdo",
    'axial.angles.central_point_wall_right': "angulo punto septal posterior - ducto naso-lagrimal derecho",
    'axial.angles.nose_point_wall_left': "angulo punta nasal - ducto naso-lagrimal izquierdo",
    'axial.angles.nose_point_wall_right': "angulo punta nasal - ducto naso-lagrimal derecho",
    'axial.proportions.central_point_wall': "proporcion angulo punto septal posterior - ducto naso-lagrimal I/D",
    'axial.proportions.central_point_wall_direction': "proporcion angulo punto septal posterior - ducto naso-lagrimal direccion",
    'axial.proportions.nose_point_wall': "proporcion angulo punta nasal - ducto naso-lagrimal I/D",
    'axial.proportions.nose_point_wall_direction': "proporcion angulo punta nasal - ducto naso-lagrimal direccion",
    'axial.angles.break_point_nose_point': "angulo de punto de quiebre - punta nasal",
    'axial.proportions.break_point_nose_point': "Direccion de desviacion angulo punto de quiebre - punta nasal: (1: Derecha, -1: Izquierda)",
    'axial.proportions.break_point_nose_point_direction': "Direccion de desviacion angulo punto de quiebre - punta nasal"
}


def patientsToCSV(patients, file):
    with open(file, mode='w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore')
        writer.writerow(human_headers)
        for p in patients:
            csv_dict = extract_patient_flat_dict(p)
            writer.writerow(csv_dict)


def extract_patient_flat_dict(p):
    base = p.complete_dict()
    csv_dict = {}
    for header in headers:
        csv_dict[header] = get_value(base, header)
    return csv_dict


def get_value(d, header):
    final_value = None
    for key in header.split("."):
        final_value = d[key]
        d = d[key]
    return d
