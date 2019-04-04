import geometry
from geometry import Point, SymmetryPoint, SymmetryAngle, SymmetryDisjointAngle
import utils.colors as cs


class FrontalFace:

    def __init__(self):
        self.middle = None
        self.upper = None
        self.chin = None
        self.nose_center = None
        self.cheekbone = SymmetryPoint()
        self.cheek = SymmetryPoint()
        self.mouth = SymmetryPoint()
        self.nose = SymmetryPoint()
        self.outer_eye = SymmetryPoint()
        self.inner_eye = SymmetryPoint()
        self.malar = SymmetryPoint()
        self.angles = Angles()
        self.proportions = None

    @staticmethod
    def __calculate_malar(outer_eye, mouth, nose, cheekbone):
        malar_eye_line = geometry.Line(outer_eye, mouth)
        malar_nose_line = geometry.Line(nose, cheekbone)
        return geometry.intersects(malar_eye_line, malar_nose_line)

    def calculate_additional(self):
        self.malar.left = FrontalFace.__calculate_malar(self.outer_eye.left, self.mouth.left, self.nose.left,
                                                           self.cheekbone.left)
        self.malar.right = FrontalFace.__calculate_malar(self.outer_eye.right, self.mouth.right, self.nose.right,
                                                           self.cheekbone.right)

    def to_dict(self):
        return {
            "middle": self.middle.get(),
            "upper": self.upper.get(),
            "chin": self.chin.get(),
            "nose_center": self.nose_center.get(),
            "outer_eye_left": self.outer_eye.left.get(),
            "inner_eye_left": self.inner_eye.left.get(),
            "outer_eye_right": self.outer_eye.right.get(),
            "inner_eye_right": self.inner_eye.right.get(),
            "cheekbone_left": self.cheekbone.left.get(),
            "cheekbone_right": self.cheekbone.right.get(),
            "nose_left": self.nose.left.get(),
            "nose_right": self.nose.right.get(),
            "cheek_left": self.cheek.left.get(),
            "cheek_right": self.cheek.left.get(),
            "mouth_left": self.mouth.left.get(),
            "mouth_right": self.mouth.left.get(),
            "malar_left": self.malar.left.get(),
            "malar_right": self.malar.left.get()
        }

    def from_dict(self, d):
        self.middle = Point.from_array(d["middle"])
        self.upper = Point.from_array(d["upper"])
        self.chin = Point.from_array(d["chin"])
        self.nose_center = Point.from_array(d["nose_center"])
        self.cheekbone.left = Point.from_array(d["cheekbone_left"])
        self.cheekbone.right = Point.from_array(d["cheekbone_right"])
        self.cheek.left = Point.from_array(d["cheek_left"])
        self.cheek.right = Point.from_array(d["cheek_right"])
        self.mouth.left = Point.from_array(d["mouth_left"])
        self.mouth.right = Point.from_array(d["mouth_right"])
        self.nose.left = Point.from_array(d["nose_left"])
        self.nose.left = Point.from_array(d["nose_right"])
        self.outer_eye.left = Point.from_array(d["outer_eye_left"])
        self.inner_eye.left = Point.from_array(d["inner_eye_left"])
        self.outer_eye.right = Point.from_array(d["outer_eye_right"])
        self.inner_eye.right = Point.from_array(d["inner_eye_right"])
        self.malar.left = Point.from_array(d["malar_left"])
        self.malar.right = Point.from_array(d["malar_right"])

    def __str__(self):
        d = self.to_dict()
        for key in d:
            d[key] = d[key].get()
        return str(d)

    def get_angles(self):
        self.angles.calculate(self)
        return self.angles

    def get_proportions(self):
        self.proportions = Proportions(self.angles)
        return self.proportions


