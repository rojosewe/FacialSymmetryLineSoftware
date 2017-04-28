from geometry import distance
import geometry
from builtins import None

def Patient(name, photo, face=None):
    name = name
    photo = photo
    face = face

class Face():
    
    def __init__(self):
        self.middle = None
        self.upper = None
        self.chin = None
        self.cheekboneL = None
        self.cheekboneR = None
        self.cheekL = None
        self.cheekR = None
        self.mouthL = None
        self.mouthR = None
        self.noseL = None
        self.noseR = None
        self.outer_eyeL = None
        self.inner_eyeL = None
        self.outer_eyeR = None
        self.inner_eyeR = None

class measurements():
    
    def __init__(self):
        self.internalCantL = None
        self.internalCantR = None
        self.externalCantL = None
        self.externalCantR = None
        self.tragoR = None
        self.tragoL = None
        self.rebordeAlarL = None
        self.rebordeAlarR = None
        self.lipL = None
        self.lipR = None
        self.mandibleL = None
        self.mandibleR = None
        
    def calculate(self, f):
        eye_line = geometry.Line(f.outer_eyeL, f.outer_eyeR)
        cheek_line = geometry.Line(f.cheekboneL, f.cheekboneR)
        nose_line = geometry.Line(f.noseL, f.noseR)
        mouth_line = geometry.Line(f.mouthL, f.mouthR)
        mandible_line = geometry.Line(f.cheekL, f.cheekR)
        eye_middle = None
        cheek_middle = None
        nose_middle = None
        mouth_middle = None
        mandible_middle = None
        self.internalCantL = geometry.distance(f.inner_eyeL, eye_middle)
        self.internalCantR = geometry.distance(f.inner_eyeR, eye_middle)
        self.externalCantL = geometry.distance(f.outer_eyeL, eye_middle)
        self.externalCantR = geometry.distance(f.outer_eyeR, eye_middle)
        self.tragoL = geometry.distance(f.cheekboneL, cheek_middle)
        self.tragoR = geometry.distance(f.cheekboneR, cheek_middle)
        self.rebordeAlarL = geometry.distance(f.noseL, nose_middle)
        self.rebordeAlarR = geometry.distance(f.noseR, nose_middle)
        self.lipL = geometry.distance(f.mouthL, mouth_middle)
        self.lipR = geometry.distance(f.mouthR, mouth_middle)
        self.mandibleL = geometry.distance(f.cheekL, mandible_middle)
        self.mandibleR = geometry.distance(f.cheekR, mandible_middle)
        
class angles():
    
    def __init__(self):
        self.angle1 = None
        self.angle2 = None
        self.angle3 = None
        self.angle4 = None
        self.angle5 = None
        self.angle6 = None
        self.angle7 = None
        self.angle8 = None
        self.angle9 = None
        self.angle10 = None
        self.angle11 = None
        self.angle12 = None
        self.angle13 = None
        self.angle14 = None
        self.angle15 = None
