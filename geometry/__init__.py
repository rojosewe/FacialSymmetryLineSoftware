from utils import colors as cs
import math

class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def get(self):
        return (self.x, self.y)
    
    def __str__(self):
        return str((self.x, self.x))

class Line:

    def __init__(self, p1, p2, w = 2, color = cs.BLACK):
        self.p1 = p1
        self.p2 = p2
        self.w = w
        self.color = color
        self.slope = ((p2.y - p1.y)/(p2.x - p1.x))
        
    def __str__(self):
        return (self.p1.x, self.p2.x) + "," + (self.p1.y, self.p2.y)

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
    math.sqrt(math.pow(point2.x - point1.x, 2) + math.pow(point2.y - point1.y, 2))
        