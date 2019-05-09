import xlsxwriter

from utils.Messages import messages as ms
from workAreas.proportions_table import SymmetryAngleProportionValue, DisplacementAngleProportionValue


class ExcelBuilder:

    def __init__(self, patients, file_name='patients.xlsx'):
        self.file_name = file_name
        self.patients = patients
        self.workbook = self.workbook = xlsxwriter.Workbook(self.file_name)
        self.frontal_writer = FrontalWriter(self, self.get_patients_by_type("frontal"))
        self.axial_writer = AxialWriter(self, self.get_patients_by_type("axial"))

    def write_patients(self):
        self.frontal_writer.write_patients()
        self.axial_writer.write_patients()
        self.workbook.close()

    def get_patients_by_type(self, patient_type):
        return list(filter(lambda patient: patient.type == patient_type, self.patients))


class ExcelWriter:

    def __init__(self):
        self.worksheet = None

    @staticmethod
    def _get_symmetry_angle_values(symmetry_angle):
        proportion_value = SymmetryAngleProportionValue(symmetry_angle)
        return (
            proportion_value.get_angle_left(),
            proportion_value.get_angle_right(),
            proportion_value.get_differential(),
            proportion_value.get_orientation()
        )

    @staticmethod
    def _get_displacement_angle_values(displacement_angle):
        proportion_value = DisplacementAngleProportionValue(displacement_angle)
        return (
            proportion_value.get_angle(),
            proportion_value.get_orientation()
        )

    def write_symmetry_angle_label(self, point1, point2, row, col):
        self.worksheet.write(row, col, ("{" + point1 + "} - {" + point2 + "}").format_map(ms))
        self.worksheet.write(row + 1, col, "{right}".format(**ms))
        self.worksheet.write(row + 1, col + 1, "{left}".format(**ms))
        self.worksheet.write(row + 1, col + 2, "{differential}".format(**ms))
        self.worksheet.write(row + 1, col + 3, "{orientation}".format(**ms))
        return row + 1, col + 3

    def write_displacement_angle_label(self, point1, point2, row, col):
        self.worksheet.write(row, col, ("{" + point1 + "} - {" + point2 + "}").format_map(ms))
        self.worksheet.write(row + 1, col, "{angle}".format(**ms))
        self.worksheet.write(row + 1, col + 1, "{deviation}".format(**ms))
        return row + 1, col + 1

    def write_patients(self):
        pass

    def write_patients(self):
        start_row, _ = self.write_col_names()
        start_row = 2
        for patient in self.patients:
            patient.calculate_proportions()
            row_values = self._write_type_column_values(patient)
            start_col = 0
            for row_value in row_values:
                self.worksheet.write(start_row, start_col, row_value)
                start_col += 1
            start_row += 1


class AxialWriter(ExcelWriter):

    def __init__(self, builder, patients):
        self.worksheet = builder.workbook.add_worksheet(name="Axial")
        self.patients = patients

    def _write_type_column_values(self, patient):
        row_values = [patient.name, patient.gender, patient.age, patient.photo]
        row_values += self._get_symmetry_angle_values(patient.values.angles.central_point_wall)
        row_values += self._get_symmetry_angle_values(patient.values.angles.nose_point_wall)
        row_values += self._get_symmetry_angle_values(patient.values.angles.nose_point_maxilar)
        row_values += self._get_displacement_angle_values(patient.values.angles.break_point_nose_point)
        return row_values

    def write_col_names(self):
        self.worksheet.write(1, 0, "{name}".format(**ms))
        self.worksheet.write(1, 1, "{gender}".format(**ms))
        self.worksheet.write(1, 2, "{age}".format(**ms))
        self.worksheet.write(1, 3, "{image}".format(**ms))
        start_row = 0
        start_col = 4
        _, start_col = self.write_symmetry_angle_label("walls", "central_point", start_row, start_col)
        _, start_col = self.write_symmetry_angle_label("walls", "nose_point", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("maxilars", "nose_point", start_row, start_col + 1)
        _, start_col = self.write_displacement_angle_label("break_point", "nose_point", start_row, start_col + 1)
        return start_row, start_col


class FrontalWriter(ExcelWriter):

    def __init__(self, builder, patients):
        self.worksheet = builder.workbook.add_worksheet(name="Frontal")
        self.patients = patients

    def _write_type_column_values(self, patient):
        row_values = [patient.name, patient.gender, patient.age, patient.photo]
        row_values += self._get_symmetry_angle_values(patient.values.angles.outer_eye_middle)
        row_values += self._get_symmetry_angle_values(patient.values.angles.inner_eye_middle)
        row_values += self._get_symmetry_angle_values(patient.values.angles.cheek_middle)
        row_values += self._get_symmetry_angle_values(patient.values.angles.nose_middle)
        row_values += self._get_symmetry_angle_values(patient.values.angles.mouth_middle)
        row_values += self._get_symmetry_angle_values(patient.values.angles.cheekbone_middle)
        row_values += self._get_symmetry_angle_values(patient.values.angles.cheek_chin)
        row_values += self._get_symmetry_angle_values(patient.values.angles.mouth_chin)
        row_values += self._get_symmetry_angle_values(patient.values.angles.cheekbone_chin)
        row_values += self._get_symmetry_angle_values(patient.values.angles.nose_eye_outer)
        row_values += self._get_symmetry_angle_values(patient.values.angles.nose_eye_inner)
        row_values += self._get_symmetry_angle_values(patient.values.angles.malar_nose)
        row_values += self._get_symmetry_angle_values(patient.values.angles.malar_vertical)
        row_values += self._get_symmetry_angle_values(patient.values.angles.malar_internal_cant)
        return row_values

    def write_col_names(self):
        self.worksheet.write(1, 0, "{name}".format(**ms))
        self.worksheet.write(1, 1, "{gender}".format(**ms))
        self.worksheet.write(1, 2, "{age}".format(**ms))
        self.worksheet.write(1, 3, "{image}".format(**ms))
        start_row = 0
        start_col = 4
        _, start_col = self.write_symmetry_angle_label("eye_outer", "middle", start_row, start_col)
        _, start_col = self.write_symmetry_angle_label("eye_inner", "middle", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("cheek", "middle", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("nose", "middle", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("mouth", "middle", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("cheekbone", "middle", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("cheek", "chin", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("mouth", "chin", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("cheekbone", "chin", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("nose_point", "eye_outer", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("nose_point", "eye_inner", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("malar", "nose", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("malar", "vertical", start_row, start_col + 1)
        _, start_col = self.write_symmetry_angle_label("malar", "eye_inner", start_row, start_col + 1)
        return start_row, start_col
