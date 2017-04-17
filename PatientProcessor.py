import sys
from pygame import mouse as m
from geometry import Point
from workAreas import Reference, Workspace


def getPoint():
    p = m.get_pos()
    return Point(p[0], p[1])        

pos = 0

def load(pygame, path):
    global pos
    Reference.init(pygame)
    Workspace.init(pygame)
    
    left = 0
    top = 0
    right = Reference.size[0] + Workspace.size[0]
    bottom = max(Reference.size[1], Workspace.size[1])
    screen = pygame.display.set_mode((right, bottom))
    
    Reference.load(screen, left, top, Reference.size[0], Reference.size[1])
    Workspace.load(screen, Reference.size[0], 0, right, Workspace.size[1])
    
    while Workspace.complete:
        P = getPoint()
        Reference.draw(P, pos)
        Workspace.draw(P, pos)
        p = getPoint()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if Workspace.processClick(event, p, pos):
                    pos += 1
                Reference.processClick(event, p, pos)
        pygame.display.flip()    