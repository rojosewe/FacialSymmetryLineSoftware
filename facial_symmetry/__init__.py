import tkinter
from PIL import Image, ImageTk, ImageDraw

points = []

window = tkinter.Tk(className="Test")
im = Image.open("../Pics/pic.jpg")
canvas = tkinter.Canvas(window, width=im.size[0], height=im.size[1])
canvas.pack()
imTk = ImageTk.PhotoImage(im)
canvas.create_image(im.size[0]//2, im.size[1]//2, image=imTk)
draw = ImageDraw.Draw(im)

def reset():
    global points, im, imTk, draw, canvas
    im = Image.open("../Pics/pic.jpg")
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
            
canvas.bind("<Button-1>", callback)
canvas.bind_all('<r>', resetFn) 
canvas.bind_all('<d>', delete) 
tkinter.mainloop()

