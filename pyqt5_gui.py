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
        'row':'QVBoxLayout', 
        'label':'QLabel', 
    }

    def __init__(self, typus, value=''):
        self.value = value
        self.typus = typus
        
        self.c = []
        
        self.pyqt5_class_name = self.get_pyqt5_class_name_by_string(typus)
        pyqt5_class_object = globals()[self.pyqt5_class_name]
        

        pyqt5_class_object_instance = pyqt5_class_object()
        self.pyqt5_class_instance = pyqt5_class_object_instance
        
        if(self.typus == 'column' or self.typus == 'row'):
            self.value = 'lauout has no value'

            qw = QWidget()
            pyqt5_class_object_instance.addWidget(qw)
            pyqt5_class_object_instance_inner = pyqt5_class_object()
            qw.setLayout(pyqt5_class_object_instance_inner)
            
            r = lambda: random.randint(0,255)
            rc = ('#%02X%02X%02X' % (r(),r(),r()))
            label = QLabel(rc)
            qw.setStyleSheet('background-color: '+rc)
            pyqt5_class_object_instance_inner.addWidget(label)

            pyqt5_class_object_instance.addLayout(pyqt5_class_object_instance_inner)
            

        if(self.typus == 'label'):
            pyqt5_class_object_instance.setText(self.value)

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
  "typus": "column",
  "c": [
    {
      "typus": "label",
      "value": "1"
    },
    {
      "typus": "row",
      "c": [
        {
          "typus": "label",
          "value": "2"
        },
        {
          "typus": "column",
          "c": [
            {
              "typus": "label",
              "value": "3"
            },
            {
              "typus": "row"
            }
          ]
        }
      ]
    },
    {
      "typus": "row",
      "c": [
        {
          "typus": "label",
          "value": "4"
        },
        {
          "typus": "column",
          "c": [
            {
              "typus": "label",
              "value": "5"
            },
            {
              "typus": "row",
              "c": [
                {
                  "typus": "label",
                  "value": "6"
                },
                {
                  "typus": "column",
                  "c": [
                    {
                      "typus": "label",
                      "value": "7"
                    },
                    {
                      "typus": "row"
                    },
                    {
                      "typus": "row"
                    },
                    {
                      "typus": "row"
                    },
                    {
                      "typus": "row"
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

        
        pyqt5_layout_object_typus = object['typus']
        
        if('value' in object):
            pyqt5_layout_object_value = object['value']
        else:
            pyqt5_layout_object_value = ''

        converted_object = Pyqt5_layout_object(
            pyqt5_layout_object_typus,
            pyqt5_layout_object_value
        )
        
        # print(object['c'])

        if('c' in object):
            for obj in object['c']:
                pyqt5_layout_object = self.foreach_prop_in_oject(obj, converted_object)
                
                if(pyqt5_layout_object.typus == 'column' or pyqt5_layout_object.typus == 'row'):
                    converted_object.pyqt5_class_instance.addLayout(pyqt5_layout_object.pyqt5_class_instance)
                    
                if(pyqt5_layout_object.typus == 'label'):
                    converted_object.pyqt5_class_instance.addWidget(pyqt5_layout_object.pyqt5_class_instance)

                converted_object.c.append(pyqt5_layout_object)


        return converted_object 
        
            # print(type(value))




if __name__ == '__main__':

    qApplication = QApplication(sys.argv)

    pyqt5_app = Pyqt5_app()

    sys.exit(qApplication.exec_())
