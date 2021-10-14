from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import forcepoint, pyqtSignal, pyqtSlot, Qt, QThread
import json
import sys
from json.encoder import py_encode_basestring_ascii

from cv2 import CAP_PROP_INTELPERC_DEPTH_FOCAL_LENGTH_VERT


class Data:
    def __init__(self):
        self.teststr = 'stesrt sd tla;ksjdf '

class Pyqt5_app(QWidget):
    def __init__(self):

        self.qApplication = QApplication(sys.argv)
        super().__init__()

        self.pyqt5_layout = Pyqt5_layout()
        
        self.main_layout = QVBoxLayout()

        # self.setLayout(self.pyqt5_layout.converted_layout.pyqt5_class_instance)
        self.setLayout(self.main_layout)
        
        self.disply_width = 888
        self.display_height = 500

        self.show()

        self.data = Data()
        


class Pyqt5_layout_object():
    def __init__(self, pyqt5_class_name, parent_pyqt5_layout_object):
        self.c = []
        klass = globals()[pyqt5_class_name]
        self.pyqt5_class_instance = klass()
        label = QLabel('Webcams')
        self.pyqt5_class_instance.addWidget(label)
        self.parent_pyqt5_layout_object = parent_pyqt5_layout_object
    
    @property
    def addLayout(self, layout):
        print('test test test')
        return self.pyqt5_class_instance.addLayout(layout)

class Pyqt5_layout:

    def __init__(self):
        tmp_layout = None
        self.converted_layout = None
        self.layout_json = """
            {
                "pyqt5_class_name":"QHBoxLayout",
                "c":[
                    {
                        "pyqt5_class_name":"QVBoxLayout",
                        "c":[
                            {
                                "pyqt5_class_name":"QHBoxLayout"
                            }
                        ]
                    }
                ]
            }
        """

        self.update_layout()


    def update_layout(self):
        obj = json.loads(self.layout_json)
        # print(obj['pyqt5_class_name'])
        # exit()

        self.converted_layout = self.foreach_prop_in_oject(obj, self)
        
        # self.converted_layout = self.get_pyqt5_layout_object_by_json_object()

        # print(obj)

    def foreach_prop_in_oject(self, object, parent):
        converted_object = self.get_pyqt5_layout_object_by_json_object(object, parent)
        # print(object['c'])

        if('c' in object):
            for obj in object['c']:
                pyqt5_layout_object = self.foreach_prop_in_oject(obj, converted_object)
                pyqt5_layout_object.pyqt5_class_instance.addLayout(converted_object.pyqt5_class_instance)
                converted_object.c.append(pyqt5_layout_object)


        return converted_object 
        
            # print(type(value))

    def get_pyqt5_layout_object_by_json_object(self, json_object, parent=QVBoxLayout()):
        # print(json_object.p)
        # print(vars(json_object))
        return Pyqt5_layout_object(json_object['pyqt5_class_name'], parent)




pyqt5_app = Pyqt5_app()