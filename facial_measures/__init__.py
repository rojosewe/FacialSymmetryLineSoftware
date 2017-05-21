from geometry import distance
import geometry
from utils import colors as cs

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
        
    def toDict(self):
        return {
            "middle": self.middle,
            "upper": self.upper,
            "chin": self.chin,
            "outer_eyeL": self.outer_eyeL,
            "inner_eyeL": self.inner_eyeL,
            "outer_eyeR": self.outer_eyeR,
            "inner_eyeR": self.inner_eyeR,
            "cheekboneL": self.cheekboneL,
            "cheekboneR": self.cheekboneR,
            "noseL": self.noseL,
            "noseR": self.noseR,
            "cheekL": self.cheekL,
            "cheekR": self.cheekR,
            "mouthL": self.mouthL,
            "mouthR": self.mouthR
        }
        
    def fromDict(self, d):
        self.middle = d["middle"]
        self.upper = d["upper"]
        self.chin = d["chin"]
        self.cheekboneL = d["cheekboneL"]
        self.cheekboneR = d["cheekboneR"]
        self.cheekL = d["cheekL"]
        self.cheekR = d["cheekR"]
        self.mouthL = d["mouthL"]
        self.mouthR = d["mouthR"]
        self.noseL = d["noseL"]
        self.noseR = d["noseR"]
        self.outer_eyeL = d["outer_eyeL"]
        self.inner_eyeL = d["inner_eyeL"]
        self.outer_eyeR = d["outer_eyeR"]
        self.inner_eyeR = d["inner_eyeR"]
        
    def __str__(self):
        d = self.toDict()
        for key in d:
            d[key] = d[key].get()
        return str(d)

class Measurements():
    
    def __init__(self):
        self.internalCantL= None
        self.internalCantR= None
        self.externalCantL= None
        self.externalCantR= None
        self.tragoL= None
        self.tragoR= None
        self.rebordeAlarL= None
        self.rebordeAlarR= None
        self.lipL= None
        self.lipR= None
        self.mandibleL= None
        self.mandibleR = None
    
    def calculate(self, f):
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
        
    def getLines(self, f, color=cs.BLACK, width=2):
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
        lines = []
        lines.append(geometry.Line(f.inner_eyeL, eye_middle, w=width, color=color))
        lines.append(geometry.Line(f.inner_eyeR, eye_middle, w=width, color=color))
        lines.append(geometry.Line(f.outer_eyeL, eye_middle, w=width, color=color))
        lines.append(geometry.Line(f.outer_eyeR, eye_middle, w=width, color=color))
        lines.append(geometry.Line(f.cheekboneL, cheek_middle, w=width, color=color))
        lines.append(geometry.Line(f.cheekboneR, cheek_middle, w=width, color=color))
        lines.append(geometry.Line(f.noseL, nose_middle, w=width, color=color))
        lines.append(geometry.Line(f.noseR, nose_middle, w=width, color=color))
        lines.append(geometry.Line(f.mouthL, mouth_middle, w=width, color=color))
        lines.append(geometry.Line(f.mouthR, mouth_middle, w=width, color=color))
        lines.append(geometry.Line(f.cheekL, mandible_middle, w=width, color=color))
        lines.append(geometry.Line(f.cheekR, mandible_middle, w=width, color=color))
        return lines
        
    def toDict(self):
        return {
            "internalCantL" : self.internalCantL,
            "internalCantR" : self.internalCantR,
            "externalCantL" : self.externalCantL,
            "externalCantR" : self.externalCantR,
            "tragoL" : self.tragoL,
            "tragoR" : self.tragoR,
            "rebordeAlarL" : self.rebordeAlarL,
            "rebordeAlarR" : self.rebordeAlarR,
            "lipL" : self.lipL,
            "lipR" : self.lipR,
            "mandibleL" : self.mandibleL,
            "mandibleR" : self.mandibleR
        }
        
    def __str__(self):
        return str(self.toDict())
        
        
