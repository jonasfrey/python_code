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

import tkinter as tk
from tkinter import font as tkfont
import threading
import time 

class Tkinter_Printer(threading.Thread):

    def __init__(self):
        #an 2 dimensional array [ [line maybe terminated by \n ], [ char , char, ... ], ...]
        self.lines_array = []
        self.background_color = "black"
        self.size_factor = 20



        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        self.font = tkfont.Font(family="Helvetica", size=self.size_factor, weight="bold")


        self.renderloop()


    def renderloop(self):
        while True: 
            x = 0
            y = 0
            for val in self.lines_array:
                y+=1
                for char in val:
                    x+=1
                    self.canvas.delete("all")
                    self.canvas.create_text(x*self.size_factor, y*self.size_factor, font=self.font, text=char,fill="red")

            self.root.update_idletasks()
            self.root.update()

    def printit(self, string):
        lines_strings_array = string.splitlines()

        #split string into lines and then split into characters 
        for line_string in lines_strings_array:
            line_characters_array = list(line_string)
            for line_character in line_characters_array:
                self.lines_array.append(line_character)
                
    def clear(self):
        self.lines_array = []




tkp = Tkinter_Printer()

tkp.printit('Now we can continue running code while mainloop runs!')

for i in range(1000):
    time.sleep(0.01)
    tkp.printit('yess!: '+str(i))
    print(i)