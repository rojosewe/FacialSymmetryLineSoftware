from geometry import distance
import geometry
from utils import colors as cs
from geometry import Point

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
        self.noseC = None
        self.noseR = None
        self.outer_eyeL = None
        self.inner_eyeL = None
        self.outer_eyeR = None
        self.inner_eyeR = None
        self.malarL = None
        self.malarR = None
        
    def calculate_additional(self):
        malar_eye_lineL = geometry.Line(self.outer_eyeL, self.mouthL)
        malar_nose_lineL = geometry.Line(self.noseL, self.cheekboneL)
        self.malarL = geometry.intersects(malar_eye_lineL, malar_nose_lineL)
        malar_eye_lineR = geometry.Line(self.outer_eyeR, self.mouthR)
        malar_nose_lineR = geometry.Line(self.noseR, self.cheekboneR)
        self.malarR = geometry.intersects(malar_eye_lineR, malar_nose_lineR)
    
    def toDict(self):
        return {
            "middle": self.middle.get(),
            "upper": self.upper.get(),
            "chin": self.chin.get(),
            "outer_eyeL": self.outer_eyeL.get(),
            "inner_eyeL": self.inner_eyeL.get(),
            "outer_eyeR": self.outer_eyeR.get(),
            "inner_eyeR": self.inner_eyeR.get(),
            "cheekboneL": self.cheekboneL.get(),
            "cheekboneR": self.cheekboneR.get(),
            "noseL": self.noseL.get(),
            "noseC": self.noseC.get(),
            "noseR": self.noseR.get(),
            "cheekL": self.cheekL.get(),
            "cheekR": self.cheekR.get(),
            "mouthL": self.mouthL.get(),
            "mouthR": self.mouthR.get(),
            "malarL": self.malarL.get(),
            "malarR": self.malarR.get()
        }
        
    def fromDict(self, d):
        self.middle = Point.from_array(d["middle"])
        self.upper = Point.from_array(d["upper"])
        self.chin = Point.from_array(d["chin"])
        self.cheekboneL = Point.from_array(d["cheekboneL"])
        self.cheekboneR = Point.from_array(d["cheekboneR"])
        self.cheekL = Point.from_array(d["cheekL"])
        self.cheekR = Point.from_array(d["cheekR"])
        self.mouthL = Point.from_array(d["mouthL"])
        self.mouthR = Point.from_array(d["mouthR"])
        self.noseL = Point.from_array(d["noseL"])
        self.noseC = Point.from_array(d["noseC"])
        self.noseR = Point.from_array(d["noseR"])
        self.outer_eyeL = Point.from_array(d["outer_eyeL"])
        self.inner_eyeL = Point.from_array(d["inner_eyeL"])
        self.outer_eyeR = Point.from_array(d["outer_eyeR"])
        self.inner_eyeR = Point.from_array(d["inner_eyeR"])
        self.malarL = Point.from_array(d["malarL"])
        self.malarR = Point.from_array(d["malarR"])
        
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

        self.malarExternalCantL = None
        self.malarInternalCantL = None
        self.malarNoseL = None
        self.malarLipL = None

        self.malarExternalCantR = None
        self.malarInternalCantR = None
        self.malarNoseR = None
        self.malarLipR = None

        self.noseCMalarL = None
        self.noseCMalarR = None
    
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

        self.malarExternalCantL = geometry.distance(f.outer_eyeL, f.malarL)
        self.malarExternalCantR = geometry.distance(f.outer_eyeR, f.malarR)
        self.malarInternalCantL = geometry.distance(f.inner_eyeL, f.malarL)
        self.malarInternalCantR = geometry.distance(f.inner_eyeR, f.malarR)
        self.malarNoseL = geometry.distance(f.noseL, f.malarL)
        self.malarNoseR = geometry.distance(f.noseR, f.malarR)
        self.malarLipL = geometry.distance(f.mouthL, f.malarL)
        self.malarLipR = geometry.distance(f.mouthR, f.malarR)
        self.noseCMalarL = geometry.distance(f.noseC, f.malarL)
        self.noseCMalarR = geometry.distance(f.noseC, f.malarR)

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
        upperLines = []
        lowerLines = []
        malarLines = []
        upperLines.append(geometry.Line(f.inner_eyeL, eye_middle, w=width, color=color))
        upperLines.append(geometry.Line(f.inner_eyeR, eye_middle, w=width, color=color))
        upperLines.append(geometry.Line(f.outer_eyeL, eye_middle, w=width, color=color))
        upperLines.append(geometry.Line(f.outer_eyeR, eye_middle, w=width, color=color))
        upperLines.append(geometry.Line(f.cheekboneL, cheek_middle, w=width, color=color))
        upperLines.append(geometry.Line(f.cheekboneR, cheek_middle, w=width, color=color))
        upperLines.append(geometry.Line(f.noseL, nose_middle, w=width, color=color))
        upperLines.append(geometry.Line(f.noseR, nose_middle, w=width, color=color))
        
        lowerLines.append(geometry.Line(f.mouthL, mouth_middle, w=width, color=color))
        lowerLines.append(geometry.Line(f.mouthR, mouth_middle, w=width, color=color))
        lowerLines.append(geometry.Line(f.cheekL, mandible_middle, w=width, color=color))
        lowerLines.append(geometry.Line(f.cheekR, mandible_middle, w=width, color=color))
        
        malarLines.append(geometry.Line(f.outer_eyeL, f.malarL, w=width, color=color))
        malarLines.append(geometry.Line(f.outer_eyeR, f.malarR, w=width, color=color))
        malarLines.append(geometry.Line(f.inner_eyeL, f.malarL, w=width, color=color))
        malarLines.append(geometry.Line(f.inner_eyeR, f.malarR, w=width, color=color))
        malarLines.append(geometry.Line(f.noseL, f.malarL, w=width, color=color))
        malarLines.append(geometry.Line(f.noseR, f.malarR, w=width, color=color))
        malarLines.append(geometry.Line(f.mouthL, f.malarL, w=width, color=color))
        malarLines.append(geometry.Line(f.mouthR, f.malarR, w=width, color=color))
        malarLines.append(geometry.Line(f.noseC, f.malarL, w=width, color=color))
        malarLines.append(geometry.Line(f.noseC, f.malarR, w=width, color=color))

        return upperLines, lowerLines, malarLines
        
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
        self.malarL = None
        self.malarR = None
        self.malarInternalCantL = None
        self.malarInternalCantR = None
        self.malarNoseL = None
        self.malarNoseR = None
        self.angleNoseCMalarL = None
        self.angleNoseCMalarR = None
         
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
        
        y = geometry.Point(f.noseC.x, 0)
        noseCVertical = geometry.Line(f.noseC, y)
        line = geometry.Line(f.noseC, f.malarL)
        self.angleNoseCMalarL = geometry.angle(noseCVertical, line)
        line = geometry.Line(f.noseC, f.malarR)
        self.angleNoseCMalarR = geometry.angle(noseCVertical, line)

        eyemouthLineL = geometry.Line(f.outer_eyeL, f.mouthL)
        self.malarL = geometry.angle(vertical_line, eyemouthLineL)
        eyemouthLineR = geometry.Line(f.outer_eyeR, f.mouthR)
        self.malarR = geometry.angle(vertical_line, eyemouthLineR)
        line = geometry.Line(f.inner_eyeL, f.malarL)
        self.malarInternalCantL = geometry.angle(eyemouthLineL, line)
        line = geometry.Line(f.inner_eyeR, f.malarR)
        self.malarInternalCantR = geometry.angle(eyemouthLineR, line)
        line = geometry.Line(f.noseL, f.malarL)
        self.malarNoseL = geometry.angle(eyemouthLineL, line)
        line = geometry.Line(f.noseR, f.malarR)
        self.malarNoseR = geometry.angle(eyemouthLineR, line)

        
    def getLines(self, f, color=cs.BLACK, width=2):
        upperLines = []
        lowerLines = []
        vertical_line = geometry.Line(f.middle, f.chin, color=color, w=width)
        upperLines.append(vertical_line)
        line = geometry.Line(f.middle, f.outer_eyeL, color=color, w=width)
        upperLines.append(line)
        line = geometry.Line(f.middle, f.cheekboneL, color=color, w=width)
        upperLines.append(line)
        line = geometry.Line(f.middle, f.inner_eyeL, color=color, w=width)
        upperLines.append(line)
        line = geometry.Line(f.middle, f.cheekL, color=color, w=width)
        lowerLines.append(line)
        line = geometry.Line(f.middle, f.noseL, color=color, w=width)
        upperLines.append(line)
        line = geometry.Line(f.middle, f.mouthL, color=color, w=width)
        lowerLines.append(line)
        line = geometry.Line(f.middle, f.mouthR, color=color, w=width)
        lowerLines.append(line)
        line = geometry.Line(f.middle, f.noseR, color=color, w=width)
        upperLines.append(line)
        line = geometry.Line(f.middle, f.cheekR, color=color, w=width)
        lowerLines.append(line)
        line = geometry.Line(f.middle, f.inner_eyeR, color=color, w=width)
        upperLines.append(line)
        line = geometry.Line(f.middle, f.cheekboneR, color=color, w=width)
        upperLines.append(line)
        line = geometry.Line(f.middle, f.outer_eyeR, color=color, w=width)
        upperLines.append(line)
        line = geometry.Line(f.chin, f.cheekL, color=color, w=width)
        lowerLines.append(line)
        line = geometry.Line(f.chin, f.cheekboneL, color=color, w=width)
        lowerLines.append(line)
        line = geometry.Line(f.chin, f.mouthL, color=color, w=width)
        lowerLines.append(line)
        line = geometry.Line(f.chin, f.mouthR, color=color, w=width)
        lowerLines.append(line)
        line = geometry.Line(f.chin, f.cheekR, color=color, w=width)
        lowerLines.append(line)
        line = geometry.Line(f.chin, f.cheekboneR, color=color, w=width)
        lowerLines.append(line)
        
        upperLines.append(geometry.Line(f.noseC, f.outer_eyeL, w=width, color=color))
        upperLines.append(geometry.Line(f.noseC, f.outer_eyeR, w=width, color=color))
        upperLines.append(geometry.Line(f.noseC, f.inner_eyeL, w=width, color=color))
        upperLines.append(geometry.Line(f.noseC, f.inner_eyeR, w=width, color=color))
        
        return upperLines, lowerLines
        
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
        self.malarLength = None
        self.malarExternalCantLength = None
        self.malarInternalCantLength = None
        self.malarNoseLength = None
        self.malarLipLength = None
        self.noseCMalarLength = None

        self.glabelarCantoExtAngle = None 
        self.glablearTragoAngle = None
        self.glabelarCantoIntAngle = None
        self.glablearMadibularAngle = None
        self.glablearNasalAngle = None
        self.glablearLabialAngle = None
        self.pogonionMandibularAngle = None
        self.pogonionTragoAngle = None
        self.pogonionLabialAngle = None
        self.lengthAverage = None
        self.upperLengthAverage = None
        self.lowerLengthAverage = None
        self.angleAverage = None
        self.upperAngleAverage = None
        self.lowerAngleAverage = None
        self.malarLengthAverage = None
        self.malarAngleAverage = None
        self.angleNoseCMalarAngle = None
        self.malarAngle = None
        self.malarInternalCantAngle = None
        self.malarNoseAngle = None

    def calculate(self, measurements, angles):    
        self.internalCantLength = measurements.internalCantL / measurements.internalCantR
        self.externalCantLength = measurements.externalCantL / measurements.externalCantR
        self.tragoLength = measurements.tragoL / measurements.tragoR
        self.rebordeAlarLength = measurements.rebordeAlarL / measurements.rebordeAlarR
        self.lipLength = measurements.lipL / measurements.lipR
        self.mandibleLength = measurements.mandibleL / measurements.mandibleR
        self.malarExternalCantLength = measurements.malarExternalCantL / measurements.malarExternalCantR
        self.malarInternalCantLength = measurements.malarInternalCantL / measurements.malarInternalCantR
        self.malarNoseLength = measurements.malarNoseL / measurements.malarNoseR
        self.malarLipLength = measurements.malarLipL / measurements.malarLipR
        self.noseCMalarLength = measurements.noseCMalarL / measurements.noseCMalarR

        self.glabelarCantoExtAngle = angles.angle1 / angles.angle12 
        self.glablearTragoAngle = angles.angle2 / angles.angle11
        self.glabelarCantoIntAngle = angles.angle3 / angles.angle10
        self.glablearMadibularAngle = angles.angle4 / angles.angle9
        self.glablearNasalAngle = angles.angle5 / angles.angle8
        self.glablearLabialAngle = angles.angle6 / angles.angle7
        self.pogonionMandibularAngle = angles.angle13 / angles.angle18
        self.pogonionTragoAngle = angles.angle14 / angles.angle17
        self.pogonionLabialAngle = angles.angle15 / angles.angle16
        self.angleNoseCMalarAngle = angles.angleNoseCMalarL / angles.angleNoseCMalarR
        self.malarAngle = angles.malarL / angles.malarR
        self.malarInternalCantAngle = angles.malarInternalCantL / angles.malarInternalCantR
        self.malarNoseAngle = angles.malarNoseL / angles.malarNoseR

        lengths = [self.internalCantLength, self.externalCantLength,
                   self.tragoLength, self.rebordeAlarLength,
                   self.lipLength, self.mandibleLength,
                   self.noseCMalarLength, self.malarExternalCantLength, self.malarInternalCantLength,
                   self.malarNoseLength, self.malarLipLength]
        self.lengthAverage = sum(lengths) / float(len(lengths))
        lengths = [self.internalCantLength, self.externalCantLength,
                   self.tragoLength, self.rebordeAlarLength]
        self.upperLengthAverage = sum(lengths) / float(len(lengths))
        lengths = [self.lipLength, self.mandibleLength]
        self.lowerLengthAverage = sum(lengths) / float(len(lengths))

        lengths = [self.noseCMalarLength, self.malarExternalCantLength, self.malarInternalCantLength,
                   self.malarNoseLength, self.malarLipLength]
        self.malarLengthAverage = sum(lengths) / float(len(lengths))

        angles = [self.glabelarCantoIntAngle, self.glabelarCantoExtAngle,
                  self.glablearTragoAngle, self.glablearNasalAngle,
                  self.glablearLabialAngle, self.glablearMadibularAngle,
                  self.pogonionTragoAngle, self.pogonionLabialAngle,
                  self.pogonionMandibularAngle, self.angleNoseCMalarAngle]
        self.angleAverage = sum(angles) / float(len(angles))
        angles = [self.glabelarCantoIntAngle, self.glabelarCantoExtAngle,
                              self.glablearTragoAngle, self.glablearNasalAngle, 
                              self.angleNoseCMalarAngle]
        self.upperAngleAverage = sum(angles) / float(len(angles))
        angles = [self.glablearLabialAngle, self.glablearMadibularAngle,
                  self.pogonionTragoAngle, self.pogonionLabialAngle,
                  self.pogonionMandibularAngle]
        self.lowerAngleAverage = sum(angles) / float(len(angles))

        angles = [self.malarAngle, self.malarInternalCantAngle,
                  self.malarNoseAngle]
        self.malarAngleAverage = sum(angles) / float(len(angles))


class Patient():
    
    def __init__(self, name, age, gender, photo, face=Face(), measurements=Measurements(), angles=Angles()):
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
        {'name': %s,g
        'age': %s,
        'gender': %s,
        'face': %s,
        'photo': %s,
        'measurements': %s,
        'angles': %s
        }
        """ % (self.name, self.age, self.gender, self.photo, str(self.face), str(self.measurements), str(self.angles))