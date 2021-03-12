#!/usr/bin/env python3

"""
ZetCode Tkinter tutorial

In this script, we draw text
on the window.

Author: Jan Bodnar
Website: www.zetcode.com
"""

from tkinter import Tk, Canvas, Frame, BOTH, W
import tkinter as tk
import pyglet, os

pyglet.font.add_file('./OpenSansEmoji.ttf')  #


# def main():

#     root = Tk()

#     canvas = Canvas(root)
#     root.geometry("1000x1000")
import tkinter as tk


# if __name__ == '__main__':
#     main()


root = tk.Tk()
MyLabel = tk.Label(root,text="⊛",font=('OpenSansEmoji',22)) 

# although vera is one of the in built fonts but pyglet worked for me with all the 
# font files

MyLabel.pack()
root.mainloop()