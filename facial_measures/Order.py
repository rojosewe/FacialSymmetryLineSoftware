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
NOSE_RIGHT = "RIGHT NOSE"
MOUTH_LEFT = "LEFT MOUTH"
MOUTH_RIGHT = "RIGHT MOUTH"
CHEEK_LEFT = "LEFT CHEEK"
CHEEK_RIGHT = "RIGHT CHEEK"

order = [HORIZONTAL_LINE, TOP_HEAD, CHIN, FOREHEAD, 
EYE_OUTER_LEFT, EYE_INNER_LEFT, EYE_INNER_RIGHT, EYE_OUTER_RIGHT, 
CHEEKBONE_LEFT, CHEEKBONE_RIGHT, NOSE_LEFT,
NOSE_RIGHT, MOUTH_LEFT, MOUTH_RIGHT, CHEEK_LEFT, CHEEK_RIGHT]

def getPos(pos):
    if pos < len(order) and pos >= 0:
        return order[pos]
    else:
        return None