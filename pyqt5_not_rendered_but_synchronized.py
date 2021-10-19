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

          

class Gui_object():
    event_aliases = {
      "on_click":"mousePressEvent", 
      "on_mouse_release":"mousePressEvent", 
      "on_mouse_press":"mousePressEvent", 
      "on_mouse_move":"mouseMoveEvent", 
      "on_change":"changeEvent"
    }
    
    types = [
        "label", 
        "labelimage",
        "button", 
        "slider",
        "textinput"
    ]
    input_properties = [
      "value",
      "min",
      "max",
      "step",
    ]
    def __init__(self, value, type,  *additional_properties):
        self.type = type
        self.q_objects = [self.get_q_object(value)]
        self._min = 0
        self._max = 0
        self._step = 1
        self._value = value
        # self.on_click = None
        if(len(additional_properties) > 0):
            for key, value in additional_properties.items():
                setattr(self, key, value)

    def input_change(self, param):
        print('input change called')
        print(param)

    def __setattr__(self, name: str, value) -> None:
        property_name_for_setter = name
        if(name in Gui_object.input_properties):
          intern_name = '_'+str(name)
          property_name_for_setter = intern_name
    
        super().__setattr__(property_name_for_setter, value)

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
        if(name in Gui_object.input_properties):
          name = '_'+str(name)
        print('Gui_object getattr was called with propname :'+str(name))
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
        if(self.type == "textinput"):

            o = QLineEdit(value)

            # exec(
            #     """
            # def input_change(param):
            #     print(param)
            #     """
            # )
            # def input_change(param):
            #     print(self.value)
            #     self.value = param
            #     print(self.value)
                # print(param)
                
            # o.textChanged.connect(hure)
            # fun = getattr(self, 'input_change')
            o.textChanged.connect(
                lambda val: [ setattr(self, 'value', val), print(self.value) ]
            )
            # o.textChanged.connect(getattr(self, 'input_change'))
            self.input_change(1)
            # o.changeEvent = self.input_change

            o.setText(str(value))

            # o.clicked.connect(()


        return o


class Pyqt5_layout_object():
    """
    alias:pyqt5 class name
    """
    q_class_name_mappings = {
        'containers':{
          'column':'QHBoxLayout',
          'row':'QVBoxLayout',
        }, 
        'content':{
          'label':'QLabel',
          'button':'QPushButton',
          'textinput':'QLineEdit'
        }
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

    
    def get_q_class_name_mapping(self, string):
      for key in Pyqt5_layout_object.q_class_name_mappings:
        value = Pyqt5_layout_object.q_class_name_mappings[key]
        if(string in value):
          return value[string]

      return False

    def get_pyqt5_class_name_by_string(self, string):      
      q_class_name = string 
      
      mapped_q_class_name = self.get_q_class_name_mapping(string)

      if(mapped_q_class_name):
        q_class_name = mapped_q_class_name
      
      return q_class_name

class Pyqt5_layout:

    def __init__(self, data):
        self.data = data
        self.rendered_layout = None
        self.layout_json = """
            {
  "typus": "column",
  "c": [
    {
      "typus": "textinput",
      "sync_obj": "textinput1"
    },
    {
      "typus": "button",
      "sync_obj": "button1",
      "on_click": "button1.value = 'test'"
    },
    {
      "typus": "label",
      "sync_obj": "label1",
      "on_click": "label1.value = button1.value"
    },
    {
      "typus": "label",
      "sync_obj": "button1"
    },
    {
      "typus": "row",
      "c": [
        {
          "typus": "label",
          "sync_obj": "label1"
        },
        {
          "typus": "column",
          "c": [
            {
              "typus": "label",
              "sync_obj": "button1"
            },
            {
              "typus": "row",
              "c": [
                {
                  "typus": "label",
                  "sync_obj": "button1"
                },
                {
                  "typus": "column",
                  "c": [
                    {
                      "typus": "label",
                      "sync_obj": "button1"
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

        self.rendered_layout = self.render_layout().pyqt5_class_instance


    def render_layout(self):
        obj = json.loads(self.layout_json)
        self.converted_layout = self.foreach_prop_in_oject(obj, self)
        return self.converted_layout

    def foreach_prop_in_oject(self, object, parent):
      
        pyqt5_layout_object_typus = object['typus']
        converted_object = Pyqt5_layout_object(
                pyqt5_layout_object_typus
        )

        if('sync_obj' in object):
            
            gui_object =  rgetattr(self.data, object['sync_obj'])
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
                else:
                    converted_object.pyqt5_class_instance_for_widgets.addWidget(pyqt5_layout_object.pyqt5_class_instance)

                converted_object.c.append(pyqt5_layout_object)

        return converted_object 



class Data:
    def __init__(self):
      self.initialized = True
      self.label1 = Gui_object('the text on label', 'label')
      self.button1 = Gui_object('text on btn', 'button')
      self.textinput1 = Gui_object('preview text', 'textinput')

    def set_n_get_function_by_string(self, string):

        funname = 'fun_'+str((int(time.time())))
        funstr = ''
        funstrlines = []
        funstrlines.append('def '+str(funname)+'(self, q_event):')

        for property in dir(self):
            print(property)
            funstrlines.append('    '+property+'='+'self.'+property)           
            # print(property, ":", value)
          
        funstrlines.append('    print(self.textinput1.value)')           

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
            


class Pyqt5_app(QWidget):
    instances = []
    @staticmethod
    def re_render_layout():
      for obj in Pyqt5_app.instances:
        print(obj)
        obj.render_render_layout()

    def __init__(self):
        self.__class__.instances.append(self)

        super().__init__()

        self.initialize_gui()

    def initialize_gui(self):

        self.setWindowTitle('asdf')

        data = Data()
        self.pyqt5_layout = Pyqt5_layout(data)
        self.layout = QHBoxLayout()
        self.render_render_layout()
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
        self.reset_layout()
        self.render_layout = self.pyqt5_layout.render_layout()
        self.layout.addLayout(self.render_layout.pyqt5_class_instance)


if __name__ == '__main__':

    qApplication = QApplication(sys.argv)

    pyqt5_app = Pyqt5_app()

    sys.exit(qApplication.exec_())