class Angles:

    def __init__(self):
        self.outer_eye_middle = None
        self.inner_eye_middle = None
        self.cheek_middle = None
        self.nose_middle = None
        self.mouth_middle = None
        self.cheekbone_middle = None
        self.cheek_chin = None
        self.mouth_chin = None
        self.cheekbone_chin = None
        self.malar_nose_center = None
        self.malar_eye = None
        self.malar_internal_cant = None
        self.malar_nose = None
        self.nose_eye_outer = None
        self.nose_eye_inner = None

    def calculate(self, points):
        self.outer_eye_middle = SymmetryAngle(points.outer_eye, points.middle, points.chin)
        self.inner_eye_middle = SymmetryAngle(points.inner_eye, points.middle, points.chin)
        self.cheek_middle = SymmetryAngle(points.cheek, points.middle, points.chin)
        self.nose_middle = SymmetryAngle(points.nose, points.middle, points.chin)
        self.mouth_middle = SymmetryAngle(points.mouth, points.middle, points.chin)
        self.cheekbone_middle = SymmetryAngle(points.cheekbone, points.middle, points.chin)
        self.cheek_chin = SymmetryAngle(points.cheek, points.chin, points.middle)
        self.mouth_chin = SymmetryAngle(points.mouth, points.chin, points.middle)
        self.cheekbone_chin = SymmetryAngle(points.cheekbone, points.chin, points.middle)
        y = geometry.Point(points.nose_center.x, 0)
        self.malar_nose_center = SymmetryAngle(points.malar, points.nose_center, y)
        self.malar_eye = SymmetryDisjointAngle(points.outer_eye.left, points.mouth.left,
                                               points.chin, points.middle,
                                               points.outer_eye.right, points.mouth.right,
                                               points.chin, points.middle)
        self.malar_internal_cant = SymmetryDisjointAngle(points.outer_eye.left, points.mouth.left,
                                                         points.inner_eye.left, points.malar.left,
                                                         points.outer_eye.right, points.mouth.right,
                                                         points.inner_eye.right, points.malar.right)
        self.malar_nose = SymmetryDisjointAngle(points.outer_eye.left, points.mouth.left,
                                                points.nose.left, points.malar.left,
                                                points.outer_eye.right, points.mouth.right,
                                                points.nose.right, points.malar.right)
        self.nose_eye_outer = SymmetryAngle(points.outer_eye, points.nose_center, y)
        self.nose_eye_inner = SymmetryAngle(points.outer_eye, points.nose_center, y)

    def get_lines(self, points, angles, color=cs.BLACK, width= 2):
        upper_lines = []
        lower_lines = []
        vertical_line = geometry.Line(points.middle, points.chin, color=color, w=width)
        upper_lines.append(vertical_line)
        upper_lines += angles.outer_eye_middle.get_lines()
        upper_lines += angles.inner_eye_middle.get_lines()
        upper_lines += angles.nose_middle.get_lines()
        upper_lines += angles.cheekbone_middle.get_lines()
        upper_lines += angles.malar_nose_center.get_lines()
        upper_lines += angles.malar_eye.get_lines()
        upper_lines += angles.malar_internal_cant.get_lines()
        upper_lines += angles.malar_nose.get_lines()
        upper_lines += angles.nose_eye_outer.get_lines()
        upper_lines += angles.nose_eye_inner.get_lines()
        lower_lines += angles.cheek_middle.get_lines()
        lower_lines += angles.mouth_middle.get_lines()
        lower_lines += angles.cheek_chin.get_lines()
        lower_lines += angles.mouth_chin.get_lines()
        lower_lines += angles.cheekbone_chin.get_lines()
        return upper_lines, lower_lines

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
                    "central_point_wall_left": self.central_point_wall.left_angle,
                    "central_point_wall_right": self.central_point_wall.right_angle,
                    "break_point_nose_point": self.break_point_nose_point,
                    "nose_point_wall_left": self.nose_point_wall.left_angle,
                    "nose_point_wall_right": self.nose_point_wall.right_angle,
                    "nose_point_maxilar_left": self.nose_point_maxilar.left_angle,
                    "nose_point_maxilar_right": self.nose_point_maxilar.right_angle
                }


class Proportions:

    def __init__(self, angles):
        self.outer_eye_middle = angles.outer_eye_middle.get_proportion()
        self.inner_eye_middle = angles.inner_eye_middle.get_proportion()
        self.cheek_middle = angles.cheek_middle.get_proportion()
        self.nose_middle = angles.nose_middle.get_proportion()
        self.mouth_middle = angles.mouth_middle.get_proportion()
        self.cheekbone_middle = angles.cheekbone_middle.get_proportion()
        self.cheek_chin = angles.cheek_chin.get_proportion()
        self.mouth_chin = angles.mouth_chin.get_proportion()
        self.cheekbone_chin = angles.cheekbone_chin.get_proportion()
        self.malar_nose_center = angles.malar_nose_center.get_proportion()
        self.malar_eye = angles.malar_eye.get_proportion()
        self.malar_internal_cant = angles.malar_internal_cant.get_proportion()
        self.malar_nose = angles.malar_nose.get_proportion()

    def to_dict(self):
        return {
            "outer_eye_middle": self.outer_eye_middle,
            "inner_eye_middle": self.inner_eye_middle,
            "cheek_middle": self.cheek_middle,
            "nose_middle": self.nose_middle,
            "mouth_middle": self.mouth_middle,
            "cheekbone_middle": self.cheekbone_middle,
            "cheek_chin": self.cheek_chin,
            "mouth_chin": self.mouth_chin,
            "cheekbone_chin": self.cheekbone_chin,
            "malar_nose_center": self.malar_nose_center,
            "malar_eye": self.malar_eye,
            "malar_internal_cant": self.malar_internal_cant,
            "malar_nose": self.malar_nose,
        }