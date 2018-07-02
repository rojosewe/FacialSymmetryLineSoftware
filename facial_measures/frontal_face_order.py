'''
Created on 17 Apr 2017

@author: rweffercifue
'''


HORIZONTAL_LINE = "HORIZONTAL LINE"
TOP_HEAD = "TOP HEAD"
CHIN = "CHIN"
FOREHEAD = "FOREHEAD"
EYE_OUTER_LEFT = "LEFT OUTER EYE"
EYE_INNER_LEFT = "LEFT INNER EYE"
EYE_INNER_RIGHT = "RIGHT INNER EYE"
EYE_OUTER_RIGHT = "RIGHT OUTER EYE"
CHEEKBONE_LEFT = "LEFT CHEEK BONE"
CHEEKBONE_RIGHT = "RIGHT CHEEK BONE"
NOSE_LEFT = "LEFT NOSE"
NOSE_CENTER = "CENTER NOSE"
NOSE_RIGHT = "RIGHT NOSE"
MOUTH_LEFT = "LEFT MOUTH"
MOUTH_RIGHT = "RIGHT MOUTH"
CHEEK_LEFT = "LEFT CHEEK"
CHEEK_RIGHT = "RIGHT CHEEK"

order = [HORIZONTAL_LINE, TOP_HEAD, CHIN, FOREHEAD, 
EYE_OUTER_LEFT, EYE_INNER_LEFT, EYE_INNER_RIGHT, EYE_OUTER_RIGHT, 
CHEEKBONE_LEFT, CHEEKBONE_RIGHT, NOSE_LEFT,
NOSE_CENTER, NOSE_RIGHT, MOUTH_LEFT, MOUTH_RIGHT, CHEEK_LEFT, CHEEK_RIGHT]

to_process = order.copy()
processed = []

def get_next():
    if is_completed():
        return None
    else:
        return to_process[0]


def add_to_processed(point):
    to_process.remove(point)
    if point not in processed:
        processed.append(point)
    p()


def delete_last_processed():
    to_process.insert(0, processed.pop())
    p()


def delete_all_processed():
    global to_process
    to_process = order.copy()
    processed.clear()
    p()

def start_over():
    global to_process
    to_process = order.copy()
    processed.clear()
    p()


def is_empty():
    p()
    return len(processed) == 0


def is_completed():
    return len(to_process) == 0

def p():
    print("to process: %s " % to_process)
    print("processed: %s " % processed)