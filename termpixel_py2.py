from termpixels import App, Color
from time import time
from math import sin

class FunTextApp(App):
    def on_frame(self):
        self.screen.clear()                           # remove everything from the screen
        self.screen.print("test", 0, 0)
        self.screen.print("test", 1, 1)

        self.screen.update()                          # commit the changes to the screen

if __name__ == "__main__":
    FunTextApp().start()