# Run tkinter code in another thread

import tkinter as tk
import threading
import time 

class App(threading.Thread):

    def __init__(self):
        self.num = 0
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        
        self.string_var = tk.StringVar()
        self.string_var.set(str(self.num))

        label = tk.Label(self.root, textvariable=self.string_var)
        label.pack()

        self.renderloop()

    def renderloop(self):
        while True: 
            self.string_var.set(str(self.num))
            self.root.update_idletasks()
            self.root.update()



app = App()

print('Now we can continue running code while mainloop runs!')

for i in range(1000):
    time.sleep(0.01)
    app.num = i
    print(i)