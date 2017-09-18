
from facial_measures import Patient, Face, Angles, Measurements
from geometry import Point
import sqlite3

#    m = {'internalCantL': 41.14422963927595, 'internalCantR': 140.89986572353908, 'externalCantL': 150.13207547169816, 'externalCantR': 44.86792452830184, 'tragoL': 207.32171206597877, 'tragoR': 193.75808049405538, 'rebordeAlarL': 60.16148932741971, 'rebordeAlarR': 47.88016930479493, 'lipL': 85.77358490566041, 'lipR': 71.22641509433959, 'mandibleL': 152.91080331443047, 'mandibleR': 132.09621414303498}
#    a = {'glabelarCantoExtIzq': 77.85944654988626, 'glablearTragoIzq': 65.09982186205457, 'glabelarCantoIntIzq': 51.32562773794214, 'glablearMadibularIzq': 28.272696362029926, 'glablearNasalIzq': 23.070668171818912, 'glablearLabialIzq': 20.774545963317635, 'glablearLabialDer': 17.215015614298263, 'glablearNasalDer': 18.660355201770717, 'glablearMadibularDer': 24.36974925634328, 'glabelarCantoIntDer': 51.32562773794214, 'glablearTragoDer': 63.74883306141948, 'glabelarCantoExtDer': 51.13154749261923, 'pogonionMandibularIzq': 37.646200974108844, 'pogonionTragoIzq': 67.478912173346, 'pogonionLabialIzq': 31.31024910388655}

conn = sqlite3.connect('files/patients.db')

def initdb():
    c = conn.cursor()
    # Create table
    c.execute('CREATE TABLE IF NOT EXISTS patients (name text, age real, gender text, photo text)')
    conn.commit()
    c.execute('''CREATE TABLE IF NOT EXISTS face (patient text, 
        middle_x real, upper_x real, chin_x real,
        cheekboneL_x real, cheekboneR_x real, cheekL_x real,
        cheekR_x real, mouthL_x real, mouthR_x real,
        noseL_x real, noseR_x real, outer_eyeL_x real,
        inner_eyeL_x real,outer_eyeR_x real,inner_eyeR_x real,
        middle_y real,upper_y real,chin_y real,cheekboneL_y real,
        cheekboneR_y real,cheekL_y real,cheekR_y real,mouthL_y real,
        mouthR_y real,noseL_y real,noseR_y real,outer_eyeL_y real,
        inner_eyeL_y real,outer_eyeR_y real,inner_eyeR_y real)''')
    conn.commit()
    c.execute('''CREATE TABLE IF NOT EXISTS measurements (patient text, internalCantL float,
                internalCantR float, externalCantL float, externalCantR float, 
                tragoL float, tragoR float, rebordeAlarL float, rebordeAlarR float, 
                lipL float, lipR float, mandibleL float, mandibleR float)''')
    conn.commit()
    c.execute('''CREATE TABLE IF NOT EXISTS angles (patient text, angle1 float,
            angle2 float, angle3 float, angle4 float, angle5 float,
            angle6 float, angle7 float, angle8 float, angle9 float,
            angle10 float, angle11 float, angle12 float, angle13 float,
            angle14 float, angle15 float, angle16 float, angle17 float,
            angle18 float)''')
    conn.commit()

def insertPatientEntity(patient):
    c = conn.cursor()
    c.execute('INSERT INTO patients(name, age, gender, photo) VALUES (?, ?, ?, ?)', 
              (patient.name, patient.age, patient.gender, patient.photo))
    conn.commit()

def updatePatientEntity(patient):
    c = conn.cursor()
    c.execute('UPDATE patients SET photo = ?, age = ?, gender = ? WHERE name = ?', 
              (patient.photo, patient.age, patient.gender, patient.name))
    conn.commit()

