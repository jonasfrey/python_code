import PySimpleGUI as sg
import sys 
import time

class PySimpleGUI_Printer:
    def __init__(self):
        self.i = 0
        self.width = 22
        self.height = 22
        self.font_scale = 10
        self.text = ""
        self.padding = 10
        self.size = ((self.font_scale+self.padding)* self.width,(self.font_scale+self.padding)* self.height)
        self.event = "__TIMEOUT__"
        self.value = None
        self.window_title = "pysimplegui_printer.window_title"
        self.render_id = 0
        # layout the form
        self.layout = [
            [
                sg.Text(
                    'A custom progress meter',
                    key='text',
                    size=self.size, 
                    font=("Helvetica", self.font_scale)
                )
            ],
            [
                sg.Cancel()
            ]
        ]

        # create the form
        self.window = sg.Window('Custom Progress Meter', size=self.size).Layout(self.layout)
        self.sg_text = self.window.FindElement('text')
        # loop that would normally do something useful

    def print(self, text):
        
        self.text = text
        # check to see if the cancel button was clicked and exit loop if clicked
        
        self.event, self.value = self.window.read(timeout=0)
        self.render_id += 1
        #print(self.event)
        # update bar with loop value +1 so that bar eventually reaches the maximum
        #self.progress_bar.UpdateBar(self.i+1, 10000)
        self.sg_text.update(self.text)

        self.window.TKroot.title(self.window_title)



cm = PySimpleGUI_Printer()

test_array = [
    "🌑",
    "❓",
"🌕",
"🌝",
"🌝",
"🌝",
"🌕",
"🌕",
"🍄",
"🐢",
"🔄",
#"🧱",
"💨",
#"🤡",
"🐉",
"💫",
"💱",
"🔫",
"🍏",
"🍏",
#"🏐",
"👄",
"🍏",
"🌑"]
i = 0
if len(sys.argv) > 1:
    lasdf = 16
    for value in range(0, 10000):
        i+=1
        string = ""
        lasdf = ((value+2) % 32) + 2
        for val in range(0, lasdf):

            time.sleep(0.01)
            string_list = list("⬛".join([""]*lasdf))
            #print("000"+hex(127815+val).split('x')[-1])
            #print(chr(127815+i))
            #string_list[((value+val)%lasdf-1)] = chr(127815+i)
            #string_string = ''.join(string_list)
            string_string = test_array[(i)%(len(test_array)-1)]
            string += "\n"+string_string
        #print(string_string)

        cm.print(string)
        print(string)


