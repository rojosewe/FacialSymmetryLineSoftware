import geometry
from geometry import Point, SymmetryPoint, SymmetryAngle, DisplacementAngle
from utils import colors as cs


class AxialFace:

    def __init__(self):
        self.central_point = None
        self.break_point = None
        self.point_nose = None
        self.wall = SymmetryPoint()
        self.maxilar = SymmetryPoint()
        self.angles = Angles()

    def to_dict(self):
        return {
            "central_point": self.central_point.get(),
            "break_point": self.break_point.get(),
            "point_nose": self.point_nose.get(),
            "wall_left": self.wall.get_left(),
            "wall_right": self.wall.get_right(),
            "maxilar_left": self.maxilar.get_left(),
            "maxilar_right": self.maxilar.get_right()
        }

    def calculate_additional(self):
        pass

    def from_dict(self, d):
        self.central_point = Point.from_array(d["central_point"])
        self.break_point = Point.from_array(d["break_point"])
        self.point_nose = Point.from_array(d["point_nose"])
        self.wall.left = Point.from_array(d["wall_left"])
        self.wall.right = Point.from_array(d["wall_right"])
        self.maxilar.left = Point.from_array(d["maxilar_left"])
        self.maxilar.right = Point.from_array(d["maxilar_right"])

    def get_angles(self):
        self.angles.calculate(self)
        return self.angles

    def get_proportions(self):
        return Proportions(self.get_angles())

    def __str__(self):
        d = self.to_dict()
        for key in d:
            d[key] = d[key].get()
        return str(d)


class Angles:

    def __init__(self):
        self.central_point_wall = None
        self.break_point_nose_point = None
        self.nose_point_wall = None
        self.nose_point_maxilar = None

    def calculate(self, face):
        top = Point(face.central_point.x, 0)
        vertical_line = geometry.Line(face.central_point, top)
        self.break_point_nose_point = DisplacementAngle(face.break_point, face.point_nose, vertical_line)
        self.central_point_wall = SymmetryAngle(face.wall, face.central_point, top)
        self.nose_point_wall = SymmetryAngle(face.wall, face.point_nose, face.break_point)
        self.nose_point_maxilar = SymmetryAngle(face.maxilar, face.point_nose, face.break_point)

    def get_lines(self, face, color=cs.BLACK, width=2):
        lines = []
        top = Point(face.central_point.x, 0)
        vertical_line = geometry.Line(face.central_point, top, color=cs.RED, w=width, dash=(4, 4))
        lines.append(vertical_line)
        break_line = geometry.Line(face.break_point, face.point_nose, color=cs.ORANGE, w=width)
        lines.append(break_line)
        lines += self.central_point_wall.get_lines(cs.BLUE, width)
        lines += self.nose_point_wall.get_lines(cs.GREEN, width)
        lines += self.nose_point_maxilar.get_lines(cs.YELLOW, width)
        return lines

    def __str__(self):
        return str(self.toDict())

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
        self.central_point_wall = angles.central_point_wall.get_proportion()
        self.nose_point_wall = angles.nose_point_wall.get_proportion()
        self.nose_point_maxilar = angles.nose_point_maxilar.get_proportion()
        self.break_point_nose_point = angles.break_point_nose_point.get_displacement_x()

    def to_dict(self):
        return {
            "central_point_wall": self.central_point_wall,
            "nose_point_wall": self.nose_point_wall,
            "break_point_nose_point": self.break_point_nose_point,
            "nose_point_maxilar": self.nose_point_maxilar
        }