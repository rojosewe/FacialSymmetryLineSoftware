'''
Created on 17 Apr 2017

@author: rweffercifue
'''

from geometry import Rect
from facial_measures import Face, frontal_face_order
from geometry import Point, Line, Mark, distance
from utils import colors as cs
import facial_measures
from PIL import Image
from PIL.ImageTk import PhotoImage
from workAreas.state_manager import get_patient
from facial_measures.frontal_face_order import get_next, is_completed, delete_last_processed, delete_all_processed, \
    add_to_processed, is_empty

max_v = 700
MIN_DIST = 20

screen = None
rect = None
patient = None
showLowerMeasuresUI = True
showLowerAnglesUI = True
showLowerMeasures = True
showLowerAngles = True
showUpperMeasuresUI = True
showMalarMeasuresUI = True
showUpperAnglesUI = True
showUpperMeasures = True
showUpperAngles = True
showMalarMeasures = True
guideline = []
vline = []
img_obj = None

green_marks = []
imaginary_marks = []
upperMeasures = []
upperAngles = []
lowerMeasures = []
lowerAngles = []
malarMeasures = []

pixel_points = []


def init():
    global patient, showMeasures, showAngles
    patient = get_patient()
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
    complete_visuals_if_patient_is_completed(patient)
                
def inBox(p):
    return p.x >= rect.left and p.x < rect.right and p.y >= rect.top and p.y < rect.bottom
    
def create_line(line):
    return screen.create_line(line.p1.x, line.p1.y, 
                              line.p2.x, line.p2.y, fill=line.color, width=line.w)

def createVline(line):
    vline.append(create_line(line))
    
def removeVline():
    global screen
    while len(vline) > 0:
        screen.delete(vline.pop())
    
def create_mark(mark):
    return screen.create_oval(mark.p.x - mark.r, mark.p.y - mark.r, mark.p.x + mark.r, 
                              mark.p.y + mark.r, fill=mark.color)
  
def assign_point_to_face_pos_and_return_if_completed(p):
    complete_before = is_completed()
    x = get_next()
    if inBox(p) and x and not checkForTooCloseNeightbors(p):
        if x == frontal_face_order.HORIZONTAL_LINE:
            createGuideline(Line(Point(p.x, rect.top), Point(p.x, rect.bottom), color = cs.RED))
        elif x == frontal_face_order.TOP_HEAD:
            patient.face.upper = p
        elif x == frontal_face_order.CHIN:
            patient.face.chin = p
            createVline(Line(patient.face.upper, patient.face.chin, color=cs.LIGHT, w=1))
        elif x == frontal_face_order.FOREHEAD:
            patient.face.middle = p
        elif x == frontal_face_order.EYE_OUTER_LEFT:
            patient.face.outer_eyeL = p
        elif x == frontal_face_order.EYE_INNER_LEFT:
            patient.face.inner_eyeL = p
        elif x == frontal_face_order.EYE_INNER_RIGHT:
            patient.face.inner_eyeR = p
        elif x == frontal_face_order.EYE_OUTER_RIGHT:
            patient.face.outer_eyeR = p
        elif x == frontal_face_order.CHEEKBONE_LEFT:
            patient.face.cheekboneL = p
        elif x == frontal_face_order.CHEEKBONE_RIGHT:
            patient.face.cheekboneR = p
        elif x == frontal_face_order.NOSE_LEFT:
            patient.face.noseL = p
        elif x == frontal_face_order.NOSE_CENTER:
            patient.face.noseC = p
        elif x == frontal_face_order.NOSE_RIGHT:
            patient.face.noseR = p
        elif x == frontal_face_order.MOUTH_LEFT:
            patient.face.mouthL = p
        elif x == frontal_face_order.MOUTH_RIGHT:
            patient.face.mouthR = p
        elif x == frontal_face_order.CHEEK_LEFT:
            patient.face.cheekL = p
        elif x == frontal_face_order.CHEEK_RIGHT:
            patient.face.cheekR = p
            _auxAddMark(p)
        if not frontal_face_order.is_empty():
            _auxAddMark(p)
        add_to_processed(x)
    complete_now = is_completed()
    if complete_now and not complete_before:
        return True
    else:
        return False


def createGuideline(line):
    guideline.append(create_line(line))


def removeGuideline():
    global screen
    while len(guideline) > 0:
        screen.delete(guideline.pop())


def checkForTooCloseNeightbors(p):
    for p1 in pixel_points:
        if _check_distance(p1, p) < MIN_DIST:
            return True
    return False


def _check_distance(p1, p2):
    if p1 is not None and p2 is not None:
        return distance(p1, p2)
    else:
        return True


