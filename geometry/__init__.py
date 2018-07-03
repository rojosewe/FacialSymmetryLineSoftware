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

    def __init__(self, p1, p2, w = 2, color = cs.BLACK):
        self.p1 = p1
        self.p2 = p2
        self.w = w
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