
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

class DrawingWidget(Widget):
    def __init__(self):
        super(DrawingWidget, self).__init__()

        with self.canvas:
            
            print("asdf")
            r = Rectangle(size=(300, 100),
                      pos=(300, 200))


    def update_rectangle(self, instance, value):
        print("asdf")

        self.rect.pos = self.pos
        self.rect.size = self.size


class DrawingApp(App):

    def build(self):
        print("asdf")

        root_widget = DrawingWidget()
        return root_widget

    def update(self, *args):
        print("aasdf asdf asdf asdf")

asdf = DrawingApp().run()
