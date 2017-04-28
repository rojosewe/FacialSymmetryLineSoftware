'''
Created on 17 Apr 2017

@author: rweffercifue
'''

from geometry import Rect
from facial_measures import Face, Order
from geometry import Point, Line, Mark
from utils import colors as cs
from utils import commands
from pygame import draw as d

max_v = 700

complete = 0
img = None
size = None
screen = None
rect = None
lines = []
marks = []
f = Face()

def init(pygame, path):
    global  img, size
    img = pygame.image.load(path)
    size = img.get_rect().size
    w = size[0]
    h = size[1]
    proportion = w/h
    h = min(max_v, h)
    w = int(h * proportion)
    img = pygame.transform.scale(img, (w, h))
    
def load(screen_main, left, top, right, bottom):
    global screen, rect
    screen = screen_main
    rect = Rect(left, top, right, bottom)
    print(Order.order[0])

def draw(p, pos):
    screen.blit(img, (rect.left, rect.top))
    if p.x >= rect.left and p.x < rect.right and p.y >= rect.top and p.y < rect.bottom:
        if pos < 3: 
            d.line(screen, cs.LIGHT, (p.x, rect.top), (p.x, rect.bottom), 1)
        else:
            d.circle(screen, cs.BLACK, p.get(), 2)
            d.line(screen, cs.LIGHT, (rect.left, p.y), (rect.right, p.y), 1)
            
        for l in lines:
            d.line(screen, l.color, l.p1.get(), l.p2.get(), l.w)
            
        for x in marks:
            d.circle(screen, x.color, x.get(), x.r)
    
def getFacepos(p, pos):
    global complete
    if pos < len(Order.order):
        if p.x >= rect.left and p.x < rect.right and p.y >= rect.top and p.y < rect.bottom:  
            x = Order.order[pos]
            if x == Order.HORIZONTAL_LINE:
                # set center
                vertical = Line(Point(p.x, rect.top), Point(p.x, rect.bottom), color = cs.RED)
                lines.append(vertical)  
            elif x == Order.TOP_HEAD:
                f.upper = p
            elif x == Order.CHIN:
                f.chin = p
                lines.append(Line(f.upper, f.chin, color=cs.LIGHT, w=1))
            elif x == Order.FOREHEAD:
                f.middle = p
            elif x == Order.EYE_OUTER_LEFT:
                f.outer_eyeL = p
            elif x == Order.EYE_INNER_LEFT:
                f.inner_eyeL = p
            elif x == Order.EYE_INNER_RIGHT:
                f.inner_eyeR = p
            elif x == Order.EYE_OUTER_RIGHT:
                f.outer_eyeR = p
            elif x == Order.CHEEKBONE_LEFT:
                f.cheekboneL = p
            elif x == Order.CHEEKBONE_RIGHT:
                f.cheekboneR = p
            elif x == Order.NOSE_LEFT:
                f.noseL = p
            elif x == Order.NOSE_RIGHT:
                f.noseR = p
            elif x == Order.MOUTH_LEFT:
                f.mouthL = p
            elif x == Order.MOUTH_RIGHT:
                f.mouthR = p
            elif x == Order.CHEEK_LEFT:
                f.cheekL = p
            elif x == Order.CHEEK_RIGHT:
                f.cheekR = p
            
            if pos > 0:
                marks.append(Mark(p, r = 4, color = cs.GREEN))
            print(Order.order[pos])
            pos += 1
            return True
        else:
            return False
    else:
        if complete == 0:
            print("complete")
            complete = 1
            processFullPatient(f)
        return False
    
def processClick(event, point, pos):
    return getFacepos(point, pos)

def processKey(pg, event):
    if event.key == pg.K_k:
        return commands.DELETE_MARK
    elif event.key == pg.K_c:
        return commands.CLEAR_MARKS
    elif event.key == pg.K_KP_ENTER:
        if complete == 1:
            processFullPatient()
            
def processFullPatient(f):
    print("Measured!")
    
    
def clean():
    lines.clear()
    marks.clear()
    f = Face()
    