class Angles():
    
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
        self.angle16 = None
        self.angle17 = None
        self.angle18 = None
         
    def calculate(self, f):
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
        line = geometry.Line(f.middle, f.inner_eyeR)
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
        line = geometry.Line(f.chin, f.cheekboneR)
        self.angle17 = geometry.angle(vertical_line, line)
        line = geometry.Line(f.chin, f.cheekR)
        self.angle18 = geometry.angle(vertical_line, line)
        
    def toDict(self):
        return {
            "glabelarCantoExtIzq" : self.angle1,
            "glablearTragoIzq" : self.angle2,
            "glabelarCantoIntIzq" : self.angle3,
            "glablearMadibularIzq" : self.angle4,
            "glablearNasalIzq" : self.angle5,
            "glablearLabialIzq" : self.angle6,
            "glablearLabialDer" : self.angle7,
            "glablearNasalDer" : self.angle8,
            "glablearMadibularDer" : self.angle9,
            "glabelarCantoIntDer" : self.angle10,
            "glablearTragoDer" : self.angle11,
            "glabelarCantoExtDer" : self.angle12,
            "pogonionMandibularIzq" : self.angle13,
            "pogonionTragoIzq" : self.angle14,
            "pogonionLabialIzq" : self.angle15,
            "pogonionLabialDer" : self.angle16,
            "pogonionTragoDer" : self.angle17,
            "pogonionMandibularDer" : self.angle18
        }
        
    def getLines(self, f, color=cs.BLACK, width=2):
        lines = []
        vertical_line = geometry.Line(f.middle, f.chin, color=color, w=width)
        lines.append(vertical_line)
        line = geometry.Line(f.middle, f.outer_eyeL, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.middle, f.cheekboneL, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.middle, f.inner_eyeL, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.middle, f.cheekL, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.middle, f.noseL, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.middle, f.mouthL, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.middle, f.mouthR, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.middle, f.noseR, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.middle, f.cheekR, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.middle, f.inner_eyeR, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.middle, f.cheekboneR, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.middle, f.outer_eyeR, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.chin, f.cheekL, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.chin, f.cheekboneL, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.chin, f.mouthL, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.chin, f.mouthR, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.chin, f.cheekR, color=color, w=width)
        lines.append(line)
        line = geometry.Line(f.chin, f.cheekboneR, color=color, w=width)
        lines.append(line)
        return lines
        
    def __str__(self):
        return str(self.toDict())
    
class Proportions():
    
    def __init__(self):
        self.internalCantLength = None
        self.externalCantLength = None
        self.tragoLength = None
        self.rebordeAlarLength = None
        self.lipLength = None
        self.mandibleLength = None
        self.glabelarCantoExtAngle = None 
        self.glablearTragoAngle = None
        self.glabelarCantoIntAngle = None
        self.glablearMadibularAngle = None
        self.glablearNasalAngle = None
        self.glablearLabialAngle = None
        self.pogonionMandibularAngle = None
        self.pogonionTragoAngle = None
        self.pogonionLabialAngle = None
        
    def calculate(self, measurements, angles):    
        self.internalCantLength = measurements.internalCantL / measurements.internalCantR
        self.externalCantLength = measurements.externalCantL / measurements.externalCantR
        self.tragoLength = measurements.tragoL / measurements.tragoR
        self.rebordeAlarLength = measurements.rebordeAlarL / measurements.rebordeAlarR
        self.lipLength = measurements.lipL / measurements.lipR
        self.mandibleLength = measurements.mandibleL / measurements.mandibleR
        self.glabelarCantoExtAngle = angles.angle1 / angles.angle12 
        self.glablearTragoAngle = angles.angle2 / angles.angle11
        self.glabelarCantoIntAngle = angles.angle3 / angles.angle10
        self.glablearMadibularAngle = angles.angle4 / angles.angle9
        self.glablearNasalAngle = angles.angle5 / angles.angle8
        self.glablearLabialAngle = angles.angle6 / angles.angle7
        self.pogonionMandibularAngle = angles.angle13 / angles.angle18
        self.pogonionTragoAngle = angles.angle14 / angles.angle17
        self.pogonionLabialAngle = angles.angle15 / angles.angle16
    
class Patient():
    
    def __init__(self, name, age, gender, photo, face=Face(), measurements=None, angles=None):
        self.name = name
        self.age = age
        self.gender = gender
        self.photo = photo
        self.face = face
        self.measurements = measurements
        self.angles = angles
        self.proportions = Proportions()
        
    def __str__(self):
        return """
        {'name': %s,
        'age': %s,
        'gender': %s,
        'face': %s,
        'photo': %s,
        'measurements': %s,
        'angles': %s
        }
        """ % (self.name, self.age, self.gender, self.photo, str(self.face), str(self.measurements), str(self.angles))