from geometry import distance
import geometry
from utils import colors as cs
from geometry import Point


class AxialFace:
    
    def __init__(self):
        self.central_point = None
        self.break_point = None
        self.point_nose = None
        self.wall_left = None
        self.wall_right = None
        self.angles = self.Angles()
        self.proportions = self.Proportions()

    def toDict(self):
        return {
            "central_point": self.central_point.get(),
            "break_point": self.break_point.get(),
            "point_nose": self.point_nose.get(),
            "wall_left": self.wall_left.get(),
            "wall_right": self.wall_right.get(),
        }
        
    def fromDict(self, d):
        self.central_point = Point.from_array(d["central_point"])
        self.break_point = Point.from_array(d["break_point"])
        self.point_nose = Point.from_array(d["point_nose"])
        self.wall_left = Point.from_array(d["wall_left"])
        self.wall_right = Point.from_array(d["wall_right"])

    def get_angles(self):
        self.angles.calculate(self)
        return self.angles

    def get_proportions(self):
        self.proportions.calculate(self)
        return self.proportions
        
    def __str__(self):
        d = self.toDict()
        for key in d:
            d[key] = d[key].get()
        return str(d)

    class Angles:

        def __init__(self):
            self.central_point_wall_left = None
            self.central_point_wall_right = None
            self.break_point_nose_point = None
            self.nose_point_wall_left = None
            self.nose_point_wall_right = None
         
        def calculate(self, f):
            top = Point(f.central_point.x, 0)
            vertical_line = geometry.Line(f.central_point, top)
            break_line = geometry.Line(f.break_point, f.point_nose)
            line = geometry.Line(f.central_point, f.wall_left)
            self.central_point_wall_left = geometry.angle(vertical_line, line)
            line = geometry.Line(f.central_point, f.wall_right)
            self.central_point_wall_right = geometry.angle(vertical_line, line)
            self.break_point_nose_point = geometry.angle(vertical_line, break_line)
            line = geometry.Line(f.wall_left, f.point_nose)
            self.nose_point_wall_left = geometry.angle(break_line, line)
            line = geometry.Line(f.wall_right, f.point_nose)
            self.nose_point_wall_right = geometry.angle(break_line, line)
        
        def getLines(self, f, color=cs.BLACK, width=2):
            lines = []
            top = Point(f.central_point.x, 0)
            vertical_line = geometry.Line(f.central_point, top, color=cs.RED, w=width, dash=(4,4))
            lines.append(vertical_line)
            break_line = geometry.Line(f.break_point, f.point_nose, color=cs.ORANGE, w=width)
            lines.append(break_line)
            line = geometry.Line(f.central_point, f.wall_left, color=cs.BLUE, w=width)
            lines.append(line)
            line = geometry.Line(f.central_point, f.wall_right, color=cs.BLUE, w=width)
            lines.append(line)
            line = geometry.Line(f.point_nose, f.wall_left, color=cs.GREEN, w=width)
            lines.append(line)
            line = geometry.Line(f.point_nose, f.wall_right, color=cs.GREEN, w=width)
            lines.append(line)
            return lines

        def __str__(self):
            return str(self.toDict())
    
    class Proportions:

        def __init__(self):
            self.central_point_wall = None
            self.nose_point_wall = None
            self.break_point_nose_point = None

        def calculate(self, axial, angles):
            self.central_point_wall = angles.central_point_wall_left / angles.central_point_wall_right
            self.nose_point_wall = angles.nose_point_wall_left / angles.nose_point_wall_right
            self.break_point_nose_point = -1 if axial.point_nose.x > axial.break_point.x else 1


class Patient:
    
    def __init__(self, name, age, gender, photo, axial=AxialFace()):
        self.name = name
        self.age = age
        self.gender = gender
        self.photo = photo
        self.axial = axial
        
    def __str__(self):
        return """
        {'name': %s,g
        'age': %s,
        'gender': %s,
        'face': %s,
        'photo': %s,
        'measurements': %s,
        'angles': %s,
        'axial': %s
        }
        """ % (self.name, self.age, self.gender, self.photo, str(self.face), str(self.measurements), str(self.angles),
               self.axial)