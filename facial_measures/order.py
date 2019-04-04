'''
Created on 17 Apr 2017

@author: rweffercifue
'''


class Order:

    @classmethod
    def get_next(cls):
        if cls.is_completed():
            return None
        else:
            return cls.to_process[0]

    @classmethod
    def add_to_processed(cls, point):
        if point in cls.to_process:
            cls.to_process.remove(point)
            if point not in cls.processed:
                cls.processed.append(point)

    @classmethod
    def delete_last_processed(cls):
        if not cls.is_empty():
            cls.to_process.insert(0, cls.processed.pop())

    @classmethod
    def delete_all_processed(cls):
        cls.to_process = cls.order.copy()
        cls.processed.clear()

    @classmethod
    def start_over(cls):
        cls.to_process = cls.order.copy()
        cls.processed.clear()

    @classmethod
    def is_empty(cls):
        return len(cls.processed) == 0

    @classmethod
    def is_completed(cls):
        return len(cls.to_process) == 0

    @classmethod
    def marked_order_as_completed(cls, patient):
        face_map = cls._return_face_map(patient)
        for o in cls.order:
            face_part = face_map[o]
            if face_part is not None:
                cls.add_to_processed(o)


class AxialOrder(Order):

    POINT_NOSE = "POINT NOSE"
    CENTRAL_POINT = "CENTRAL POINT"
    BREAK_POINT = "BREAK POINT"
    WALL_LEFT = "LEFT NASAL WALL"
    WALL_RIGHT = "RIGHT NASAL WALL"
    MAXILAR_LEFT = "MAXILAR LEFT"
    MAXILAR_RIGHT = "MAXILAR RIGHT"

    order = [CENTRAL_POINT, BREAK_POINT, WALL_RIGHT, WALL_LEFT, MAXILAR_RIGHT, MAXILAR_LEFT, POINT_NOSE]

    to_process = order.copy()
    processed = []

    @classmethod
    def _return_face_map(cls, patient):
        axial = patient.values
        return {
            cls.CENTRAL_POINT: axial.central_point,
            cls.BREAK_POINT: axial.break_point,
            cls.POINT_NOSE: axial.point_nose,
            cls.WALL_LEFT: axial.wall_left,
            cls.WALL_RIGHT: axial.wall_right,
            cls.MAXILAR_RIGHT: axial.maxilar_right,
            cls.MAXILAR_LEFT: axial.maxilar_left
        }

    @classmethod
    def marked_order_as_completed(cls, patient):
        face_map = cls._return_face_map(patient)
        for o in cls.order:
            face_part = face_map[o]
            if face_part is not None:
                cls.add_to_processed(o)


class FrontalOrder(Order):
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

    @classmethod
    def _return_face_map(cls, patient):
        frontal = patient.values
        return {
            cls.TOP_HEAD: frontal.upper,
            cls.CHIN: frontal.chin,
            cls.FOREHEAD: frontal.middle,
            cls.EYE_OUTER_LEFT: frontal.outer_eye.left,
            cls.EYE_INNER_LEFT: frontal.inner_eye.left,
            cls.EYE_INNER_RIGHT: frontal.inner_eye.right,
            cls.EYE_OUTER_RIGHT: frontal.outer_eye.rught,
            cls.CHEEKBONE_LEFT: frontal.cheekbone.left,
            cls.CHEEKBONE_RIGHT: frontal.cheekbone.right,
            cls.NOSE_LEFT: frontal.nose.left,
            cls.NOSE_CENTER: frontal.nose_center,
            cls.NOSE_RIGHT: frontal.nose.right,
            cls.MOUTH_LEFT: frontal.mouth.left,
            cls.MOUTH_RIGHT: frontal.mouth.right,
            cls.CHEEK_LEFT: frontal.cheek.left,
            cls.CHEEK_RIGHT: frontal.cheek.right
        }
