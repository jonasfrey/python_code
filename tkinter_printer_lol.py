# from tkinter import *
# from tkinter import font as tkfont
# import time
# import threading

# class Tkinter_Printer:
#     def __init__(self): 
#         self.background_color = "black"
#         self.size_factor = 20

#         self.root = Tk()
#         self.root.geometry("500x500")
#         self.canvas = Canvas(self.root, width=500, height=500)
#         self.canvas.pack()
#         self.font = tkfont.Font(family="Helvetica", size=self.size_factor, weight="bold")

#         self.render_id = 0
#         self.running = True



#         # self.render_thread = threading.Thread(target=self.render)
#         # self.render_thread.setDaemon(True)
#         # # print "Starting thread"
#         # self.render_thread.start()
#         # # time.sleep(0.1)
#         # # print "Something done"
#         # # t1.join()
#         # # print "Thread Done"


#     # def render(self): 
#     #     while self.running:
#     #         time.sleep(0.005)
#     #         self.render_id += 1
#     #         self.root.update_idletasks()
#     #         self.root.update()

#     def asdf(self, string):
#         print(string)
#         lines_strings_array = string.splitlines()
#         y = 1
#         x = 1
#         for line_string in lines_strings_array:
#             y+= 1
#             line_characters_array = list(line_string)

#             for line_character in line_characters_array:
#                 x+=1
#                 self.canvas.create_text(x*self.size_factor, y*self.size_factor, font=self.font, text=line_character,fill="red")
#                 print(line_character)
        
#         self.root.update_idletasks()
#         self.root.update()
#         self.root.mainloop()

# tkp = Tkinter_Print()
# tkp.asdf("hello world")
# time.sleep(1)
# tkp.asdf("fdsa fasdf")




# Run tkinter code in another thread
#!/usr/bin/env python3

import tkinter as tk
from tkinter import font as tkfont
import threading
import time 

class Tkinter_Printer(threading.Thread):

    def __init__(self):
        #an 2 dimensional array [ [line maybe terminated by \n ], [ char , char, ... ], ...]
        self.lines_array = []
        self.print_text = ""
        self.background_color = "black"
        self.size_factor = 10
        self.window_width = 500
        self.window_height = 500
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        #self.root.protocol("WM_DELETE_WINDOW", self.callback)
        
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height)
        self.canvas.pack()
        self.canvas.create_text(20, 30, font="Arial", text="😃\n😃")
        self.canvas.pack()
        self.font = tkfont.Font(family="Arial", size=self.size_factor)
        self.canvas.bind('<Configure>', self.resize)

        self.renderloop()

    def resize(self, event):
        # print("configure event triggered")
        # print(self.root.winfo_width())
        # print(self.root.winfo_width())
        self.window_width =self.root.winfo_width()
        self.window_height =self.root.winfo_height()

        if (self.window_height > self.window_width):
            square_max_size = self.window_width
        else:
            square_max_size = self.window_width

        #w,h = event.width-100, event.height-100
        #self.canvas.config(width=w, height=h)

    def renderloop(self):
        while True: 
            self.canvas.delete("all")
            #self.canvas.create_text(x*self.size_factor, y*self.size_factor, font=self.font, text=char,fill="red")
            self.canvas.create_text(0, 0,font="Arial",text=self.print_text+"😃\n😃")

            self.root.update_idletasks()
            self.root.update()

    def renderloop_old(self):
        while True: 
            self.canvas.delete("all")
            x = 0
            y = 0
            for chars_array in self.lines_array:
                #a line could possibily  extend the maximum characters per line, so we split the chars_array into multiple by max size !                
                chars_array_lines = list(self.divide_chunks(chars_array, int(self.window_width/(self.size_factor))))

                for chars_array in chars_array_lines: 
                    y+=1
                    x = 0
                    for char in chars_array:
                        x+=1
                        self.canvas.create_text(x*self.size_factor, y*self.size_factor, font=self.font, text=char,fill="red")

            self.root.update_idletasks()
            self.root.update()

    def divide_chunks(self, l, n): 
        
        # looping till length l 
        for i in range(0, len(l), n):  
            yield l[i:i + n] 

    def printit_old(self, string):
        lines_strings_array = string.splitlines()
        
        #split string into lines and then split into characters 
        for line_string in lines_strings_array:
            line_characters_array = list(line_string)
            line_arr = []
            for line_character in line_characters_array:
                line_arr.append(line_character)

            self.lines_array.append(line_arr)

    def printit(self, string): 
        self.print_text = string
                
    def clear(self):
        self.lines_array = []



# usage 
# tkp = Tkinter_Printer()

# # tkp.printit('Now we can continue running code while mainloop runs!')
# print('Now we can continue running code while mainloop runs!')

# for i in range(1000):
#     time.sleep(0.01)
#     tkp.clear()
#     tkp.printit("A".join([""]*i)+'yess!: '+str(i))
#     #print(i)