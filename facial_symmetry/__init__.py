import tkinter
from PIL import Image, ImageTk, ImageDraw
from  tkinter import filedialog
import easygui
from easygui.boxes.derived_boxes import msgbox

points = []

# fnm = filedialog.askopenfilename()
default = "/home/rojosewe/Pictures/"
fnm = easygui.fileopenbox(msg="Abre la foto", default=default)
window = tkinter.Tk(className="Test")
im = Image.open(fnm)
canvas = tkinter.Canvas(window, width=im.size[0], height=im.size[1])
canvas.pack()
imTk = ImageTk.PhotoImage(im)
canvas.create_image(im.size[0]//2, im.size[1]//2, image=imTk)
draw = ImageDraw.Draw(im)

def openNewFile(event):
    global fnm, default
    fnm = easygui.fileopenbox(msg="Abre la foto", default=default)
    reset()

def reset():
    global points, im, imTk, draw, canvas, fnm
    im = Image.open(fnm)
    imTk = ImageTk.PhotoImage(im)
    canvas.create_image(im.size[0] // 2, im.size[1] // 2, image=imTk)
    draw = ImageDraw.Draw(im)

def resetFn(event):
    global points, im, imTk, draw, canvas
    reset()
    points = []

def delete(event):
    global points, im, imTk, draw, canvas
    reset()
    if len(points) <= 2:
        points = []
    else:
        del points[-1]
        del points[-1]
    px = None
    for point in points:
        if px is None:
            px = point
        else:
            drawHorizontal(px, point)
            px = None

def drawHorizontal(p1, p2):
    global points, im, imTk, draw, canvas
    draw.line((p1[0], p1[1], p2[0], p2[1]), fill=128, width=3)
    print("drew line %s, %s " % (p1, p2))
    imTk = ImageTk.PhotoImage(im)
    canvas.create_image(im.size[0] // 2, im.size[1] // 2, image=imTk)

def drawAllPoints(points):
    print(points)
    n = len(points)
    if (n > 0):
        if (n % 2 == 0):
            p1 = points[n - 1]
            p2 = points[n - 2]
            drawHorizontal(p1, p2)

def addPoint(x, y):
    global points, im, imTk, draw, canvas
    points.append((x, y))
    drawAllPoints(points)

def callback(event):
    global im, imTk, draw
    addPoint(event.x, event.y)
    
def calculateProportions(event):
    global points
    if(len(points) != 6):
        msgbox("Tienen que haber 6 puntos.")
    else:
        msgbox("Las proporciones son estas")
        
def showhelp(event):
    msgbox("""
    - Click: Pones un punto en la cara.\n
    - r: Borras todas las lineas.\n
    - d: Borras la ultima linea.\n
    - o: Abre una foto nueva.\n
    - p: Sacas las proporciones.\n
    - h: Ayuda.\n
    """)    
            
canvas.bind("<Button-1>", callback)
canvas.bind_all('<r>', resetFn) 
canvas.bind_all('<d>', delete) 
canvas.bind_all('<o>', openNewFile)
canvas.bind_all('<p>', calculateProportions)
canvas.bind_all('<h>', showhelp)
tkinter.mainloop()

