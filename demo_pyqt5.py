import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QApplication,QLineEdit, QLabel, QVBoxLayout, QPushButton, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import forcepoint, pyqtSignal, pyqtSlot, Qt, QThread

def window():
    app = QApplication(sys.argv)
    q_main_widget = QWidget() 

    # test_layout_widget_parent_child_behaviour(q_main_widget)
    # test_widget_set_two_layouts(q_main_widget)
    test_layout_set_two_layouts(q_main_widget)

    q_main_widget.setWindowTitle("QLabel Demo")
    q_main_widget.show()
    sys.exit(app.exec_())

def test_widget_set_two_layouts(q_main_widget):
    l1 = QVBoxLayout()    
    l2 = QVBoxLayout()

    q_main_widget.setLayout(l1)    
    q_main_widget.setLayout(l2)


def test_layout_set_two_layouts(q_main_widget):
    main_layout = QVBoxLayout()
    l1 = QVBoxLayout()    
    l2 = QVBoxLayout()

    main_layout.addLayout(l1)   
    main_layout.addLayout(l2)

    q_main_widget.setLayout(main_layout) 

def test_layout_widget_parent_child_behaviour(q_main_widget):
    q_widget_2 = QWidget()

    # trying to set widget to widget
    try:
        q_main_widget.addWidget(q_widget_2)
    except: 
        print('q_main_widget.addWidget(q_widget_2) is not working')

    q_layout_1 = QVBoxLayout()

    q_widget_2.setStyleSheet("background-color: red;")
    # trying to set layout to widget 
    try:
        q_main_widget.setLayout(q_layout_1)
    except: 
        print('q_main_widget.setLayout(q_widget_2) is not working')
        
    q_layout_2 = QVBoxLayout()
    q_layout_1.addWidget(q_widget_2)
    q_widget_2.setLayout(q_layout_2)
    q_layout_1.addLayout(q_layout_2)

    test_label_1 = QLabel('test label 1')
    q_layout_2.addWidget(test_label_1)
    vboxlayout = QVBoxLayout()
    q_main_widget.setLayout(vboxlayout)
def hovered():
    print("hovering")
def clicked():
    print("clicked")
	
if __name__ == '__main__':
    window()