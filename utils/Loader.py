
from facial_measures import Patient, Face, Angles, Measurements
from geometry import Point
import sqlite3

conn = sqlite3.connect('files/patients.db')
    
def getFace(name):
    c = conn.cursor()
    c.execute('''SELECT patient, middle_x, upper_x, chin_x, cheekboneL_x, cheekboneR_x, cheekL_x,
            cheekR_x, mouthL_x, mouthR_x, noseL_x, noseR_x, outer_eyeL_x,
            inner_eyeL_x,outer_eyeR_x,inner_eyeR_x, middle_y,upper_y,chin_y,cheekboneL_y,
            cheekboneR_y,cheekL_y,cheekR_y,mouthL_y, mouthR_y,noseL_y, noseR_y,outer_eyeL_y,
            inner_eyeL_y,outer_eyeR_y, inner_eyeR_y FROM face WHERE patient=?''', (name,))
    x = c.fetchone()
    if x is None:
        return None
    f = Face()
    f.middle = Point(x[1], x[16])
    f.upper = Point(x[2], x[17])
    f.chin = Point(x[3], x[18])
    f.cheekboneL = Point(x[4], x[19])
    f.cheekboneR = Point(x[5], x[20])
    f.cheekL = Point(x[6], x[21])
    f.cheekR = Point(x[7], x[22])
    f.mouthL = Point(x[8], x[23])
    f.mouthR = Point(x[9], x[24])
    f.noseL = Point(x[10], x[25])
    f.noseR = Point(x[11], x[26])
    f.outer_eyeL = Point(x[12], x[27])
    f.inner_eyeL = Point(x[13], x[28])
    f.outer_eyeR = Point(x[14], x[29])
    f.inner_eyeR = Point(x[15], x[30])
    return f
    
def getMeasurements(name):
    c = conn.cursor()
    c.execute('SELECT * FROM measurements WHERE patient=?', (name,))
    x = c.fetchone()
    if x is None:
        return None
    m = Measurements()
    m.internalCantL = x[1]
    m.internalCantR = x[2]
    m.externalCantL = x[3]
    m.externalCantR = x[4]
    m.tragoL = x[5]
    m.tragoR = x[6]
    m.rebordeAlarL = x[7]
    m.rebordeAlarR = x[8]
    m.lipL = x[9]
    m.lipR = x[10]
    m.mandibleL = x[11]
    m.mandibleR = x[12]
    return m

def getAngles(name):
    c = conn.cursor()
    c.execute('SELECT * FROM angles WHERE patient=?', (name,))
    x = c.fetchone()
    if x is None:
        return None
    a = Angles()
    a.angle1 = x[1]
    a.angle2 = x[2]
    a.angle3 = x[3]
    a.angle4 = x[4]
    a.angle5 = x[5]
    a.angle6 = x[6]
    a.angle7 = x[7]
    a.angle8 = x[8]
    a.angle9 = x[9]
    a.angle10 = x[10]
    a.angle11 = x[11]
    a.angle12 = x[12]
    a.angle13 = x[13]
    a.angle14 = x[14]
    a.angle15 = x[15]
    a.angle16 = x[16]
    a.angle17 = x[17]
    a.angle18 = x[18]
    return a
    
def openPatient(name):
    pe = getPatientEntity(name)
    f = getFace(name)
    if f.noseC is None:
        f.noseC = Point((f.noseL.x + f.noseR.x) / 2, (f.noseL.y + f.noseR.y) / 2)
    m = getMeasurements(name)
    a = getAngles(name)
    p = Patient(pe[0], pe[1], pe[2], pe[3], f, m, a)
    p.face.calculate_additional()
    p.measurements.calculate(p.face)
    p.angles.calculate(p.face)
    p.proportions.calculate(m, a)
    return p
    
def getPatientEntity(name):
    print(name)
    c = conn.cursor()
    c.execute('SELECT * FROM patients WHERE name=?', (name,))
    return c.fetchone()

def getAllPatients():
    patients = []
    for name in getAllPatientsNames():
        print("exporting %s" % name)
        patients.append(openPatient(name))
    return patients

def getAllPatientsNames():
    c = conn.cursor()
    c.execute('SELECT name FROM patients')
    return [x[0] for x in c.fetchall()]