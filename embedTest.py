import tkinter as tk
from PIL.ImageTk import PhotoImage

root = tk.Tk()
embed = tk.Frame(root, width = 500, height = 500) #creates embed frame for pygame window
embed.grid(columnspan = (600), rowspan = 500) # Adds grid
embed.pack(side = tk.LEFT) #packs window to the left
buttonwin = tk.Frame(root, width = 75, height = 500)
buttonwin.pack(side = tk.LEFT)

w = tk.Canvas(root, width=200, height=100)
w.pack()

w.create_line(0, 0, 200, 100)
w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

i = w.create_rectangle(50, 25, 150, 75, fill="blue")
w.one = PhotoImage(file="images/reference.jpeg")
i = w.create_image(0, 0, image=w.one, state="normal") 

tk.mainloop()