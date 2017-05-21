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
    
def humanAngleProps(prop):
    if prop > 1.0:
        d = (prop - 1) * 100
        return "{0:.2f}% mas amplio hacia la izquierda.".format(d)
    elif prop < 1.0:
        d = (1 - prop) * 100
        return "{0:.2f}% mas amplio hacia la derecha.".format(d)
    else:
        return "Ambos lados son de angulo identico"
    

def load(pygame, patient, complete=False, loaded=False):
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
                elif command == Commands.START:
                    if Workspace.complete:
                        return Commands.START
                    else:
                        if gui.boolbox("Exiting", "You are exiting. All progress in this patient will be lost.", ["OK", "Cancel"]):
                            pygame.quit()
                            return Commands.START
                        else:
                            continue
                elif command == Commands.SHOW_PROPORTIONS:
                    if Workspace.complete:
                        prop = patient.proportions
                        
                        msg = """
Proporciones Medida:
    - Canto interno :   %s
    - Canto externo :   %s
    - Trago :           %s
    - Reborder alar :   %s
    - Comisura bucal :  %s
    - Ang. mandibular : %s
Proporciones Angulares:
    - Glabelar - Canto interno :   %s
    - Glabelar - Canto externo :   %s
    - Glabelar - Trago :           %s
    - Glabelar - Reborder alar :   %s
    - Glabelar - Comisura bucal :  %s
    - Glabelar - Ang. mandibular : %s
    - Pogonion - Trago :           %s
    - Pogonion - Comisura bucal :  %s
    - Pogonion - Ang. mandibular : %s
""" % (humanLengthProps(prop.internalCantLength), humanLengthProps(prop.externalCantLength),
       humanLengthProps(prop.tragoLength), humanLengthProps(prop.rebordeAlarLength), 
       humanLengthProps(prop.lipLength), humanLengthProps(prop.mandibleLength),
       humanAngleProps(prop.glabelarCantoIntAngle), humanAngleProps(prop.glabelarCantoExtAngle),
       humanAngleProps(prop.glablearTragoAngle), humanAngleProps(prop.glablearNasalAngle), 
       humanLengthProps(prop.glablearLabialAngle), humanLengthProps(prop.glablearMadibularAngle),
       humanAngleProps(prop.pogonionTragoAngle), humanLengthProps(prop.pogonionLabialAngle), 
       humanLengthProps(prop.pogonionMandibularAngle))
                        gui.msgbox(msg, "measurements")                    
                elif command == None:
                    if event.key == pygame.K_q:
                        return Commands.EXIT
                    
        pygame.display.flip()        
