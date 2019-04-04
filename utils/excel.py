'''
Created on May 14, 2017

@author: root
'''

import xlsxwriter


class ExcelWriter:

    def patients_to_excel(self, patients, file):
        workbook = xlsxwriter.Workbook(file)
        worksheet = workbook.add_worksheet()
        self.write_row(0, worksheet, self.headers, self.human_headers)
        for i, p in enumerate(patients):
            patient_values = self.extract_patient_flat_dict(p)
            self.write_row(i + 1, worksheet, self.headers, patient_values)
        workbook.close()

    def write_row(self, row, worksheet, headers, row_values):
        for i, h in enumerate(headers):
            print(i, h, row_values[h])
            value = row_values[h]
            worksheet.write(row, i, str(value))

    def extract_patient_flat_dict(self, p):
        base = p.complete_dict()
        csv_dict = {}
        for header in self.headers:
            csv_dict[header] = self.get_value(base, header)
        return csv_dict

    def get_value(self, d, header):
        final_value = None
        for key in header.split("."):
            final_value = d[key]
            d = d[key]
        return final_value


class AxialExcelWriter(ExcelWriter):

    def __init__(self):
        self.headers = ['name', 'age', 'gender', 'values.central_point', 'values.break_point', 'values.point_nose',
                        'values.wall_left', 'values.wall_right', 'values.maxilar_left', 'values.maxilar_right',
                        'values.angles.break_point_nose_point',
                        'values.angles.nose_point_wall_left',
                        'values.angles.nose_point_wall_right',
                        'values.angles.nose_point_maxilar_left',
                        'values.angles.nose_point_maxilar_right',
                        'values.proportions.central_point_wall',
                        'values.proportions.central_point_wall_direction',
                        'values.proportions.nose_point_wall', 'values.proportions.nose_point_wall_direction',
                        'values.proportions.break_point_nose_point',
                        'values.proportions.break_point_nose_point_direction']
        self.human_headers = {
            'name': "Nombre",
            'age': "Edad",
            'gender': "Genero",
            'values.central_point': "punto septal posterior [x,y]",
            'values.break_point': "punto de quiebre [x,y]",
            'values.point_nose': "punta nasal [x,y]",
            'values.wall_left': "punto ducto naso-lagrimal izquierdo [x,y]",
            'values.wall_right': "punto ducto naso-lagrimal derecho [x,y]",
            'values.maxilar_left': "punto maxilar izquierdo [x,y]",
            'values.maxilar_right': "punto maxilar derecho [x,y]",
            'values.angles.central_point_wall_left': "angulo punto septal posterior - ducto naso-lagrimal izquierdo",
            'values.angles.central_point_wall_right': "angulo punto septal posterior - ducto naso-lagrimal derecho",
            'values.angles.nose_point_wall_left': "angulo punta nasal - ducto naso-lagrimal izquierdo",
            'values.angles.nose_point_wall_right': "angulo punta nasal - ducto naso-lagrimal derecho",
            'values.angles.nose_point_maxilar_left': "angulo punta nasal - maxilar izquierdo",
            'values.angles.nose_point_maxilar_right': "angulo punta nasal -  maxilar derecho",
            'values.proportions.central_point_wall': "proporcion angulo punto septal posterior - ducto naso-lagrimal I/D",
            'values.proportions.central_point_wall_direction': "proporcion angulo punto septal posterior - ducto naso-lagrimal direccion",
            'values.proportions.nose_point_wall': "proporcion angulo punta nasal - ducto naso-lagrimal I/D",
            'values.proportions.nose_point_wall_direction': "proporcion angulo punta nasal - ducto naso-lagrimal direccion",
            'values.proportions.nose_maxilar_wall': "proporcion angulo punta nasal - punto maxilar I/D",
            'values.proportions.nose_point_maxilar_direction': "proporcion angulo punta nasal - punto maxilar direccion",
            'values.angles.break_point_nose_point': "angulo de punto de quiebre - punta nasal",
            'values.proportions.break_point_nose_point': "Direccion de desviacion angulo punto de quiebre - punta nasal: (1: Derecha, -1: Izquierda)",
            'values.proportions.break_point_nose_point_direction': "Direccion de desviacion angulo punto de quiebre - punta nasal"
        }


class AxialExcelWriter(ExcelWriter):

    def __init__(self):
        self.headers = ['name', 'age', 'gender', 'type', 'values.central_point',
                        'values.break_point', 'values.point_nose',
                        'values.wall_left', 'values.wall_right', 'values.maxilar_left', 'values.maxilar_right',
                        'values.angles.break_point_nose_point',
                        'values.angles.nose_point_wall_left',
                        'values.angles.nose_point_wall_right',
                        'values.angles.nose_point_maxilar_left',
                        'values.angles.nose_point_maxilar_right',
                        'values.proportions.central_point_wall',
                        'values.proportions.central_point_wall_direction',
                        'values.proportions.nose_point_wall', 'values.proportions.nose_point_wall_direction',
                        'values.proportions.break_point_nose_point',
                        'values.proportions.break_point_nose_point_direction']
        self.human_headers = {
            'name': "Nombre",
            'age': "Edad",
            'gender': "Genero",
            'type': "Tipo",
            'values.central_point': "punto septal posterior [x,y]",
            'values.break_point': "punto de quiebre [x,y]",
            'values.point_nose': "punta nasal [x,y]",
            'values.wall_left': "punto ducto naso-lagrimal izquierdo [x,y]",
            'values.wall_right': "punto ducto naso-lagrimal derecho [x,y]",
            'values.maxilar_left': "punto maxilar izquierdo [x,y]",
            'values.maxilar_right': "punto maxilar derecho [x,y]",
            'values.angles.central_point_wall_left': "angulo punto septal posterior - ducto naso-lagrimal izquierdo",
            'values.angles.central_point_wall_right': "angulo punto septal posterior - ducto naso-lagrimal derecho",
            'values.angles.nose_point_wall_left': "angulo punta nasal - ducto naso-lagrimal izquierdo",
            'values.angles.nose_point_wall_right': "angulo punta nasal - ducto naso-lagrimal derecho",
            'values.angles.nose_point_maxilar_left': "angulo punta nasal - maxilar izquierdo",
            'values.angles.nose_point_maxilar_right': "angulo punta nasal -  maxilar derecho",
            'values.proportions.central_point_wall': "proporcion angulo punto septal posterior - ducto naso-lagrimal I/D",
            'values.proportions.central_point_wall_direction': "proporcion angulo punto septal posterior - ducto naso-lagrimal direccion",
            'values.proportions.nose_point_wall': "proporcion angulo punta nasal - ducto naso-lagrimal I/D",
            'values.proportions.nose_point_wall_direction': "proporcion angulo punta nasal - ducto naso-lagrimal direccion",
            'values.proportions.nose_maxilar_wall': "proporcion angulo punta nasal - punto maxilar I/D",
            'values.proportions.nose_point_maxilar_direction': "proporcion angulo punta nasal - punto maxilar direccion",
            'values.angles.break_point_nose_point': "angulo de punto de quiebre - punta nasal",
            'values.proportions.break_point_nose_point': "Direccion de desviacion angulo punto de quiebre - punta nasal: (1: Derecha, -1: Izquierda)",
            'values.proportions.break_point_nose_point_direction': "Direccion de desviacion angulo punto de quiebre - punta nasal"
        }
