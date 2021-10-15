from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import forcepoint, pyqtSignal, pyqtSlot, Qt, QThread
import json
import sys
import random
import functools
from json.encoder import py_encode_basestring_ascii
import time 

import cv2

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))



'''
important , this is your data object, you can reference its data in the view with

"value" : "self.data.name_of_the_data_object_attribute"

'''
class Data:
    def __init__(self):
        self.label1 = Gui_object('label1', 'llabel 1 gui object', 'label')

class Gui_object():
    types = [
        "label", 
        "labelimage"
    ]
    def __init__(self, name, value, type, *additional_properties):
        self.type = type
        self.q_object = self.get_q_object(name, value)
        self.name = name
        self.value = value
        if(len(additional_properties) > 0):
            for key, value in additional_properties.items():
                setattr(self, key, value)

    def __setattr__(self, name: str, value) -> None:
        super().__setattr__(str(name), value)
        if(name == 'value'):
            if(self.type == "label"): 
                self.q_object.setText(value)

            if(self.type == "labelimage"):
                pixmap = self.convert_cv_to_pixmap(value)
                print(self.q_object)
                self.q_object.setPixmap(pixmap)

        if(name == 'value'):
            if(self.type == "labelimage"):
                self.resize_label_image(self.q_object)

    def __getattribute__(self, name):
        #return super(self).__getattribute__(name)
        #return super().__getattribute__(str(name))
        try: 

            return super().__getattribute__(str(name))
        except: 
            if(name=='width'):
                return 50 #default value 
            if(name=='height'):
                return 50 #default value 
            raise AttributeError
                
        # if(hasattr(self, "_"+str(name))):
        #     return super(self).__getattribute__(str(name))
        # else:
        #     raise AttributeError
                
    def resize_label_image(self, q_object):
        q_object.resize(self.width, self.height)

    def convert_cv_to_pixmap(self, cv_img):
        
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(22,22, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


    def get_q_object(self, name, value):
        if(self.type == "label"):

            l = QLabel(value)
            #self.left_box.addWidget(l)
            l.setText(value)

            return l
        if(self.type == "labelimage"): 
            o = QLabel()
            self.resize_label_image(o)
            return o 



class Pyqt5_app(QWidget):
    def __init__(self):

        super().__init__()

        self.setup_gui()

    def setup_gui(self):

        self.setWindowTitle('asdf')

        self.pyqt5_layout = Pyqt5_layout(data=Data())
        self.setLayout(self.pyqt5_layout.converted_layout.pyqt5_class_instance)
        
        self.show()
        self.setGeometry(300, 300, 300, 220)

        t = 0
        while(True):
          t = t + 1
          time.sleep(0.1)
          self.pyqt5_layout.data.label1.value = 't is:'+str(t)
class Pyqt5_layout_object():
    """
    alias:pyqt5 class name
    """
    qbox_layout_class_name_mappings = {
        'column':'QHBoxLayout',
        'row':'QVBoxLayout', 
        'label':'QLabel', 
    }

    def __init__(self, typus):
        self.value = ''
        self.typus = typus
        
        self.c = []
        
        self.pyqt5_class_name = self.get_pyqt5_class_name_by_string(typus)
        pyqt5_class_object = globals()[self.pyqt5_class_name]
        
        if(self.typus == 'column' or self.typus == 'row'):

            pyqt5_class_object_instance = pyqt5_class_object()
            self.pyqt5_class_instance = pyqt5_class_object_instance
            
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
            

        # label = QLabel('Webcams')
        # self.pyqt5_class_instance.addWidget(label)
    
    def get_pyqt5_class_name_by_string(self, string):
        try:
            return Pyqt5_layout_object.qbox_layout_class_name_mappings[string]
        except:
            return string

class Pyqt5_layout:

    def __init__(self, data):
        self.data = data
        tmp_layout = None
        self.converted_layout = None
        self.layout_json = """
            {
  "typus": "column",
  "c": [
    {
      "typus": "label",
      "value": "label1"
    },
    {
      "typus": "row",
      "c": [
        {
          "typus": "label",
          "value": "label1"
        },
        {
          "typus": "column",
          "c": [
            {
              "typus": "label",
              "value": "label1"
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
          "value": "label1"
        },
        {
          "typus": "column",
          "c": [
            {
              "typus": "label",
              "value": "label1"
            },
            {
              "typus": "row",
              "c": [
                {
                  "typus": "label",
                  "value": "label1"
                },
                {
                  "typus": "column",
                  "c": [
                    {
                      "typus": "label",
                      "value": "label1"
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
        converted_object = Pyqt5_layout_object(
                pyqt5_layout_object_typus
        )

        if('value' in object):
            
            pyqt5_layout_object_value =  rgetattr(self.data, object['value'])

            converted_object.pyqt5_class_instance = pyqt5_layout_object_value.q_object
        
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
