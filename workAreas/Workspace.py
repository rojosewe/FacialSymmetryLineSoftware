'''
Created on 17 Apr 2017

@author: rweffercifue
'''

from geometry import Rect
from facial_measures import Face, Order
from geometry import Point, Line, Mark
from utils import colors as cs
from utils import Commands
from pygame import draw as d
import facial_measures


max_v = 700

complete = 0
img = None
size = None
screen = None
rect = None
guideline = []
vertical = []
marks = []
patient = None

def init(pygame, patient_value):
    global  img, size, patient
    patient = patient_value
    img = pygame.image.load(patient.photo)
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
    
def deleteLastMark():
    if len(marks) == 1:
        vertical.clear()
    elif len(marks) == 0:
        guideline.clear()
    
    if len(marks) > 0:
        del marks[-1]

def draw(p, pos):
    screen.blit(img, (rect.left, rect.top))
    if p.x >= rect.left and p.x < rect.right and p.y >= rect.top and p.y < rect.bottom:
        if pos < 3: 
            d.line(screen, cs.LIGHT, (p.x, rect.top), (p.x, rect.bottom), 1)
        else:
            d.circle(screen, cs.BLACK, p.get(), 2)
            d.line(screen, cs.LIGHT, (rect.left, p.y), (rect.right, p.y), 1)
        
        if len(guideline) > 0:
            l = guideline[0]
            d.line(screen, l.color, l.p1.get(), l.p2.get(), l.w)
            
        if len(vertical) > 0:
            l = vertical[0]
            d.line(screen, l.color, l.p1.get(), l.p2.get(), l.w)
            
        for x in marks:
            d.circle(screen, x.color, x.get(), x.r)
    
def getFacepos(p, pos):
    global complete, vertical, guideline
    if pos < len(Order.order):
        if p.x >= rect.left and p.x < rect.right and p.y >= rect.top and p.y < rect.bottom:  
            x = Order.order[pos]
            if x == Order.HORIZONTAL_LINE:
                # set center
                guideline.append(Line(Point(p.x, rect.top), Point(p.x, rect.bottom), color = cs.RED))
            elif x == Order.TOP_HEAD:
                patient.face.upper = p
            elif x == Order.CHIN:
                patient.face.chin = p
                vertical.append(Line(patient.face.upper, patient.face.chin, color=cs.LIGHT, w=1))
            elif x == Order.FOREHEAD:
                patient.face.middle = p
            elif x == Order.EYE_OUTER_LEFT:
                patient.face.outer_eyeL = p
            elif x == Order.EYE_INNER_LEFT:
                patient.face.inner_eyeL = p
            elif x == Order.EYE_INNER_RIGHT:
                patient.face.inner_eyeR = p
            elif x == Order.EYE_OUTER_RIGHT:
                patient.face.outer_eyeR = p
            elif x == Order.CHEEKBONE_LEFT:
                patient.face.cheekboneL = p
            elif x == Order.CHEEKBONE_RIGHT:
                patient.face.cheekboneR = p
            elif x == Order.NOSE_LEFT:
                patient.face.noseL = p
            elif x == Order.NOSE_RIGHT:
                patient.face.noseR = p
            elif x == Order.MOUTH_LEFT:
                patient.face.mouthL = p
            elif x == Order.MOUTH_RIGHT:
                patient.face.mouthR = p
            elif x == Order.CHEEK_LEFT:
                patient.face.cheekL = p
            elif x == Order.CHEEK_RIGHT:
                patient.face.cheekR = p
            
            if pos > 0:
                marks.append(Mark(p, r = 4, color = cs.GREEN))
            print(Order.order[pos])
            pos += 1
            return Commands.NEXT
        else:
            return Commands.OUT_OF_BOUNDS
    if complete == 0:
        complete = 1
        return Commands.MEASUREMENTS_DONE
    elif complete == 1:
        return Commands.MEASUREMENTS_DONE_REP
    
def processClick(event, point, pos):
    print("Processing")
    return getFacepos(point, pos)

def processKey(pg, event):
    if event.key == pg.K_d:
        return Commands.DELETE_MARK
    elif event.key == pg.K_c:
        return Commands.CLEAR_MARKS
    elif event.key == pg.K_KP_ENTER:
        if complete == 1:
            print("1")
            processFullPatient()
            return Commands.MEASUREMENTS_DONE
        else:
            print("0")
            
def processFullPatient(patient):
    patient.measurements = facial_measures.Measurements()
    patient.angles = facial_measures.Angles()
    patient.measurements.calculate(patient.face)
    patient.angles.calulate(patient.face)
    return patient
    
def clean():
    guideline.clear()
    vertical.clear()
    marks.clear()
    patient.face = Face()
    