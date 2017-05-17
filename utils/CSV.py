'''
Created on May 14, 2017

@author: root
'''

columns = ["Nombre", "Edad", "Genero", "canto_interno_izq", "canto_externo_izq", "trago_izq", "reborde_alar_izq",
           "comisura_labial_izq", "angulo_mandibular_izq", 
           "canto_interno_der", "canto_externo_der", "trago_der", "reborde_alar_der",
           "comisura_labial_der", "angulo_mandibular_der", 
           "ang_glabelar_canto_interno_izq", "ang_glabelar_canto_externo_izq", "ang_glabelar_trago_izq", 
           "ang_glabelar_reborde_alar_izq", "ang_glabelar_comisura_labial_izq", "ang_glabelar_angulo_mandibular_izq", 
           "ang_glabelar_canto_interno_der", "ang_glabelar_canto_externo_der", "ang_glabelar_trago_der", 
           "ang_glabelar_reborde_alar_der", "ang_glabelar_comisura_labial_der", "ang_glabelar_angulo_mandibular_der",
            "ang_pogonion_trago_izq", "ang_pogonion_comisura_labial_izq", "ang_pogonion_angulo_mandibular_izq", 
           "ang_pogonion_trago_der", "ang_pogonion_comisura_labial_der", "ang_pogonion_angulo_mandibular_der"
           ]

def patientsToCSV(patients, file):
    with open(file, mode='w+') as f:
        f.write(",".join(columns) + "\n")
        for p in patients:
            str = "'%s',%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
p.name, p.age, p.gender, p.measurements.internalCantL, p.measurements.externalCantL, p.measurements.tragoL, p.measurements.rebordeAlarL, 
p.measurements.lipL, p.measurements.mandibleL, p.measurements.internalCantR, p.measurements.externalCantR, 
p.measurements.tragoR, p.measurements.rebordeAlarR, p.measurements.lipR, p.measurements.mandibleR, 
p.angles.angle3, p.angles.angle1, p.angles.angle2, p.angles.angle5, p.angles.angle6, p.angles.angle4, 
p.angles.angle10, p.angles.angle12, p.angles.angle11, p.angles.angle8, p.angles.angle7, p.angles.angle9, 
p.angles.angle14, p.angles.angle15, p.angles.angle13, p.angles.angle17, p.angles.angle16, p.angles.angle18)
            f.write(str)