from geometry import distance
import geometry

class Patient():
    
    def __init__(self, name, photo, face=None):
        self.name = name
        self.photo = photo
        self.face = face

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

class Measurements():
    
    def __init__(self, f):
        vertical_line = geometry.Line(f.upper, f.chin)
        eye_line = geometry.Line(f.outer_eyeL, f.outer_eyeR)
        cheek_line = geometry.Line(f.cheekboneL, f.cheekboneR)
        nose_line = geometry.Line(f.noseL, f.noseR)
        mouth_line = geometry.Line(f.mouthL, f.mouthR)
        mandible_line = geometry.Line(f.cheekL, f.cheekR)
        eye_middle = geometry.intersects(eye_line, vertical_line)
        cheek_middle = geometry.intersects(cheek_line, vertical_line)
        nose_middle = geometry.intersects(nose_line, vertical_line)
        mouth_middle = geometry.intersects(mouth_line, vertical_line)
        mandible_middle = geometry.intersects(mandible_line, vertical_line)
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
        
class Angles():
    
    def __init__(self, f):
        vertical_line = geometry.Line(f.middle, f.chin)
        line = geometry.Line(f.middle, f.outer_eyeL)
        self.angle1 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.middle, f.cheekboneL)
        self.angle2 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.middle, f.inner_eyeL)
        self.angle3 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.middle, f.cheekL)
        self.angle4 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.middle, f.noseL)
        self.angle5 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.middle, f.mouthL)
        self.angle6 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.middle, f.mouthR)
        self.angle7 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.middle, f.noseR)
        self.angle8 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.middle, f.cheekR)
        self.angle9 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.middle, f.inner_eyeL)
        self.angle10 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.middle, f.cheekboneR)
        self.angle11 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.middle, f.outer_eyeR)
        self.angle12 = geometry.angle(vertical_line, line)
        vertical_line = geometry.Line(f.chin, f.middle)
        line = geometry.Line(f.chin, f.cheekL)
        self.angle13 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.chin, f.cheekboneL)
        self.angle14 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.chin, f.mouthL)
        self.angle15 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.chin, f.mouthR)
        self.angle16 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.chin, f.cheekR)
        self.angle17 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.chin, f.cheekboneR)
        self.angle18 = geometry.angle(vertical_line, line)