def complete_visuals_if_patient_is_completed(patient):
    if is_completed():
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
        _auxAddMark(patient.face.noseC)
        _auxAddMark(patient.face.noseR)
        _auxAddMark(patient.face.mouthL)
        _auxAddMark(patient.face.mouthR)
        _auxAddMark(patient.face.cheekL)
        _auxAddMark(patient.face.cheekR)
        processFullPatient(patient)


def _auxAddMark(p):
    green_marks.append(create_mark(Mark(p, r=4, color=cs.GREEN)))
    pixel_points.append(p)

def addMeasures(patient):
    global lowerMeasures, upperMeasures
    um, lm, ml = patient.measurements.getLines(patient.face, color = cs.GREEN, width = 2)
    for line in um:
        upperMeasures.append(create_line(line))
    for line in lm:
        lowerMeasures.append(create_line(line))
    for line in ml:
        malarMeasures.append(create_line(line))
    toggleLowerMeasures()
    toggleUpperMeasures()
    toggleMalarMeasures()
    
def addImaginaryMarks(patient):
    imaginary_marks.append(create_mark(Mark(patient.face.malarL, r = 4, color = cs.GREEN)))
    imaginary_marks.append(create_mark(Mark(patient.face.malarR, r = 4, color = cs.GREEN)))

def addAngles(patient):
    global lowerAngles, upperAngles
    ua, la = patient.angles.getLines(patient.face, color = cs.BLUE, width = 2)
    for line in ua:
        upperAngles.append(create_line(line))
    for line in la:
        lowerAngles.append(create_line(line))
    toggleLowerAngles()
    toggleUpperAngles()


def processMove(p):
    x = get_next()
    if x == frontal_face_order.HORIZONTAL_LINE:
        if len(guideline) == 0:
            createGuideline(Line(Point(p.x, rect.top), Point(p.x, rect.bottom), color = cs.RED))
        screen.coords(guideline[0], p.x, rect.top, p.x, rect.bottom)

    
def process_click_return_if_completed(event, point):
    completed_now = assign_point_to_face_pos_and_return_if_completed(point)
    if completed_now:
        processFullPatient(patient)
    return completed_now


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

def toggleMalarMeasures():
    global showMalarMeasures, showMalarMeasuresUI, malarMeasures, screen
    showMalarMeasures = showMalarMeasuresUI.get()
    for measure in malarMeasures:
        if not showMalarMeasures:
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
    addMeasures(patient)
    addAngles(patient)
    addImaginaryMarks(patient)

def processFullPatient(patient):
    patient.measurements = facial_measures.Measurements()
    patient.angles = facial_measures.Angles()
    patient.face.calculate_additional()
    patient.measurements.calculate(patient.face)
    patient.angles.calculate(patient.face)
    patient.proportions.calculate(patient.measurements, patient.angles)
    completeWorkspace(patient)
    return patient


def undo_previous_action():
    global screen, lowerMeasures, upperMeasures, lowerAngles, upperAngles
    if is_completed():
        _delete_last_mark()
        delete_last_processed()
        delete_measures_andImaginary_marks(lowerAngles, lowerMeasures, screen, upperAngles, upperMeasures)
    elif not is_empty():
        delete_last_processed()
        x = get_next()
        if is_empty():
            removeGuideline()
        else:
            _delete_last_mark()
        if x == frontal_face_order.CHIN:
            removeVline()


def clean():
    global screen, green_marks, lowerAngles, upperAngles, lowerMeasures, upperMeasures
    delete_measures_andImaginary_marks(lowerAngles, lowerMeasures, screen, upperAngles, upperMeasures)
    for i in range(len(green_marks)):
        _delete_last_mark()
    delete_all_processed()
    removeGuideline()
    removeVline()
    patient.face = Face()


def delete_measures_andImaginary_marks(lowerAngles, lowerMeasures, screen, upperAngles, upperMeasures):
    for measure in upperMeasures:
        screen.delete(measure)
    for measure in lowerMeasures:
        screen.delete(measure)
    for measure in malarMeasures:
        screen.delete(measure)
    for angle in upperAngles:
        screen.delete(angle)
    for angle in lowerAngles:
        screen.delete(angle)
    for p in imaginary_marks:
        screen.delete(p)
    lowerMeasures.clear()
    upperMeasures.clear()
    lowerAngles.clear()
    upperAngles.clear()
    imaginary_marks.clear()


def _delete_last_mark():
    global pixel_points, green_marks
    if len(green_marks) == 0:
        return None
    pixel_points.pop()
    m = green_marks.pop()
    screen.delete(m)


def restart():
    clean()
