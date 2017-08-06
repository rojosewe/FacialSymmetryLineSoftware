'''
Created on May 14, 2017

@author: root
'''

import os

columns = ["Nombre", "Edad", "Genero", "canto_interno_der", "canto_externo_der", "trago_der", "reborde_alar_der",
           "comisura_labial_der", "angulo_mandibular_der", 
           "canto_interno_izq", "canto_externo_izq", "trago_izq", "reborde_alar_izq",
           "comisura_labial_izq", "angulo_mandibular_izq", 
           "ang_glabelar_canto_interno_der", "ang_glabelar_canto_externo_der", "ang_glabelar_trago_der", 
           "ang_glabelar_reborde_alar_der", "ang_glabelar_comisura_labial_der", "ang_glabelar_angulo_mandibular_der", 
           "ang_glabelar_canto_interno_izq", "ang_glabelar_canto_externo_izq", "ang_glabelar_trago_izq", 
           "ang_glabelar_reborde_alar_izq", "ang_glabelar_comisura_labial_izq", "ang_glabelar_angulo_mandibular_izq",
            "ang_pogonion_trago_der", "ang_pogonion_comisura_labial_der", "ang_pogonion_angulo_mandibular_der", 
           "ang_pogonion_trago_izq", "ang_pogonion_comisura_labial_izq", "ang_pogonion_angulo_mandibular_izq",
           "prop_longitud_canto_interno", "prop_longitud_canto_externo", "prop_longitud_trago", "prop_longitud_reborde_alar",
           "prop_longitud_comisura_labial", "prop_longitud_ang_mandibular", "prop_angulo_glabelar_canto_ext", 
           "prop_angulo_glabelar_trago", "prop_angulo_glabelar_canto_int",  "prop_angulo_glabelar_ang_mandibular", 
           "prop_angulo_glabelar_reborde_alar", "prop_angulo_pogonion_ang_mandibular", "prop_angulo_pogonion_trago", 
           "prop_angulo_pogonion_comisura_labial"
           ]

def patientsToCSV(patients, file):
    with open(file, mode='w+') as f:
        f.write(",".join(columns) + "\n")
        for p in patients:
            str = "'%s',%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s%s" % (
p.name, p.age, p.gender, p.measurements.internalCantL, p.measurements.externalCantL, p.measurements.tragoL, p.measurements.rebordeAlarL, 
p.measurements.lipL, p.measurements.mandibleL, p.measurements.internalCantR, p.measurements.externalCantR, 
p.measurements.tragoR, p.measurements.rebordeAlarR, p.measurements.lipR, p.measurements.mandibleR, 
p.angles.angle3, p.angles.angle1, p.angles.angle2, p.angles.angle5, p.angles.angle6, p.angles.angle4, 
p.angles.angle14, p.angles.angle15, p.angles.angle13, p.angles.angle17, p.angles.angle16, p.angles.angle18,
p.angles.angle10, p.angles.angle12, p.angles.angle11, p.angles.angle8, p.angles.angle7, p.angles.angle9, 
p.proportions.internalCantLength, p.proportions.externalCantLength, p.proportions.tragoLength, p.proportions.rebordeAlarLength,  
p.proportions.lipLength, p.proportions.mandibleLength, 
p.proportions.glabelarCantoExtAngle, p.proportions.glablearTragoAngle,
p.proportions.glabelarCantoIntAngle, p.proportions.glablearMadibularAngle, p.proportions.glablearNasalAngle, 
p.proportions.pogonionMandibularAngle, p.proportions.pogonionTragoAngle, p.proportions.pogonionLabialAngle, 
os.linesep)
            f.write(str)
