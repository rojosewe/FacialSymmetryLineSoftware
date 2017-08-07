'''
Created on 17 Apr 2017

@author: rweffercifue
'''

from geometry import Rect
from facial_measures import Face, Order
from geometry import Point, Line, Mark, distance
from utils import colors as cs
from utils import Commands
import facial_measures
from PIL import Image
from PIL.ImageTk import PhotoImage

max_v = 700
MIN_DIST = 20

complete = False
screen = None
rect = None
patient = None
showLowerMeasuresUI = True
showLowerAnglesUI = True
showLowerMeasures = True
showLowerAngles = True
showUpperMeasuresUI = True
showUpperAnglesUI = True
showUpperMeasures = True
showUpperAngles = True
guideline = []
vline = []
marks = []
img_obj = None
upperMeasures = []
upperAngles = []
lowerMeasures = []
lowerAngles = []
geopoints = []


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
    
def _check_distance(p1, p2):
    if p1 is not None and p2 is not None:
        return distance(p1, p2)
    else:
        return True    

def checkForTooCloseNeightbors(p):
    for p1 in geopoints:
        if _check_distance(p1, p) < MIN_DIST:
            return True
    return False
  
def getFacepos(p, pos):
    global complete
    if inBox(p):
        x = Order.getPos(pos)
        if x:
            if checkForTooCloseNeightbors(p):
                return Commands.REPEAT

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
    geopoints.append(p)

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
    global lowerMeasures, upperMeasures
    um, lm = patient.measurements.getLines(patient.face, color = cs.GREEN, width = 2)
    for line in um:
        upperMeasures.append(create_line(line))
    for line in lm:
        lowerMeasures.append(create_line(line))

def addAngles(patient):
    global lowerAngles, upperAngles
    ua, la = patient.angles.getLines(patient.face, color = cs.BLUE, width = 2)
    for line in ua:
        upperAngles.append(create_line(line))
    for line in la:
        lowerAngles.append(create_line(line))

def processMove(p, pos):
    x = Order.getPos(pos)
    if x == Order.HORIZONTAL_LINE:
        if len(guideline) == 0:
            createGuideline(Line(Point(p.x, rect.top), Point(p.x, rect.bottom), color = cs.RED))
        screen.coords(guideline[0], p.x, rect.top, p.x, rect.bottom)

    
def processClick(event, point, pos):
    return getFacepos(point, pos)


def toggleUpperAngles():
    global showUpperAngles, showUpperAnglesUI, upperAngles, screen
    showUpperAngles = showUpperAnglesUI.get()
    print(showUpperAngles)
    for angle in upperAngles:
        if not showUpperAngles:
            screen.itemconfig(angle, state="hidden")
        else:
            screen.itemconfig(angle, state="normal")

def toggleUpperMeasures():
    global showUpperMeasures, showUpperMeasuresUI, upperMeasures, screen
    showUpperMeasures = showUpperMeasuresUI.get()
    for measure in upperMeasures:
        if not showUpperMeasures:
            screen.itemconfig(measure, state="hidden")
        else:
            screen.itemconfig(measure, state="normal")


def toggleLowerAngles():
    global showLowerAngles, showLowerAnglesUI, lowerAngles, screen
    showLowerAngles = showLowerAnglesUI.get()
    print(showLowerAngles)
    for angle in lowerAngles:
        if not showLowerAngles:
            screen.itemconfig(angle, state="hidden")
        else:
            screen.itemconfig(angle, state="normal")

def toggleLowerMeasures():
    global showLowerMeasures, showLowerMeasuresUI, lowerMeasures, screen
    showLowerMeasures = showLowerMeasuresUI.get()
    for measure in lowerMeasures:
        if not showLowerMeasures:
            screen.itemconfig(measure, state="hidden")
        else:
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

def _auxPopMark():
    global geopoints, marks
    if len(marks) == 0:
        return None
    geopoints.pop()
    return marks.pop()

def deleteLastMark(pos):
    global complete, screen, lowerMeasures, upperMeasures, lowerAngles, upperAngles
    x = Order.getPos(pos - 1)
    if complete:
        for measure in upperMeasures:
            screen.delete(measure)
        for measure in lowerMeasures:
            screen.delete(measure)
        for angle in upperAngles:
            screen.delete(angle)
        for angle in lowerAngles:
            screen.delete(angle)
        m = _auxPopMark()
        screen.delete(m)
        lowerMeasures.clear()
        upperMeasures.clear()
        lowerAngles.clear()
        upperAngles.clear()
        complete = False
    elif x:
        if x == Order.HORIZONTAL_LINE:
            removeGuideline()
        elif x == Order.CHIN:
            removeVline()
            m = _auxPopMark()
            screen.delete(m)
        else:
            m = _auxPopMark()
            screen.delete(m)
    
def clean():
    global complete, screen, marks, lowerAngles, upperAngles, lowerMeasures, upperMeasures
    removeGuideline()
    removeVline()
    for i in range(len(marks)):
        m = _auxPopMark()
        screen.delete(m)
    for measure in lowerMeasures:
        screen.delete(measure)
    for measure in upperMeasures:
        screen.delete(measure)
    for angle in lowerAngles:
        screen.delete(angle)
    for angle in upperAngles:
        screen.delete(angle)
    patient.face = Face()
    lowerAngles.clear()
    upperAngles.clear()
    lowerMeasures.clear()
    upperMeasures.clear()
    complete = False
