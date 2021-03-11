from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
import sys



App = QApplication(sys.argv)
qmw = QMainWindow()
qmw.title = "PyQt5 Drawing Rectangle"
qmw.top = 100
qmw.left = 100
qmw.width = 680
qmw.height = 500
qmw.setWindowIcon(QtGui.QIcon("icon.png"))
qmw.setWindowTitle(qmw.title)
qmw.setGeometry(qmw.top, qmw.left, qmw.width, qmw.height)
qmw.show()


painter = QPainter(qmw)
painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
#painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
painter.setBrush(QBrush(Qt.green, Qt.DiagCrossPattern))

painter.drawRect(100, 15, 300,200)



sys.exit(App.exec())
