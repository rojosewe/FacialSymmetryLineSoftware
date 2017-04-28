import sys
from pygame import mouse as m
from geometry import Point
from workAreas import Reference, Workspace
from utils import commands

def getPoint():
    p = m.get_pos()
    return Point(p[0], p[1])        

pos = 0

def load(pygame, path):
    global pos
    Reference.init(pygame)
    Workspace.init(pygame, path)
    
    left = 0
    top = 0
    right = Reference.size[0] + Workspace.size[0]
    bottom = max(Reference.size[1], Workspace.size[1])
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
                if Workspace.processClick(event, p, pos):
                    pos += 1
                Reference.processClick(event, p, pos)
            elif event.type == pygame.KEYUP:
                command = Workspace.processKey(pygame, event)
                if command == commands.DELETE_MARK:
                    pos = max(pos - 1, 0)
                if command == commands.CLEAR_MARKS:
                    pos = 0
                    Workspace.clean()
                if command == None:
                    if event.key == pygame.K_q:
                        return commands.EXIT
                    
        pygame.display.flip()    