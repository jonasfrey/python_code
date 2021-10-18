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


class Data:
    def __init__(self):
      self.initialized = True

      self.label1 = Gui_object('the text on label', 'label')
      self.button1 = Gui_object('text on btn', 'button')

    def printsomething(self,var):
        print(var)

    def button1_click(self):
        self.button1.value = 'btn 1 clicked '+str(time.time())

    def set_n_get_function_by_string(self, string):

        funname = 'fun_'+str((int(time.time())))
        funstr = ''
        funstrlines = []
        funstrlines.append('def '+str(funname)+'(self, q_event):')

        for property in dir(self):
            print(property)
            funstrlines.append('    '+property+'='+'self.'+property)           
            # print(property, ":", value)

        # funstrlines.append('    return '+string)
        funstrlines.append('    '+string)
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
            

class Gui_object():
    event_aliases = {
      "on_click":"mousePressEvent", 
      "on_mouse_release":"mousePressEvent", 
      "on_mouse_press":"mousePressEvent", 
      "on_mouse_move":"mouseMoveEvent", 
      "on_change":"changeEvent", 
    }
    
    types = [
        "label", 
        "labelimage",
        "button", 
        "slider"
    ]

    def __init__(self, value, type, *additional_properties):
        self.type = type
        self.q_objects = [self.get_q_object(value)]
        self.min = 0
        self.max = 0
        self.step = 1
        self.value = value
        # self.on_click = None
        if(len(additional_properties) > 0):
            for key, value in additional_properties.items():
                setattr(self, key, value)

    def __setattr__(self, name: str, value) -> None:
        super().__setattr__(str(name), value)
        if(name == 'value'):
          self.q_objects_set_value(value)

        for event_name_alias, event_name_qt in Gui_object.event_aliases.items(): 
          if(name == event_name_alias):
            for q_object in self.q_objects:
              setattr(q_object, event_name_qt, value )


    def q_objects_set_value(self, value):
      for q_object in self.q_objects:
            if(self.type == "label"
              or self.type == "button"
            ): 
                q_object.setText(str(value))

            if(self.type == "labelimage"):
                pixmap = self.convert_cv_to_pixmap(value)
                self.resize_label_image(q_object)
                print(q_object)
                q_object.setPixmap(pixmap)

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
                
                
    def resize_label_image(self, q_object):
        q_object.resize(self.width, self.height)

    def convert_cv_to_pixmap(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.width, self.height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def get_q_object(self, value):
        # print('creating object fwith val'+str(value))
        # print('creating object fwith type'+str(self.type))
        if(self.type == "label"):
            o = QLabel(value)
            o.setText(str(value))

        if(self.type == "labelimage"): 
            o = QLabel()
            self.resize_label_image(o)
        if(self.type == "button"): 
            o = QPushButton(value)
            # o.clicked.connect(() 

        return o

class NestedTest:
    def __init__(self):
        self.nested_obj = Gui_object('text on lab', 'button')


class Pyqt5_app(QWidget):
    def __init__(self):

        super().__init__()

        self.setup_gui()

    def setup_gui(self):

        self.setWindowTitle('asdf')

        
        data = Data()
        data.nt = NestedTest()

        self.pyqt5_layout = Pyqt5_layout(data)

        qlab = QPushButton('click me')

        qlab.setText('CLICK ME')

        def c():
          self.pyqt5_layout.data.label1.value = str(time.time())
          print('test')

        qlab.clicked.connect(c)

        self.pyqt5_layout.converted_layout.pyqt5_class_instance.addWidget(qlab)
        
        self.setLayout(self.pyqt5_layout.converted_layout.pyqt5_class_instance)
        
        self.show()
        self.setGeometry(300, 300, 300, 220)


class Pyqt5_layout_object():
    """
    alias:pyqt5 class name
    """
    qbox_layout_class_name_mappings = {
        'column':'QHBoxLayout',
        'row':'QVBoxLayout', 
        'label':'QLabel', 
        'button':'QPushButton', 
    }

    def __init__(self, typus):
        self.value = ''
        self.typus = typus
        self.c = []
        self.pyqt5_class_instance_for_widgets = None
        self.pyqt5_class_name = self.get_pyqt5_class_name_by_string(typus)
        pyqt5_class_object = globals()[self.pyqt5_class_name]

        if(self.typus == 'column' or self.typus == 'row'):

            pyqt5_layoutouter = pyqt5_class_object()
            self.pyqt5_class_instance = pyqt5_layoutouter
            qw = QWidget()
            pyqt5_layoutouter.addWidget(qw)
            pyqt5_layoutinner = pyqt5_class_object()
            qw.setLayout(pyqt5_layoutinner)

            r = lambda: random.randint(0,255)
            rc = ('#%02X%02X%02X' % (r(),r(),r()))
            # label = QLabel(rc)
            # pyqt5_layoutinner.addWidget(label)
            qw.setStyleSheet('background-color: '+rc)
            
            self.pyqt5_class_instance_for_widgets = pyqt5_layoutinner


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
      "typus": "button",
      "syncd_obj": "button1",
      "on_click": "button1.value = 'holz schnoms'"
    },
    {
      "typus": "button",
      "syncd_obj": "nt.nested_obj",
      "on_click": "nt.nested_obj.value = time.time()"
    },
    {
      "typus": "row",
      "c": [
        {
          "typus": "label",
          "syncd_obj": "label1",
          "on_click": "print(q_event.globalX())"
        },
        {
          "typus": "column",
          "c": [
            {
              "on_mouse_move": "print(q_event.globalX())",
              "typus": "label",
              "syncd_obj": "label1"
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
          "syncd_obj": "label1"
        },
        {
          "typus": "column",
          "c": [
            {
              "typus": "label",
              "syncd_obj": "label1"
            },
            {
              "typus": "row",
              "c": [
                {
                  "typus": "label",
                  "syncd_obj": "label1"
                },
                {
                  "typus": "column",
                  "c": [
                    {
                      "typus": "label",
                      "syncd_obj": "label1"
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
        self.converted_layout = self.foreach_prop_in_oject(obj, self)

    def foreach_prop_in_oject(self, object, parent):
      
        pyqt5_layout_object_typus = object['typus']
        converted_object = Pyqt5_layout_object(
                pyqt5_layout_object_typus
        )

        if('syncd_obj' in object):
            
            gui_object =  rgetattr(self.data, object['syncd_obj'])
            child_gui_object = Gui_object(
              gui_object.value, 
              gui_object.type
            )

            gui_object.q_objects.append(
             child_gui_object.q_objects[0] 
            )

            converted_object.pyqt5_class_instance = child_gui_object.q_objects[0]
        
        for event_name_alias, event_name_qt in Gui_object.event_aliases.items():
          if(event_name_alias in object):
            try:
              fun_or_str = rgetattr(self.data, object[event_name_alias])
              if(callable((fun_or_str))):
                fun = fun_or_str
            except:
              function_body = self.data.set_n_get_function_by_string(object[event_name_alias])
              print(function_body)
              setattr(gui_object, event_name_alias, function_body)

        if('c' in object):
            for obj in object['c']:

                pyqt5_layout_object = self.foreach_prop_in_oject(obj, converted_object)
                
                if(pyqt5_layout_object.typus == 'column' or pyqt5_layout_object.typus == 'row'):
                    converted_object.pyqt5_class_instance.addLayout(pyqt5_layout_object.pyqt5_class_instance)
                    
                if(
                  pyqt5_layout_object.typus == 'label'
                  or
                  pyqt5_layout_object.typus == 'button'
                  ):  
                    print(pyqt5_layout_object.pyqt5_class_instance)
                    converted_object.pyqt5_class_instance_for_widgets.addWidget(pyqt5_layout_object.pyqt5_class_instance)

                converted_object.c.append(pyqt5_layout_object)

        return converted_object 

if __name__ == '__main__':

    qApplication = QApplication(sys.argv)

    pyqt5_app = Pyqt5_app()

    sys.exit(qApplication.exec_())