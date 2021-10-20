
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
        self.dict_object = dict_object
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

        for i in self.dict_object:
            if(hasattr(self.qt_object, i)):
                
                function_body = self.data.set_n_get_return_function_by_string(self.dict_object[i])

                if(i == 'mousePressEvent'):
                    setattr(self.qt_object, i, function_body)
                else: 

                    attr = getattr(self.qt_object, i)
                    if(callable(attr)):
                        function_return = function_body()
                        print(attr)
                        attr(function_return)
                        # print(attr)

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
    
    def if_condition_is_true(self):
        # if condition is true or non existsing 
        if('if' in self.dict_object):
            condition = self.dict_object["if"]
            function_body = self.data.set_n_get_return_function_by_string(condition)
            condition_result = function_body()
            return condition_result
        else:
            return True
class Pyqt5_layout:

    def __init__(self, data):

        self.data = data
        
        self.rendered_layout = None
        self.layout_json = """
            {
              "qt_class_name" : "QVBoxLayout", 
              "c": [
                { 
                    "qt_class_name": "QPushButton",  
                    "c": "'click me'", 
                    "mousePressEvent": "print('hi')"       
                },
                { 
                    "qt_class_name": "QPushButton",  
                    "c": "'len(cameras)'+str(len(cameras))", 
                    "mousePressEvent": "Pyqt5_app.re_render_layout()" ,
                    "mousePressEventdisabled": "print('lel whz is this alreadz called')" 
                },
                { 
                    "qt_class_name": "QPushButton",  
                    "c": "'add cam'", 
                    "mousePressEvent": "cameras.append(1)"       
                },
                { 
                    "qt_class_name": "QPushButton",  
                    "c": "'remove cam'", 
                    "mousePressEvent": "cameras.pop(0)"       
                },
                {
                    "if": "len(cameras) > 0", 
                    "qt_class_name": "QLabel",  
                    "c": "str(time.time())+'len cameras is bigger 0'"           
                },
                {
                  "qt_class_name": "QLabel",  
                  "c": "str(time.time())+'i want to get rendered'"
                },
                {
                  "qt_class_name": "QLabel",  
                  "c": "len(cameras)"
                },
                {
                  "qt_class_name": "QWidget",  
                  "setStyleSheet": "'background-color: '+random_color()",
                  "c": [
                    {
                    "qt_class_name": "QHBoxLayout",  
                    "c": [
                        {
                            "qt_class_name" : "QVBoxLayout"
                        }
                    ]
                    }
                  ]
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

                if(pyqt5_layout_object_child == False):
                    continue

                if(pyqt5_layout_object_parent.qt_class_name == 'QWidget'):
                    pyqt5_layout_object_parent.qt_object.setLayout(pyqt5_layout_object_child.qt_object)
                else: 
                    if(pyqt5_layout_object_child.is_qt_layout_class_name()):
                        pyqt5_layout_object_parent.qt_object.addLayout(pyqt5_layout_object_child.qt_object)
                    else:
                        pyqt5_layout_object_parent.qt_object.addWidget(pyqt5_layout_object_child.qt_object)

        if(pyqt5_layout_object_parent.if_condition_is_true()):
            return pyqt5_layout_object_parent
        else:
            return False

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

    def random_color(self):
        r = lambda: random.randint(0,255)
        rc = ('#%02X%02X%02X' % (r(),r(),r()))
        return str(rc)

    def set_n_get_function_by_string(self, string, last_line_prefix):

        funname = 'fun_'+str((int(time.time())))
        funstr = ''
        funstrlines = []
        funstrlines.append('def '+str(funname)+'(self, *args):')

        for property in dir(self):
            # print(property)
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
        self.setLayout(self.layout)
        self.show()

    def reset_layout(self):
        if(hasattr(self, 'render_layout')):
            self.layout.removeItem(self.render_layout)
            for i in reversed(range(self.render_layout.count())):
                if(self.render_layout.itemAt(i).widget() != None):
                    self.render_layout.itemAt(i).widget().setParent(None)

    def render_render_layout(self):

        if(hasattr(self, 'pyqt5_layout')):
            print('re rendering layout')
            self.reset_layout()
            self.render_layout = self.pyqt5_layout.render_layout()
            self.layout.addLayout(self.render_layout)


if __name__ == '__main__':

    qApplication = QApplication(sys.argv)

    pyqt5_app = Pyqt5_app()

    sys.exit(qApplication.exec_())