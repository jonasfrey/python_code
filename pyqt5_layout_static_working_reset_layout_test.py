from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QApplication,QLineEdit, QLabel, QVBoxLayout, QPushButton, QSlider
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import forcepoint, pyqtSignal, pyqtSlot, Qt, QThread
import json
import sys
import random
import functools
from json.encoder import py_encode_basestring_ascii
import time 
import copy
import types


import cv2

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


class Pyqt5_layout_object: 
    qt_layout_class_names = [
        "QHBoxLayout",
        "QVBoxLayout"
    ]
    def __init__(self,dict_object, data):
        self.data = data
        self.qt_class_name = dict_object["qt_class_name"]
        self.qt_object = globals()[self.qt_class_name]()
        if 'c' in dict_object:
            self.c = dict_object["c"] # c is shor for children, can be string, or data path
        else:
            self.c = None

        self.synced_obj_data_path = None 
        self.render_function = None

        if(self.wants_to_be_evaluated()):
            function_body = self.data.set_n_get_return_function_by_string(self.c)

            self.qt_object.setText(str(function_body()))

    def has_children(self):
        return (type(self.c) == list)
            # self.type = 'has_children'
            # has children 
    def wants_to_be_synced(self):
        try:
            rgetattr(self.data, self.c)
            return True
        except:
            return False
            # wants to be synced
            # self.type = 'wants_to_be_synced'
            # c is the path of a data object which has to be synced 
            # for example data.cameras[0]
    def wants_to_be_evaluated(self):
        return (
            self.is_qt_layout_class_name() == False and 
            self.has_children() == False and 
            self.wants_to_be_synced() == False
            )
            # self.type = 'wants_to_be_evaluated'
            # wants to be evaluated 
    def is_qt_layout_class_name(self):
        return self.qt_class_name in Pyqt5_layout_object.qt_layout_class_names
        
class Pyqt5_layout:

    def __init__(self, data):

        self.data = data
        
        self.rendered_layout = None
        self.layout_json = """
            {
              "qt_class_name" : "QVBoxLayout", 
              "c": [
                {
                  "qt_class_name": "QLabel",  
                  "c": "str(time.time())+'i want to get rendered'"
                },
                {
                  "qt_class_name": "QLabel",  
                  "c": "len(cameras)"
                },
                {
                  "qt_class_name": "QHBoxLayout",  
                  "c": [
                    {
                        "qt_class_name" : "QVBoxLayout"
                    }
                  ]
                },
                {
                  "qt_class_name": "QVBoxLayout",  
                  "c": [
                    {
                        "qt_class_name" : "QHBoxLayout", 
                        "c": [
                            {
                                "qt_class_name" : "QHBoxLayout"
                            }
                        ]
                    },
                    {
                        "qt_class_name" : "QHBoxLayout", 
                        "c": [
                            {
                                "qt_class_name" : "QHBoxLayout"
                            }
                        ]
                    }
                  ]
                }
              ]

            }
        """

        self.rendered_layout = self.render_layout()


    def render_layout(self):
        obj = json.loads(self.layout_json)
        self.converted_layout = self.foreach_prop_in_oject(obj)
        return self.converted_layout.qt_object

    def foreach_prop_in_oject(self, object):

        pyqt5_layout_object_parent = Pyqt5_layout_object(object, self.data)
        if(pyqt5_layout_object_parent.has_children()):
            for obj in pyqt5_layout_object_parent.c:
                pyqt5_layout_object_child = self.foreach_prop_in_oject(obj)
                    
                if(pyqt5_layout_object_child.is_qt_layout_class_name()):
                    pyqt5_layout_object_parent.qt_object.addLayout(pyqt5_layout_object_child.qt_object)
                else:
                    pyqt5_layout_object_parent.qt_object.addWidget(pyqt5_layout_object_child.qt_object)

        return pyqt5_layout_object_parent


class Camera(): 
    def __init__(self) -> None:
        self.test = 1
        # self.xyz = ... 
        # self.xyz = ... 
        # self.xyz = ... 
        # and so on

class Data():
    def __init__(self) -> None:
        self.cameras = []

    def set_n_get_return_function_by_string(self, string):
        return self.set_n_get_function_by_string(string, 'return')

    def set_n_get_void_function_by_string(self, string):
        return self.set_n_get_function_by_string(string, '')


    def set_n_get_function_by_string(self, string, last_line_prefix):

        funname = 'fun_'+str((int(time.time())))
        funstr = ''
        funstrlines = []
        funstrlines.append('def '+str(funname)+'(self):')

        for property in dir(self):
            print(property)
            funstrlines.append('    '+property+'='+'self.'+property)           
            # print(property, ":", value)

        # funstrlines.append('    return '+string)
        funstrlines.append('    '+str(last_line_prefix)+' '+string)
        funstr = "\n".join(funstrlines)
        #print(funstr) 
        exec(funstr)
        functionbody = locals()[funname]
        # we have to bind the method to the class in order to automatically
        # get the first parameter 'self'
        # simply setattr wont work
        # setattr(self, fname, lambda: functionbody(self))
        # this will bind the method to the self
        setattr(self, funname, types.MethodType( functionbody, self ))

        return getattr(self, funname)
            


class Pyqt5_app(QWidget):
    instances = []
    @staticmethod
    def re_render_layout():
      for obj in Pyqt5_app.instances:
        obj.render_render_layout()

    def __init__(self):
        self.__class__.instances.append(self)

        super().__init__()

        self.initialize_gui()

    def initialize_gui(self):

        self.setWindowTitle('asdf')
        
        self.data = Data()
        
        if(True):
            self.data.cameras.append(Camera())
        
        self.pyqt5_layout = Pyqt5_layout(self.data)
        
        self.layout = QHBoxLayout()
        self.render_render_layout()
        
        # slider = QSlider()
        # self.layout.addWidget(slider)
        self.setLayout(self.layout)
        self.show()

    def reset_layout(self):
        if(hasattr(self, 'render_layout')):
            self.layout.removeItem(self.render_layout)
            for i in reversed(range(self.render_layout.count())): 
                
                self.render_layout.itemAt(i).widget().setParent(None)

    def render_render_layout(self):
        # if(hasattr(self, 'pyqt5_layout')):
        print('re rendering layout')
        # self.reset_layout()
        self.layout = QHBoxLayout()
        self.render_layout = self.pyqt5_layout.render_layout()
        self.layout.addLayout(self.render_layout)


if __name__ == '__main__':

    qApplication = QApplication(sys.argv)

    pyqt5_app = Pyqt5_app()

    sys.exit(qApplication.exec_())