def insertFace(patient):
    c = conn.cursor()
    f = patient.face
    print(str(f.cheekboneL))
    c.execute('''INSERT INTO face (patient, 
            middle_x, upper_x, chin_x, cheekboneL_x, cheekboneR_x, cheekL_x,
            cheekR_x, mouthL_x, mouthR_x, noseL_x, noseR_x, outer_eyeL_x,
            inner_eyeL_x,outer_eyeR_x,inner_eyeR_x, middle_y,upper_y,chin_y,cheekboneL_y,
            cheekboneR_y,cheekL_y,cheekR_y,mouthL_y, mouthR_y,noseL_y,noseR_y,outer_eyeL_y,
            inner_eyeL_y,outer_eyeR_y,inner_eyeR_y) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            , (patient.name, f.middle.x, f.upper.x , f.chin.x, f.cheekboneL.x, f.cheekboneR.x, f.cheekL.x,
            f.cheekR.x, f.mouthL.x, f.mouthR.x, f.noseL.x, f.noseR.x, f.outer_eyeL.x,
            f.inner_eyeL.x, f.outer_eyeR.x, f.inner_eyeR.x, f.middle.y, f.upper.y , f.chin.y, f.cheekboneL.y, 
            f.cheekboneR.y, f.cheekL.y,
            f.cheekR.y, f.mouthL.y, f.mouthR.y, f.noseL.y, f.noseR.y, f.outer_eyeL.y,
            f.inner_eyeL.y, f.outer_eyeR.y, f.inner_eyeR.y))
    conn.commit()
    
def updateFace(patient):
    c = conn.cursor()
    f = patient.face
    c.execute('''UPDATE face SET middle_x = ?, 
            upper_x = ?, chin_x = ?, cheekboneL_x = ?, cheekboneR_x = ?, cheekL_x = ?,
            cheekR_x = ?, mouthL_x = ?, mouthR_x = ?, noseL_x = ?, noseR_x = ?, outer_eyeL_x = ?,
            inner_eyeL_x = ?,outer_eyeR_x = ?,inner_eyeR_x = ?, middle_y = ?,upper_y = ?,
            chin_y = ?,cheekboneL_y = ?,
            cheekboneR_y = ?,cheekL_y = ?,cheekR_y = ?,mouthL_y = ?, mouthR_y = ?,noseL_y = ?,noseR_y = ?,
            outer_eyeL_y = ?, inner_eyeL_y = ?, outer_eyeR_y = ?, inner_eyeR_y = ? WHERE patient = ?'''
            , (f.middle.x, f.upper.x , f.chin.x, f.cheekboneL.x, f.cheekboneR.x, f.cheekL.x,
            f.cheekR.x, f.mouthL.x, f.mouthR.x, f.noseL.x, f.noseR.x, f.outer_eyeL.x,
            f.inner_eyeL.x, f.outer_eyeR.x, f.inner_eyeR.x, f.middle.y, f.upper.y , f.chin.y, 
            f.cheekboneL.y, f.cheekboneR.y, f.cheekL.y,
            f.cheekR.y, f.mouthL.y, f.mouthR.y, f.noseL.y, f.noseR.y, f.outer_eyeL.y,
            f.inner_eyeL.y, f.outer_eyeR.y, f.inner_eyeR.y, patient.name))
    conn.commit()
    
def getFace(name):
    c = conn.cursor()
    c.execute('''SELECT patient, middle_x, upper_x, chin_x, cheekboneL_x, cheekboneR_x, cheekL_x,
            cheekR_x, mouthL_x, mouthR_x, noseL_x, noseR_x, outer_eyeL_x,
            inner_eyeL_x,outer_eyeR_x,inner_eyeR_x, middle_y,upper_y,chin_y,cheekboneL_y,
            cheekboneR_y,cheekL_y,cheekR_y,mouthL_y, mouthR_y,noseL_y,noseR_y,outer_eyeL_y,
            inner_eyeL_y,outer_eyeR_y,inner_eyeR_y FROM face WHERE patient=?''', (name,))
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

def insertMeasurements(patient):
    c = conn.cursor()
    m = patient.measurements
            
    c.execute('''INSERT INTO measurements (patient, internalCantL, internalCantR,externalCantL,
            externalCantR,tragoL,tragoR,rebordeAlarL,rebordeAlarR,lipL,
            lipR,mandibleL, mandibleR) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            , (patient.name, m.internalCantL, m.internalCantR, m.externalCantL, 
            m.externalCantR, m.tragoL, m.tragoR, m.rebordeAlarL, m.rebordeAlarR, m.lipL, m.lipR, 
            m.mandibleL, m.mandibleR))
    conn.commit()
    
def updateMeasurements(patient):
    c = conn.cursor()
    m = patient.measurements
    c.execute('''UPDATE measurements SET internalCantL = ?, internalCantR = ?, externalCantL = ?, 
            externalCantR = ?, tragoL = ?, tragoR = ?, rebordeAlarL = ?, rebordeAlarR = ?, lipL = ?, 
            lipR = ?, mandibleL = ?, mandibleR = ? WHERE patient = ?'''
            , (m.internalCantL, m.internalCantR, m.externalCantL, 
            m.externalCantR, m.tragoL, m.tragoR, m.rebordeAlarL, m.rebordeAlarR, m.lipL, m.lipR, 
            m.mandibleL, m.mandibleR, patient.name))
    conn.commit()
    
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
    m.mandibleR  = x[12]
    return m
    
def insertAngles(patient):
    c = conn.cursor()
    a = patient.angles
    c.execute('''INSERT INTO angles (patient, angle1,
            angle2, angle3, angle4, angle5,
            angle6, angle7, angle8, angle9,
            angle10, angle11, angle12, angle13,
            angle14, angle15, angle16, angle17, angle18) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            , (patient.name, a.angle1,
            a.angle2, a.angle3, a.angle4, a.angle5,
            a.angle6, a.angle7, a.angle8, a.angle9,
            a.angle10, a.angle11, a.angle12, a.angle13,
            a.angle14, a.angle15, a.angle16, a.angle17, a.angle18))
    conn.commit()
    
def updateAngles(patient):
    c = conn.cursor()
    a = patient.angles
    c.execute('''UPDATE angles SET angle1 = ?, 
            angle2 = ?,  angle3 = ?,  angle4 = ?,  angle5 = ?, 
            angle6 = ?,  angle7 = ?,  angle8 = ?,  angle9 = ?, 
            angle10 = ?,  angle11 = ?,  angle12 = ?,  angle13 = ?, 
            angle14 = ?,  angle15 = ?,  angle16 = ?,  angle17 = ?,  angle18 = ?
            WHERE patient = ?'''
            , (a.angle1,
            a.angle2, a.angle3, a.angle4, a.angle5, a.angle6, a.angle7, 
            a.angle8, a.angle9, a.angle10, a.angle11, a.angle12, a.angle13, 
            a.angle14, a.angle15, a.angle16, a.angle17, a.angle18, patient.name))
    conn.commit()
    
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
    m = getMeasurements(name)
    a = getAngles(name)
    p = Patient(pe[0], pe[1], pe[2], pe[3], f, m, a)
    p.face.calculate_additional()
    p.measurements.calculate(p.face)
    p.proportions.calculate(m, a)
    return p

def savePatient(patient):
    exists = getPatientEntity(patient.name)
    if exists is None:
        insertPatientEntity(patient)
        insertFace(patient)
        insertMeasurements(patient)
        insertAngles(patient)
    else:
        updatePatientEntity(patient)
        updateFace(patient)
        updateMeasurements(patient)
        updateAngles(patient)
    conn.commit()
    
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