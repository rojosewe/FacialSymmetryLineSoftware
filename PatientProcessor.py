import sys
from pygame import mouse as m
from geometry import Point
from workAreas import Reference, Workspace
from utils import Commands, Loader
import easygui as gui

def getPoint():
    p = m.get_pos()
    return Point(p[0], p[1])        

pos = 0

def humanLengthProps(prop):
    if prop > 1.0:
        d = (prop - 1) * 100
        return "{0:.2f}% mas largo hacia la izquierda.".format(d)
    elif prop < 1.0:
        d = (1 - prop) * 100
        return "{0:.2f}% mas largo hacia la derecha.".format(d)
    else:
        return "Ambos lados son de distancia identica"
    

def load(pygame, patient, complete=False):
    global pos
    rw, rh = Reference.init(pygame)
    ww, wh = Workspace.init(pygame, patient)
    if complete:
        pos = 2000
    left = 0
    top = 0
    right = rw + ww
    bottom = max(rh, wh)
    print(right)
    screen = pygame.display.set_mode((right, bottom))
    
    Reference.load(screen, left, top, rw, rh)
    Workspace.load(screen, rw, 0, right, wh)
    
    while True:
        P = getPoint()
        Reference.draw(P, pos)
        Workspace.draw(P, pos)
        p = getPoint()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                command = Workspace.processClick(event, p, pos)
                print(command)
                if command == Commands.NEXT:
                    pos += 1
                elif command == Commands.MEASUREMENTS_DONE_REP:
                    continue
                elif command == Commands.MEASUREMENTS_DONE:
                    patient = Workspace.processFullPatient(patient)
                    Loader.savePatient(patient)
                Reference.processClick(event, p, pos)
            elif event.type == pygame.KEYUP:
                command = Workspace.processKey(pygame, event)
                if command == Commands.DELETE_MARK:
                    pos = max(pos - 1, 0)
                    Workspace.deleteLastMark()
                elif command == Commands.CLEAR_MARKS:
                    pos = 0
                    Workspace.clean()
                elif command == Commands.SHOW_PROPORTIONS:
                    if Workspace.complete:
                        internalCant = patient.measurements.internalCantL / patient.measurements.internalCantR
                        externalCant = patient.measurements.externalCantL / patient.measurements.externalCantR
                        trago = patient.measurements.tragoL / patient.measurements.tragoR
                        rebordeAlar = patient.measurements.rebordeAlarL / patient.measurements.rebordeAlarR
                        lip = patient.measurements.lipL / patient.measurements.lipR
                        mandible = patient.measurements.mandibleL / patient.measurements.mandibleR
                        
                        
                        msg = """
Proporciones:
    - Canto interno :   %s
    - Canto externo :   %s
    - Trago :           %s
    - Reborder alar :   %s
    - Comisura bucal :  %s
    - Ang. mandibular : %s
    - 
""" % (humanLengthProps(internalCant), humanLengthProps(externalCant),
       humanLengthProps(trago), humanLengthProps(rebordeAlar), 
       humanLengthProps(lip), humanLengthProps(mandible))
                        gui.msgbox(msg, "measurements")                    
                elif command == None:
                    if event.key == pygame.K_q:
                        return Commands.EXIT
                    
        pygame.display.flip()        
    