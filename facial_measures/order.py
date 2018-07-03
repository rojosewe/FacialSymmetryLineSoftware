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


class AxialOrder(Order):

    POINT_NOSE = "POINT NOSE"
    CENTRAL_POINT = "CENTRAL POINT"
    BREAK_POINT = "BREAK POINT"
    WALL_LEFT = "LEFT NASAL WALL"
    WALL_RIGHT = "RIGHT NASAL WALL"

    order = [CENTRAL_POINT, POINT_NOSE, BREAK_POINT, WALL_LEFT, WALL_RIGHT]

    to_process = order.copy()
    processed = []

    @classmethod
    def _return_face_map(cls, patient):
        axial = patient.axial
        return {
            cls.CENTRAL_POINT: axial.central_point,
            cls.BREAK_POINT: axial.break_point,
            cls.POINT_NOSE: axial.point_nose,
            cls.WALL_LEFT: axial.wall_left,
            cls.WALL_RIGHT: axial.wall_right
        }

    @classmethod
    def marked_order_as_completed(cls, patient):
        face_map = cls._return_face_map(patient)
        for o in cls.order:
            face_part = face_map[o]
            if face_part is not None:
                cls.add_to_processed(o)



