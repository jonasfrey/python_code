import sys
from PyQt5.QtCore import lowercasebase


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

        self.setLayout(layout)

        print(self.children())


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Window()

    window.show()

    sys.exit(app.exec_())