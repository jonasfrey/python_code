from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

import time
from multiprocessing import Process

f = open("demofile2.txt", "w")
f.write("Woops! I have deleted the content!")
f.close()


class IncrediblyCrudeClock(Label):

    def update(self, *args):

        f = open("demofile2.txt", "r")
        te = f.read()

        self.text = te + str(time.time() * 1000)

class TimeApp(App):
    def build(self):
        crudeclock = IncrediblyCrudeClock()
        Clock.schedule_interval(crudeclock.update, 0.1)
        return crudeclock



def loop_b():

    if __name__ == "__main__":

        TimeApp().run()



def loop_a():
    i = 0

    while 1:
        i+= 1
        time.sleep(0.016)
        f = open("demofile2.txt", "w")
        f.write(str(i) + "asdf asdf")
        f.close()

        #text_global = str("test "+ str(i) + " end text")
        if(i ==  100):
            Process(target=loop_b).start()

if __name__ == '__main__':
    Process(target=loop_a).start()