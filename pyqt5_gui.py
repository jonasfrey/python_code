from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import forcepoint, pyqtSignal, pyqtSlot, Qt, QThread
import json
import sys
import random
from json.encoder import py_encode_basestring_ascii

from cv2 import CAP_PROP_INTELPERC_DEPTH_FOCAL_LENGTH_VERT, THRESH_TOZERO


class Data:
    def __init__(self):
        self.teststr = 'stesrt sd tla;ksjdf '

class Pyqt5_app(QWidget):
    def __init__(self):

        super().__init__()

        self.setup_gui()

    def setup_gui(self):

        self.setWindowTitle('asdf')

        self.main_layout = QHBoxLayout()
        

        pyqt5_layout_object = Pyqt5_layout_object('QVBoxLayout')

        self.left_box = QVBoxLayout()
        self.left_box = pyqt5_layout_object.pyqt5_class_instance
        label = QLabel('111')
        self.left_box.addWidget(label)
        self.main_layout.addLayout(self.left_box)

        self.right_box = QHBoxLayout()
        label = QLabel('222')
        self.right_box.addWidget(label)
        self.main_layout.addLayout(self.right_box)
            


        self.pyqt5_layout = Pyqt5_layout()
        self.setLayout(self.pyqt5_layout.converted_layout.pyqt5_class_instance)
        #self.setLayout(self.main_layout)
        
        
        self.show()
        self.setGeometry(300, 300, 300, 220)
        # self.pyqt5_layout.converted_layout.pyqt5_class_instance.addWidget(label)

        # self.pyqt5_layout = Pyqt5_layout()
        
        #  self.setLayout(self.pyqt5_layout.converted_layout.pyqt5_class_instance)

        # self.data = Data()

        # w.setWindowTitle('Simple')
        # w.show()


        
        


class Pyqt5_layout_object():
    """
    alias:pyqt5 class name
    """
    qbox_layout_class_name_mappings = {
        'column':'QHBoxLayout',
        'row':'QVBoxLayout'
    }

    def __init__(self, string):
        self.c = []
        self.get_pyqt5_class_name_by_string(string)
        pyqt5_class_object = globals()[self.get_pyqt5_class_name_by_string(string)]
        pyqt5_class_object_instance = pyqt5_class_object()

        qw = QWidget()
        r = lambda: random.randint(0,255)
        rc = ('#%02X%02X%02X' % (r(),r(),r()))
        label = QLabel(rc)
        qw.setStyleSheet('background-color: '+rc)
        pyqt5_class_object_instance.addWidget(qw)
        pyqt5_class_object_instance_inner = pyqt5_class_object()
        qw.setLayout(pyqt5_class_object_instance_inner)
        pyqt5_class_object_instance_inner.addWidget(label)
        pyqt5_class_object_instance.addLayout(pyqt5_class_object_instance_inner)
        
        self.pyqt5_class_instance = pyqt5_class_object_instance


        # label = QLabel('Webcams')
        # self.pyqt5_class_instance.addWidget(label)
    
    def get_pyqt5_class_name_by_string(self, string):
        try:
            return Pyqt5_layout_object.qbox_layout_class_name_mappings[string]
        except:
            return string

class Pyqt5_layout:

    def __init__(self):
        tmp_layout = None
        self.converted_layout = None
        self.layout_json = """
            {
                "pyqt5_class_name":"column",
                "c":[
                        {
                            "pyqt5_class_name":"row",
                            "c":[
                                    {
                                        "pyqt5_class_name":"column",
                                        "c":[
                                                {
                                                    "pyqt5_class_name":"row",
                                                    "c":[
                                                        
                                                    ]
                                                }
                                        ]
                                    }
                            ]
                        },
                        {
                            "pyqt5_class_name":"row",
                            "c":[
                                    {
                                        "pyqt5_class_name":"column",
                                        "c":[
                                                {
                                                    "pyqt5_class_name":"row",
                                                    "c":[
                                                        {
                                                            "pyqt5_class_name":"column",
                                                            "c":[
                                                                {
                                                                    "pyqt5_class_name":"row"
                                                                },
                                                                {
                                                                    "pyqt5_class_name":"row"
                                                                },
                                                                {
                                                                    "pyqt5_class_name":"row"
                                                                },
                                                                {
                                                                    "pyqt5_class_name":"row"
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                        ]
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

        converted_object = Pyqt5_layout_object(object['pyqt5_class_name'])
        # print(object['c'])

        if('c' in object):
            for obj in object['c']:
                pyqt5_layout_object = self.foreach_prop_in_oject(obj, converted_object)
                try:
                    converted_object.pyqt5_class_instance.addLayout(pyqt5_layout_object.pyqt5_class_instance)
                except:
                    print('alreadz')
                    raise
                converted_object.c.append(pyqt5_layout_object)


        return converted_object 
        
            # print(type(value))




if __name__ == '__main__':

    qApplication = QApplication(sys.argv)

    pyqt5_app = Pyqt5_app()

    sys.exit(qApplication.exec_())
