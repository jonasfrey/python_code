import sys
from PyQt5.QtCore import lowercasebase
import random

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

        # Create a QHBoxLayout instance

        layout = QHBoxLayout()
        l = QVBoxLayout()

        layout.addLayout(l)

        # Add widgets to the layout

        label = QLabel('asdf')
        l.addWidget(label)

        l.addWidget(label, 1)

        l.addWidget(label, 2)
        #unfortunately we cannot have the same qobject at multiple places...

        # Set the layout on the application's window

        pyqt5_layoutouter = QHBoxLayout()

        layout.addLayout(pyqt5_layoutouter)
        qw = QWidget()
        pyqt5_layoutouter.addWidget(qw)
        pyqt5_layoutinner = QHBoxLayout()
        qw.setLayout(pyqt5_layoutinner)

        r = lambda: random.randint(0,255)
        rc = ('#%02X%02X%02X' % (r(),r(),r()))
        label = QLabel(rc)
        qw.setStyleSheet('background-color: '+rc)
        pyqt5_layoutinner.addWidget(label)
        self.setLayout(layout)



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Window()

    window.show()

    sys.exit(app.exec_())