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

x = w.create_line(0, 0, 200, 100)
w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

w.delete(x)
tk.mainloop()