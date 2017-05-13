import sys
from pygame import mouse as m
from geometry import Point
from workAreas import Reference, Workspace
from utils import Commands, Loader

def getPoint():
    p = m.get_pos()
    return Point(p[0], p[1])        

pos = 0

def load(pygame, patient):
    global pos
    Reference.init(pygame)
    Workspace.init(pygame, patient)
    
    left = 0
    top = 0
    right = Reference.size[0] + Workspace.size[0]
    bottom = max(Reference.size[1], Workspace.size[1])
    print(right)
    screen = pygame.display.set_mode((right, bottom))
    
    Reference.load(screen, left, top, Reference.size[0], Reference.size[1])
    Workspace.load(screen, Reference.size[0], 0, right, Workspace.size[1])
    
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
                elif command == None:
                    if event.key == pygame.K_q:
                        return Commands.EXIT
                    
        pygame.display.flip()        
    