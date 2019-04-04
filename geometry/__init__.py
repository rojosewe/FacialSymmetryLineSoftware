from utils import colors as cs
import math

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def get(self):
        return [self.x, self.y]
    
    def __str__(self):
        return str([self.x, self.y])

    @staticmethod
    def from_array(a):
        return Point(a[0], a[1])

class Line:

    def __init__(self, p1, p2, w=2, color=cs.BLACK, dash=None):
        self.p1 = p1
        self.p2 = p2
        self.w = w
        self.dash = dash
        self.color = color
        if p2.x - p1.x == 0:
            self.slope = 0
        else:
            self.slope = ((p2.y - p1.y)/(p2.x - p1.x))
        
    def __str__(self):
        return str((self.p1.x, self.p2.x)) + "," + str((self.p1.y, self.p2.y))
    
    def getFormulaicValues(self):
        A = (self.p1.y - self.p2.y)
        B = (self.p2.x - self.p1.x)
        C = (self.p1.x * self.p2.y - self.p2.x * self.p1.y)
        return A, B, -C

class Mark:
    
    def __init__(self, p, r = 2, color = cs.BLACK):
        self.p = p
        self.r = r
        self.color = color
        
    def get(self):
        return self.p.get()
    
class Rect:
    
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        
def distance(point1, point2):
    return math.sqrt(math.pow(point2.x - point1.x, 2) + math.pow(point2.y - point1.y, 2))
    
def intersects(line1, line2):
    lf1 = line1.getFormulaicValues()
    lf2 = line2.getFormulaicValues()
    D  = lf1[0] * lf2[1] - lf1[1] * lf2[0]
    Dx = lf1[2] * lf2[1] - lf1[1] * lf2[2]
    Dy = lf1[0] * lf2[2] - lf1[2] * lf2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return Point(x,y)
    else:
        return None
    

def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]


def angle(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA.p1.x - lineA.p2.x), (lineA.p1.y - lineA.p2.y)]
    vB = [(lineB.p1.x - lineB.p2.x), (lineB.p1.y - lineB.p2.y)]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5

    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod / magB / magA)
    
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle) % 360

    if ang_deg-180>=0:
        # As in if statement
        return 360 - ang_deg
    else: 
        return ang_deg


class SymmetryPoint:

    def __init__(self):
        self.left = None
        self.right = None

    def get_right(self):
        self.__get_point(self.right)

    def get_left(self):
        self.__get_point(self.left)

    def __get_point(self, point):
        if point:
            return point.get()
        else:
            return None


class SymmetryAngle:

    def __init__(self, symmetry_point, reference_point_main, reference_point_2):
        self.reference_point_main = reference_point_main
        self.symmetry_point = symmetry_point
        self.reference_line = Line(reference_point_main, reference_point_2)
        self.left_line = self.get_left_line()
        self.right_line = self.get_right_line()
        self.left_angle = angle(self.reference_line, self.left_line)
        self.right_angle = angle(self.reference_line, self.right_line)
        self.proportion = self.left_angle / self.right_angle

    def get_angles(self):
        return self.left_angle, self.right_angle

    def get_proportion(self):
        return self.proportion

    def get_lines(self, color=cs.BLACK, width=2):
        return self.get_left_line(color, width), self.get_right_line(color, width)

    def get_left_line(self, color=cs.BLACK, width=2):
        return Line(self.reference_point_main, self.symmetry_point.left, color=color, w=width)

    def get_right_line(self, color=cs.BLACK, width=2):
        return Line(self.reference_point_main, self.symmetry_point.right, color=color, w=width)


class SymmetryDisjointAngle:

    def __init__(self, symmetry_point_left_1, symmetry_point_left_2,
                 reference_point_left_1, reference_point_left_2,
                 symmetry_point_right_1, symmetry_point_right_2,
                 reference_point_right_1, reference_point_right_2):
        self.reference_line_left = Line(reference_point_left_1, reference_point_left_2)
        self.reference_line_right = Line(reference_point_right_1, reference_point_right_2)
        self.left_line = Line(symmetry_point_left_1, symmetry_point_left_2)
        self.right_line = Line(symmetry_point_right_1, symmetry_point_right_2)
        self.left_angle = angle(self.reference_line_left, self.left_line)
        self.right_angle = angle(self.reference_line_right, self.right_line)
        self.proportion = self.left_angle / self.right_angle

    def get_angles(self):
        return self.left_angle, self.right_angle

    def get_proportion(self):
        return self.proportion

    def get_lines(self, color=cs.BLACK, width=2):
        return self.get_left_line(color, width), self.get_right_line(color, width)

    def get_left_line(self, color=cs.BLACK, width=2):
        return Line(self.symmetry_point_left_1, self.symmetry_point_left_2, color=color, w=width)

    def get_right_line(self, color=cs.BLACK, width=2):
        return Line(self.symmetry_point_right_2, self.symmetry_point_right_2, color=color, w=width)


class DisplacementAngle:

    def __init__(self, main_point_1, main_point_2, reference_line):
        self.main_point_1 = main_point_1
        self.main_point_2 = main_point_2
        self.reference_line = reference_line
        self.main_line = self.get_line()
        self.main_angle = angle(self.reference_line, self.main_line)

    def get_displacement_x(self):
        return self.main_point_1.x - self.main_point_2.x

    def get_displacement_y(self):
        return self.main_point_1.y - self.main_point_2.y

    def get_angle(self):
        return self.main_angle

    def get_line(self, color=cs.BLACK, width=2):
        return Line(self.main_point_1, self.main_point_2, color=color, w=width)
