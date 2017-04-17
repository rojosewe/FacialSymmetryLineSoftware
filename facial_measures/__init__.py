
def Patient(name, photo, face=None):
    name = name
    photo = photo
    face = face

class Face():
    
    def __init__(self):
        self.middle = None
        self.upper = None
        self.chin = None
        self.cheekboneL = None
        self.cheekboneR = None
        self.cheekL = None
        self.cheekR = None
        self.mouthL = None
        self.mouthR = None
        self.noseL = None
        self.noseR = None
        self.outer_eyeL = None
        self.inner_eyeL = None
        self.outer_eyeR = None
        self.inner_eyeR = None

class Horizontal():
    
    def __init__(self):
        self.left_eye = None
        self.right_eye = None
        self.bridge = None
        self.nose = None
        self.mouth = None
        self.chin = None