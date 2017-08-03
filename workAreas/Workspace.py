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
showMeasuresUI = True
showAnglesUI = True
showMeasures = True
showAngles = True
guideline = []
vline = []
marks = []
img_obj = None
measures = []
angles = []

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
    img_obj = img_obj.resize((right - left, bottom - top), Image.ANTIALIAS)
    img_obj = PhotoImage(img_obj)
    screen.create_image(rect.left, rect.top, image=img_obj, anchor="nw")
                
def inBox(p):
    return p.x >= rect.left and p.x < rect.right and p.y >= rect.top and p.y < rect.bottom
    
def create_line(line):
    return screen.create_line(line.p1.x, line.p1.y, 
                              line.p2.x, line.p2.y, fill=line.color, width=line.w)
    
def createGuideline(line):
    guideline.append(create_line(line))
    
def removeGuideline():
    global screen
    while len(guideline) > 0:
        screen.delete(guideline.pop())

def createVline(line):
    vline.append(create_line(line))
    
def removeVline():
    global screen
    while len(vline) > 0:
        screen.delete(vline.pop())
    
def create_mark(mark):
    return screen.create_oval(mark.p.x - mark.r, mark.p.y - mark.r, mark.p.x + mark.r, 
                              mark.p.y + mark.r, fill=mark.color)
    
def getFacepos(p, pos):
    global complete
    if inBox(p):
        x = Order.getPos(pos)
        if x:
            if x == Order.HORIZONTAL_LINE:
                createGuideline(Line(Point(p.x, rect.top), 
                                                Point(p.x, rect.bottom), color = cs.RED))
            elif x == Order.TOP_HEAD:
                patient.face.upper = p
            elif x == Order.CHIN:
                patient.face.chin = p
                createVline(Line(patient.face.upper, patient.face.chin, color=cs.LIGHT, w=1))
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
                _auxAddMark(p)
                pos += 1
                return Commands.MEASUREMENTS_DONE
            if pos > 0:
                _auxAddMark(p)
            print(x)
            pos += 1
            return Commands.NEXT
    else:
        return Commands.OUT_OF_BOUNDS
    if not complete:
        return Commands.MEASUREMENTS_DONE
    else:
        return Commands.MEASUREMENTS_DONE_REP
    
def _auxAddMark(p):
    marks.append(create_mark(Mark(p, r = 4, color = cs.GREEN)))
def loadCompletedPatient(patient):
    _auxAddMark(patient.face.upper)
    _auxAddMark(patient.face.chin)
    createVline(Line(patient.face.upper, patient.face.chin, color=cs.LIGHT, w=1))
    _auxAddMark(patient.face.middle)
    _auxAddMark(patient.face.outer_eyeL)
    _auxAddMark(patient.face.inner_eyeL)
    _auxAddMark(patient.face.inner_eyeR)
    _auxAddMark(patient.face.outer_eyeR)
    _auxAddMark(patient.face.cheekboneL)
    _auxAddMark(patient.face.cheekboneR)
    _auxAddMark(patient.face.noseL)
    _auxAddMark(patient.face.noseR)
    _auxAddMark(patient.face.mouthL)
    _auxAddMark(patient.face.mouthR)
    _auxAddMark(patient.face.cheekL)
    _auxAddMark(patient.face.cheekR)            
    return processFullPatient(patient)

def addMeasures(patient):
    global measures
    for line in patient.measurements.getLines(patient.face, color = cs.GREEN, width = 2):
        measures.append(create_line(line))

def addAngles(patient):
    global angles
    for line in patient.angles.getLines(patient.face, color = cs.BLUE, width = 2):
        angles.append(create_line(line))    

def processMove(p, pos):
    x = Order.getPos(pos)
    if x == Order.HORIZONTAL_LINE:
        if len(guideline) == 0:
            createGuideline(Line(Point(p.x, rect.top), Point(p.x, rect.bottom), color = cs.RED))
        screen.coords(guideline[0], p.x, rect.top, p.x, rect.bottom)

    
def processClick(event, point, pos):
    return getFacepos(point, pos)


def toggleAngles():
    global showAngles, screen
    showAngles = showAnglesUI.get()
    print(showAngles)
    if not showAngles:
        for angle in angles:
            screen.itemconfig(angle, state="hidden")
    else:
        
        for angle in angles:
            screen.itemconfig(angle, state="normal")

def toggleMeasures():
    global showMeasures, screen
    showMeasures = showMeasuresUI.get()
    if not showMeasures:
        for measure in measures:
            screen.itemconfig(measure, state="hidden")
    else:
        
        for measure in measures:
            screen.itemconfig(measure, state="normal")
                        

def completeWorkspace(patient):
    global complete
    addMeasures(patient)
    addAngles(patient)
    complete = True

def processFullPatient(patient):
    patient.measurements = facial_measures.Measurements()
    patient.angles = facial_measures.Angles()
    patient.measurements.calculate(patient.face)
    patient.angles.calculate(patient.face)
    patient.proportions.calculate(patient.measurements, patient.angles)
    completeWorkspace(patient)
    return patient

def deleteLastMark(pos):
    global complete, screen, marks, measures, angles
    x = Order.getPos(pos - 1)
    if complete:
        for measure in measures:
            screen.delete(measure)
        for angle in angles:
            screen.delete(angle)
        m = marks.pop()
        screen.delete(m)
        measures.clear()
        angles.clear()
        complete = False
    elif x:
        if x == Order.HORIZONTAL_LINE:
            removeGuideline()
        elif x == Order.CHIN:
            removeVline()
            m = marks.pop()
            screen.delete(m)
        else:
            m = marks.pop()
            screen.delete(m)
    
def clean():
    global complete, screen, measures, angles
    removeGuideline()
    removeVline()
    for mark in marks:
        screen.delete(mark)
    for measure in measures:
        screen.delete(measure)
    for angle in angles:
        screen.delete(angle)
    patient.face = Face()
    measures.clear()
    angles.clear()
    complete = False