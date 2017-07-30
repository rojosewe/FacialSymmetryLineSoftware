'''
Created on 17 Apr 2017

@author: rweffercifue
'''

from geometry import Rect
from facial_measures import Face, Order
from geometry import Point, Line, Mark
from utils import colors as cs
from utils import Commands
import facial_measures
from PIL import Image
from PIL.ImageTk import PhotoImage
from workAreas.Reference import img_obj


max_v = 700

complete = False
screen = None
rect = None
patient = None
showMeasures = True
showAngles = True
guidelines = []
marks = []
img_obj = None


def init(patient_value):
    global  patient, showMeasures, showAngles
    patient = patient_value
    showMeasures = True
    showAngles = True
    pil_img = Image.open(patient.photo)
    w, h = pil_img.size
    proportion = w/h
    h = min(max_v, h)
    w = int(h * proportion)
    return (w, h)
    
def load(screen_main, left, top, right, bottom):
    global screen, rect, img_obj
    screen = screen_main
    rect = Rect(left, top, right, bottom)
    img_obj = Image.open(patient.photo)
    img_obj.resize((120, 120), Image.ANTIALIAS)
    img_obj = PhotoImage(img_obj, size=(120, 120))
    screen.create_image(rect.left, rect.top, image=img_obj, anchor="nw")
    
def deleteLastMark():
    global complete
    if len(marks) == 1:
        vertical.clear()
    elif len(marks) == 0:
        guideline.clear()
    complete = False
    if len(marks) > 0:
        del marks[-1]

# def draw(p, pos):
#     if p.x >= rect.left and p.x < rect.right and p.y >= rect.top and p.y < rect.bottom:
#         if pos < 3: 
#             d.line(screen, cs.LIGHT, (p.x, rect.top), (p.x, rect.bottom), 1)
#         else:
#             d.circle(screen, cs.BLACK, p.get(), 2)
#             d.line(screen, cs.LIGHT, (rect.left, p.y), (rect.right, p.y), 1)
#         
#         if len(guideline) > 0:
#             l = guideline[0]
#             d.line(screen, l.color, l.p1.get(), l.p2.get(), l.w)
#             
#         if len(vertical) > 0:
#             l = vertical[0]
#             d.line(screen, l.color, l.p1.get(), l.p2.get(), l.w)
#             
#         for x in marks:
#             d.circle(screen, x.color, x.get(), x.r)
#         if complete:
#             if showMeasures:
#                 for m in measures:
#                     d.line(screen, m.color, m.p1.get(), m.p2.get(), m.w)
#                     
#             if showAngles:
#                 for a in angles:
#                     d.line(screen, a.color, a.p1.get(), a.p2.get(), a.w)
                    
def create_line(line):
    return screen.create_line(line.p1.x, line.p1.y, 
                              line.p2.x, line.p2.y, fill=line.color, width=line.w)
    
def create_mark(mark):
    return screen.create_oval(mark.p.x, mark.p.y, mark.p.x + mark.r, 
                              mark.p.y + mark.r, fill=mark.color)
    
def getFacepos(p, pos):
    global complete, vertical, guideline
    if pos < len(Order.order):
        if p.x >= rect.left and p.x < rect.right and p.y >= rect.top and p.y < rect.bottom:  
            x = Order.order[pos]
            if x == Order.HORIZONTAL_LINE:
                guidelines.append(create_line(Line(Point(p.x, rect.top), 
                                                Point(p.x, rect.bottom), color = cs.RED)))
            elif x == Order.TOP_HEAD:
                patient.face.upper = p
            elif x == Order.CHIN:
                patient.face.chin = p
                line = Line(patient.face.upper, patient.face.chin, color=cs.LIGHT, w=1)
                guidelines.append(line)
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
                marks.append(create_mark(Mark(p, r = 4, color = cs.GREEN)))
            print(Order.order[pos])
            pos += 1
            return Commands.NEXT
        else:
            return Commands.OUT_OF_BOUNDS
    if not complete:
        complete = True
        return Commands.MEASUREMENTS_DONE
    else:
        return Commands.MEASUREMENTS_DONE_REP
    
def addMeasures(patient):
    global measures
    measures = patient.measurements.getLines(patient.face, color = cs.GREEN, width = 2)

def addAngles(patient):
    global angles
    angles = patient.angles.getLines(patient.face, color = cs.BLUE, width = 2)
    
def processClick(event, point, pos):
    return getFacepos(point, pos)

def processKey(pg, event):
    global showAngles, showMeasures
    if event.char == "d":
        return Commands.DELETE_MARK
    elif event.char == "c":
        return Commands.CLEAR_MARKS
    elif event.char == "a":
        showAngles = not showAngles
    elif event.char == "m":
        showMeasures = not showMeasures
    elif event.char == "p":
        return Commands.SHOW_PROPORTIONS
    elif event.char == "n":
        return Commands.START
            
def processFullPatient(patient):
    patient.measurements = facial_measures.Measurements()
    patient.angles = facial_measures.Angles()
    patient.measurements.calculate(patient.face)
    patient.angles.calculate(patient.face)
    patient.proportions.calculate(patient.measurements, patient.angles)
    addMeasures(patient)
    addAngles(patient)
    return patient
    
def clean():
    global complete
    guideline.clear()
    vertical.clear()
    marks.clear()
    patient.face = Face()
    measures.clear()
    angles.clear()
    complete = False