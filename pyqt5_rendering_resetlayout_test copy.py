import sys
from PyQt5.QtCore import lowercasebase
import random
import time

from PyQt5.QtWidgets import (

    QApplication,

    QHBoxLayout,
    QLabel,

    QPushButton,
    QVBoxLayout,

    QWidget,

)


class Window(QWidget):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("QHBoxLayout Example")
        self.datanum = 0

        self.render_widget = QWidget()
        self.layout = QHBoxLayout()
        # self.render_widget.setLayout(self.layout)
        # self.layout.addWidget(self.render_widget)
        self.render_layout = QHBoxLayout()
        self.layout.addLayout(self.render_layout)
        self.render_render_layout()
        self.setLayout(self.layout)



    def butnclick(self):
        self.datanum = self.datanum + 1
        self.render_render_layout()
        
    def reset_layout(self):
        for i in reversed(range(self.render_layout.count())): 
            self.render_layout.itemAt(i).widget().setParent(None)
        self.layout.removeItem(self.render_layout)

    def render_render_layout(self):
        self.reset_layout()
        self.render_layout = QHBoxLayout()

        self.pushButton = QPushButton('datanum'+str(self.datanum), self)
        self.pushButton.clicked.connect(self.butnclick)
        self.render_layout.addWidget(self.pushButton)
        
        
        self.layout.addLayout(self.render_layout)



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Window()

    window.show()

    sys.exit(app.exec_())