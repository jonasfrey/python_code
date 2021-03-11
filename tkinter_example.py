from tkinter import *
from tkinter import font as tkfont
import time
root = Tk()
root.geometry("500x900")

canvas = Canvas(root, width=250, height=200)
canvas.pack()

i = 0
while i < 1000:
    print(i)
    canvas.delete("all")
    canvas.create_rectangle(i, 0, 100, 100, fill="black", outline = 'black')
    i+= 1
    helvetica_bold = tkfont.Font(family="Helvetica", size=12, weight="bold")
    canvas.create_text(i, 30, anchor=W, font=helvetica_bold, text=u'\uf911',		 fill="white")
    root.update_idletasks()
    root.update()
    time.sleep(0.1)