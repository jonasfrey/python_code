
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
import gc
import inspect
import weakref

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))



class Pyqt5_view_object: 
    instances = []

    qt_layout_class_names = [
        "QHBoxLayout",
        "QVBoxLayout"
    ]
    qt_input_events = [
        "event",
        "closeEvent",
        "focusInEvent",
        "focusOutEvent",
        "enterEvent",
        "keyPressEvent",
        "keyReleaseEvent",
        "leaveEvent",
        "mouseDoubleClickEvent",
        "mouseMoveEvent",
        "mousePressEvent",
        "mouseReleaseEvent",
        "moveEvent",
        "paintEvent",
        "resizeEvent", 
        "sliderMoved",

    ]
    qt_input_events_special = [
        "textChanged",
        "valueChanged"
    ]
    qt_class_names_with_setText = [
        "QLabel", 
        "QPushButton", 
        "QLineEdit", 
    ]
    qt_class_names_with_setValue = [
        "QSlider"
    ]

    def __init__(self, dict_object, data):
        self.__class__.instances.append(self)
        self.data = data
        self.dict_object = dict_object
        self.qt_constructor = dict_object["qt_constructor"]
        self.qt_layout_added = False
        if(self.qt_constructor.find('(') == -1):
            self.qt_constructor = self.qt_constructor + '()'
        self.qt_class_name = self.get_qt_class_name_by_constructor(self.qt_constructor)
        # self.qt_object = globals()[self.qt_class_name]()
        self.qt_constructor_instance_varname = "tmp_qt_constructor_instance"
        self.qt_object = exec(self.qt_constructor_instance_varname+' = '+self.qt_constructor)  
        # since we cannot set background color or .hide / .show on QHBoxlayout and QVBoxlayout 
        # we neet a wrapper of this kind
        # q_layout
        #   q_widget <- can be visible toggled with .show / .hide , can have bg color with setStylesheet backgroun-color...
        #       q_layout
        #           qt_object <- instance of actual object from view.. label or input or layout or widget , 

        # why 4 additional qt_objects ? 
        # because the qt_object type is dynamic: layout or qwidget 
        # and qt allows only the following behaviour with addWidget or addLayout or setLayout
        # -------------------------------
        # possible      possible
        # qt_layout     qt_layout
        #   qt_laout        qt_widget
        # possible      not possible
        # qt_widget     qt_widget
        #   qt_layout       qt_widget
        self.qt_object = locals()[self.qt_constructor_instance_varname]

        self.qt_layout_great_grand_parent = QVBoxLayout()
        self.qt_widget_grand_parent = QWidget()
        self.qt_layout_parent = QVBoxLayout()
        self.qt_layout_great_grand_parent.addWidget(self.qt_widget_grand_parent)
        self.qt_widget_grand_parent.setLayout(self.qt_layout_parent)
        
        self.qt_layout_great_grand_parent.setSpacing(0)
        # self.qt_layout_great_grand_parent.setMargin(0)
        
        self.qt_layout_parent.setSpacing(0)
        # self.qt_layout_parent.setMargin(0)

        if(self.is_qt_layout_class_name()):
            self.qt_layout_parent.addLayout(self.qt_object)
        else:
            self.qt_layout_parent.addWidget(self.qt_object)

        # self.qt_object = exec(self.qt_constructor)
        self.code_statements_before_string_evaluation = []
        self.code_statements_after_string_evaluation = []

        if 'c' in dict_object:
            self.c = dict_object["c"] # c is shor for children, can be string, or data path
        else:
            self.c = None

        if 'code_statements_before_string_evaluation' in self.dict_object:
            self.code_statements_before_string_evaluation = self.dict_object['code_statements_before_string_evaluation']
        if 'code_statements_after_string_evaluation' in self.dict_object:
            self.code_statements_after_string_evaluation = self.dict_object['code_statements_after_string_evaluation']

        self.synced_obj_data_path = None 
        self.render_function = None

        self.init_event_listeners()

    def init_event_listeners(self):
        
        if(self.is_qt_layout_class_name() == False):
            self.qt_object.setMouseTracking(True)

        for i in self.dict_object:
            if(hasattr(self.qt_object, i)):
                function_body = self.data.get_void_function_by_string(self.dict_object[i], self.code_statements_before_string_evaluation, self.code_statements_after_string_evaluation+["Pyqt5_app.re_render_view()"])
                is_qt_input_event = False
                if(i in Pyqt5_view_object.qt_input_events):
                    is_qt_input_event = True
                    setattr(self.qt_object, i, function_body)
                if(i in Pyqt5_view_object.qt_input_events_special):
                    # function_body = self.data.get_void_function_by_string(self.dict_object[i], self.code_statements_before_string_evaluation, self.code_statements_after_string_evaluation)
                    is_qt_input_event = True
                    # self.qt_object.event = self.qt_object_event_function
                    localattrname = 'i_cannot_connect_this_function_directly_thats_why_i_set_this_attribute_'+str(i)
                    setattr(self.qt_object, localattrname, function_body)
                    qt_event_function = getattr(self.qt_object, i)
                    qt_event_function.connect(getattr(self.qt_object, localattrname))
                    # self.qt_object.valueChanged.connect(
                    #     lambda val: function_body(val)
                    # )
                    # qt_object_fun = getattr(self.qt_object, i)
                    # qt_object_fun.connect(getattr(self.qt_object, localattrname))
                    
                if(is_qt_input_event == False):
                    function_body = self.data.get_return_function_by_string(self.dict_object[i], self.code_statements_before_string_evaluation, self.code_statements_after_string_evaluation)
                    attr = getattr(self.qt_object, i)
                    if(callable(attr)):
                        function_return = function_body()
                        # print(attr)
                        attr(function_return)
                        # print(attr)


    def update_evaluated_properties_for_parent_widget_or_layout(self, qt_widget_or_layout):
        for i in self.dict_object:
            if(i in Pyqt5_view_object.qt_input_events):
                # we skip the event handlers since we initialize them in an other place
                continue
            else:      
                if(hasattr(qt_widget_or_layout, i)):
                    qt_function_or_property = getattr(qt_widget_or_layout, i)
                    function_body = self.data.get_return_function_by_string(
                        self.dict_object[i],
                        self.code_statements_before_string_evaluation,
                        self.code_statements_after_string_evaluation
                        )
                    evaluated_return = function_body()
                
                    if(callable(qt_function_or_property)):
                        qt_function_or_property(evaluated_return)
                    else:
                        setattr(qt_widget_or_layout, i, evaluated_return)

    def update_evaluated_properties(self):
        #  not only the 'c' property wants to be evaluated, for example there are properties like
        #  (widget).setStyleSheet or (layout).setSpacing
        #  so we have to try to evaluate those as well
        self.update_evaluated_properties_for_parent_widget_or_layout(self.qt_widget_grand_parent)
        self.update_evaluated_properties_for_parent_widget_or_layout(self.qt_layout_great_grand_parent)

        if(self.wants_to_be_evaluated()):
            function_body = self.data.get_return_function_by_string(self.c, self.code_statements_before_string_evaluation, self.code_statements_after_string_evaluation)
            evaluated_return = str(function_body())

            self.set_evaluated_return(evaluated_return)

    def set_evaluated_return(self, evaluated_return):
        if(self.qt_class_name in Pyqt5_view_object.qt_class_names_with_setText):
            self.qt_object.setText(evaluated_return)

        if(self.qt_class_name in Pyqt5_view_object.qt_class_names_with_setValue):
            self.qt_object.setValue(int(evaluated_return))

    def get_qt_class_name_by_constructor(self, string):
        parts = string.split('(')
        qt_class_name = parts.pop(0)
        return qt_class_name

    def has_c_property(self):
        return 'c' in self.dict_object

    def has_children(self):
        return (type(self.c) == list)
            # self.type = 'has_children'
            # has children 
    def wants_to_be_synced(self):
        tmpfalse = False
        return tmpfalse 
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
            self.has_c_property() == True and
            self.wants_to_be_synced() == False
            )
            # self.type = 'wants_to_be_evaluated'
            # wants to be evaluated 
    def is_qt_layout_class_name(self):
        return self.qt_class_name in Pyqt5_view_object.qt_layout_class_names
    
    def if_condition_is_true(self):
        # if condition is true or non existsing 
        if('if' in self.dict_object):
            condition = self.dict_object["if"]
            function_body = self.data.get_return_function_by_string(condition, self.code_statements_before_string_evaluation, self.code_statements_after_string_evaluation)
            condition_result = function_body()
            return condition_result
        else:
            return True

    def re_render_qt_object(self):
        if(self.if_condition_is_true()):
            self.qt_widget_grand_parent.show()
            self.update_evaluated_properties()
        else:
            self.qt_widget_grand_parent.hide()
              
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class View_object:
    def __init__(self, parent_view_object, original_object, data):
        self.child_view_objects = []
        # self.parent_view_object = parent_view_object
        self.parent_view_object = None
        self.original_object = original_object
        self.data = data
        self.for_statement = None
        self.pyqt5_view_objects = []
        
        self.update_pyqt5_view_objects()


    def get_parent_view_object_pyqt5_view_objects(self):
        if(self.parent_view_object != None):
            arr = self.parent_view_object.pyqt5_view_objects
        else:
            arr = []

        return arr
    def handle_for_statement_update_pyqt5_view_objects(self):
        if('index_in_array' in self.original_object):
            print("self.original_object['index_in_array']")
            print(self.original_object['index_in_array'])

        parts = str(self.original_object['for']).split(' in ')
        self.array_var_name_in_for_statement = parts.pop(len(parts)-1)
        parts = parts.pop(0).split(',')
        self.value_var_name_in_for_statement = parts.pop(0).strip()
        self.index_var_name_in_for_statement = parts.pop(0).strip()

        code_statements_before_string_evaluation = self.get_code_statements_before_string_evaluation_by_array_index(0)
        print(code_statements_before_string_evaluation)

        evaluated_array_var_len = self.data.get_return_function_by_string(
            "len("+self.array_var_name_in_for_statement+")", 
            code_statements_before_string_evaluation
        )()

        print(str(evaluated_array_var_len)+': length of array_var_name_in_for')
        print(str(len(self.pyqt5_view_objects))+': length of actual array')
        if(evaluated_array_var_len == len(self.pyqt5_view_objects)):
            return False
        # print(length)
        # exit()

        for key in range(len(self.pyqt5_view_objects), evaluated_array_var_len):
            original_object_copy = self.original_object.copy()

            original_object_copy['index_in_array'] = key
        
            #  code_statements_before_string_evaluation = self.get_code_statements_before_string_evaluation_by_array_index(key)

            original_object_copy['code_statements_before_string_evaluation'] = (
                code_statements_before_string_evaluation + 
                [str(self.value_var_name_in_for_statement)+' = '+str(self.array_var_name_in_for_statement)+'['+str(key)+']']
                ) 

            pyqt5_view_object = Pyqt5_view_object(original_object_copy, self.data)
            self.pyqt5_view_objects.append(pyqt5_view_object)
            # print(value)
    
    def has_parent_view_object(self):
        return self.parent_view_object != None

    def get_code_statements_before_string_evaluation_by_array_index(self, array_index):
        
        arr = []

        if self.has_parent_view_object():
            # print(len(self.parent_view_object.pyqt5_view_objects))
            parent_view_object_pyqt5_view_object = self.parent_view_object.pyqt5_view_objects[array_index]
            if 'code_statements_before_string_evaluation' in parent_view_object_pyqt5_view_object.dict_object:
                # print(parent_view_object_pyqt5_view_object.dict_object['code_statements_before_string_evaluation'])
                arr = parent_view_object_pyqt5_view_object.dict_object['code_statements_before_string_evaluation']
        
        return arr

    def update_pyqt5_view_objects(self):
        
        # print('json or original_object')
        # print(json.dumps(self.original_object))
        # print(type(self.original_object['qt_constructor']))
        # if the original_object has a for property we have to handle it here
        if('for' in self.original_object):
            self.handle_for_statement_update_pyqt5_view_objects()
        else: 
            self.original_object['code_statements_before_string_evaluation'] = self.get_code_statements_before_string_evaluation_by_array_index(0)
            self.original_object['index_in_array'] = 0
            self.pyqt5_view_objects = [Pyqt5_view_object(self.original_object, self.data)]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Pyqt5_view:

    def __init__(self, data):

        self.data = data
        self.pyqt5_view_object_parent = None
        self.view_json_tmpdisbld = """
            {
                "qt_constructor" : "QVBoxLayout", 
                "setStyleSheet": "'background-color: '+random_color()",
                "setSpacing": "sliderval.value",
                "setContentMargins": "sliderval.value",

                "c": [
                    {
                        "setStyleSheet": "'background-color: '+random_color()",
                        "qt_constructor" : "QHBoxLayout", 
                        "c":[
                            { 
                                "qt_constructor": "QPushButton",  
                                "c": "'print to console'", 
                                "mousePressEvent" : "print('printing to console')"
                            },
                            { 
                                "qt_constructor": "QPushButton",  
                                "c": "'print to console'", 
                                "mousePressEvent" : "print('printing to console')"
                            },
                            { 
                                "qt_constructor": "QPushButton",  
                                "c": "'print to console'", 
                                "mousePressEvent" : "print('printing to console')"
                            }
                        ]
                    },
                    { 
                        "qt_constructor": "QSlider(Qt.Horizontal)", 
                        "c": "sliderval.value",
                        "valueChangedasdf": "print('value '+str(event)+' changed at:'+str(time.time()))",
                        "valueChanged": "sliderval._value = event",
                        "sliderMovedasdf": "print('value '+str(event)+' changed at:'+str(time.time()))",
                        "setMinimum" : "1", 
                        "setMaximum" : "10" 
                    },
                    { 
                        "qt_constructor": "QLabel", 
                        "c":"'slider val : '+str(sliderval.value)"
                    },
                    { 
                        "qt_constructor": "QLineEdit",  
                        "c": "textforinput.value", 
                        "textChanged": "textforinput._value = event"
                    },
                    { 
                        "qt_constructor": "QLabel",  
                        "c": "'text is :'+str(textforinput.value)" 
                    },
                    { 
                        "qt_constructor": "QPushButton",  
                        "c": "'reset text above'", 
                        "mousePressEvent" : "textforinput.value = 'reseetet text'"
                    },
                    { 
                        "qt_constructor": "QPushButton",  
                        "c": "'print to console'", 
                        "mousePressEvent" : "print('printing to console')"
                    },

                    { 
                        "qt_constructor": "QPushButton",  
                        "c": "'click me'", 
                        "mousePressEvent": "test_synced_obj()", 
                        "mouseMoveEvent" : "print('damn mouse moved on butto')"
                    },
                    {
                    "qt_constructor_qwidget_is_not_allowed_use_qwdiget_property_to_render_on_widget": "QWidget",  
                    "setStyleSheet": "'background-color: '+random_color()",
                    "c": [
                        { 
                            "qt_constructor_this_wont_be_possible_since_qwidget_cannot_directly_be_child_of_qwidget": "QLabel",  
                            "c": "'qlabel directly child of qwidget'" 
                        },
                        {
                        "qt_constructor": "QHBoxLayout",  
                        "c": [
                            {
                                "qt_constructor" : "QVBoxLayout"
                            }
                        ]
                        }
                    ]
                    },
                    { 
                        "qt_constructor": "QPushButton",  
                        "c": "'len(cameras)'+str(len(cameras))", 
                        "mousePressEvent": "Pyqt5_app.re_render_view()" ,
                        "mousePressEventdisabled": "print('lel whz is this alreadz called')" 
                    },
                    { 
                        "qt_constructor": "QPushButton",  
                        "c": "'add cam'", 
                        "mousePressEvent": "cameras.append(1)"       
                    },
                    { 
                        "qt_constructor": "QPushButton",  
                        "c": "'remove cam'", 
                        "mousePressEvent": "cameras.pop(0)"       
                    },
                    {
                        "if": "len(cameras) > 2",
                        "qt_constructor": "QHBoxLayout",  
                        "c":[
                            {
                                "if": "len(cameras) > 3", 
                                "qt_constructor": "QLabel",  
                                "c": "str(time.time())+' i show because cameras is bigger 3'"           
                            },
                            {
                                "if": "len(cameras) > 1", 
                                "qt_constructor": "QLabel",  
                                "c": "str(time.time())+' i show because cameras is bigger 1'"           
                            },
                            {
                                "qt_constructor": "QLabel",  
                                "c": "str(time.time())+' i show because cameras is bigger 2'"           
                            }
                        ]
                    },
                    { 
                        "qt_constructor": "QPushButton",  
                        "c": "'add to string array'", 
                        "mousePressEvent": "stringarray.append(Synced_data_obj('more txt'+str(len(stringarray))))"       
                    },
                    { 
                        "qt_constructor": "QPushButton",  
                        "c": "'remove from string array'", 
                        "mousePressEvent": "stringarray.pop(1)"       
                    },
                    { 
                        "qt_constructor": "QLabel",  
                        "c": "'len(stringarray):'+str(len(stringarray))" 
                    },
                    {
                        "qt_constructor": "QLabel",  
                        "c": "str(time.time())+'i want to get rendered'"
                    },
                    {
                        "qt_constructor": "QLabel",  
                        "c": "len(cameras)"
                    },
                    {
                        "qt_constructor": "QHBoxLayout",  
                        "for": "value_asdf_test, key in stringarray",
                        "c": [
                            {
                                "qt_constructor":"QLabel", 
                                "c":"'str arr val '+str(value_asdf_test.value)"
                            }
                        ]
                    },
                    {
                        "qt_constructor": "QLabel",  
                        "c": "textasdf.value"
                    },  
                    {
                        "qt_constructor": "QVBoxLayout",  
                        "c": [
                            {
                                "qt_constructor" : "QHBoxLayout", 
                                "c": [
                                    {
                                        "qt_constructor" : "QHBoxLayout"
                                    }
                                ]
                            },
                            {
                                "qt_constructor" : "QHBoxLayout", 
                                "c": [
                                    {
                                        "qt_constructor" : "QHBoxLayout"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        """
        self.view_json = """
            
                {
                    "qt_constructor" : "QHBoxLayout", 
                    "for": "val1, key in stringarray",
                    "c":[
                        {
                            "for": "value_asdf_test, key in stringarray",
                            "qt_constructor":"QLabel", 
                            "c":"'str arr val '+str(value_asdf_test.value)"
                        }
                    ]
                }
            
        """

    def render_view_without_reset(self):
        # self.recursive_update_for_loops(self.pyqt5_view_object_parent[0])
        for instance in Pyqt5_view_object.instances:
            instance.re_render_qt_object()

        # for obj in gc.get_objects():
        #     if(hasattr(obj, 'qt_constructor')):
        #         print(time.time())

        #     if isinstance(obj, pyqt5_view_object):
        #         print(time.time())
        #         print(obj)
        #         obj.re_render_qt_object()

    def get_rendered_view_from_json(self):
        self.original_object = json.loads(self.view_json)

        # if(type(self.original_object) != dict):
        #     raise Exception('root of view_json hase to be one single object {...}, not an array')
        # if('for' in self.original_object):
        #     raise Exception('root of view_json must not contain a "for" property')
        self.original_object_copy = (self.original_object).copy()

        newobj = self.recursive_update_rendered_objects(self.original_object_copy)
        

        # self.data.stringarray.append(Synced_data_obj('stringarray text 3'))
        # self.data.stringarray.append(Synced_data_obj('stringarray text 4'))
        
        # self.recursive_update_rendered_objects(self.original_object_copy)

        self.recursive_check_rendered_objects(newobj)

        # self.recursive_update_rendered_objects(self.original_object_copy)

        # self.parent_view_object = self.recursive_build_view_objects(self.original_object_copy)
        # self.recursive_pyqt5_addLayout(self.parent_view_object)

        # # after initialization we have to render once 
        # self.render_view_without_reset()

        # print(self.pyqt5_view_object_parent.toJSON())
        
        return self.parent_view_object.pyqt5_view_objects[0].qt_layout_great_grand_parent

    def recursive_check_rendered_objects(self, obj):
        f = open(str(time.time())+"recursive_check_rendered_objects_json.json", "w")
        f.write(json.dumps(obj, sort_keys=True, indent=4))
        f.close()

        print("file written")
        exit()
        # print(json.dumps(original_object))
        # if(len(original_object['rendered_objects']) > 1):
        #     for obj in original_object['rendered_objects']:
        #         print((obj['code_statements_before_string_evaluation']))
        #         self.recursive_check_rendered_objects(obj)
        # else:
        #     self.recursive_check_rendered_objects(original_object['rendered_objects'][0])

    def recursive_update_rendered_objects(self, original_object):
        if not "qt_constructor" in original_object:
            print('skipping dict_object, no qt_constructor property is set!')
            return False

        # print("original_object['qt_constructor']")
        # print(original_object['qt_constructor'])


        if( 'code_statements_before_string_evaluation' not in original_object):
            code_statements_before_string_evaluation = []
        else:
            code_statements_before_string_evaluation = original_object['code_statements_before_string_evaluation'].copy()

        # print(code_statements_before_string_evaluation)
        if('for' in original_object):

            original_object['rendered_objects'] = []
            
            parts = str(original_object['for']).split(' in ')
            array_var_name_in_for_statement = parts.pop(len(parts)-1)
            parts = parts.pop(0).split(',')
            value_var_name_in_for_statement = parts.pop(0).strip()
            index_var_name_in_for_statement = parts.pop(0).strip()

            evaluated_array_var_len = self.data.get_return_function_by_string(
                "len("+array_var_name_in_for_statement+")",
                code_statements_before_string_evaluation
            )()

            for key in range(0, evaluated_array_var_len):
                
                # since we are in a for loop we have to copy again
                original_object_copy =  copy.deepcopy(original_object)
                # we have to remove the for property now to prevent circular reference
                del original_object_copy['for']
                del original_object_copy['rendered_objects']
               

                # instead we rename the prop to generated_by_for_statement
                original_object_copy['generated_by_for_statement'] = original_object['for']
            
                original_object_copy['array_var_name_in_for_statement'] = array_var_name_in_for_statement
                original_object_copy['value_var_name_in_for_statement'] = value_var_name_in_for_statement
                original_object_copy['index_var_name_in_for_statement'] = index_var_name_in_for_statement
                original_object_copy['index_number_in_for_loop'] = key

                original_object_copy['code_statements_before_string_evaluation'] = (
                    code_statements_before_string_evaluation + 
                    [str(value_var_name_in_for_statement)+
                    ' = '+str(array_var_name_in_for_statement)+
                    '['+str(key)+']']
                    ) 
                
                print("original_object_copy['code_statements_before_string_evaluation']")
                print(original_object_copy['code_statements_before_string_evaluation'])
                print(id(original_object_copy))
                original_object_copy['python_id'] = id(original_object_copy)

                original_object['rendered_objects'].insert(key, original_object_copy)
                # print(value)
        # else: 
        #     original_object['rendered_objects'].append(original_object_copy)

        if('for' in original_object):
            if 'c' in original_object:
                # since we have the rendered_objects[key].c we dont need the c anymore
                del original_object['c']

        if('for' in original_object):
            for rendered_object in original_object['rendered_objects']:
                if 'c' in rendered_object:
                    stmnts = (rendered_object['code_statements_before_string_evaluation']).copy()
                    print("stmnts")
                    print(stmnts)
                    if(type(rendered_object['c']) == list): 
                        for child_original_object in rendered_object['c']:
                            # print(rendered_object['code_statements_before_string_evaluation'])
                            child_original_object['code_statements_before_string_evaluation'] = stmnts
                            child_original_object = self.recursive_update_rendered_objects(child_original_object)
                            
        else:
            if 'c' in original_object:
                if(type(original_object['c']) == list): 
                    for child_original_object in original_object['c']:
                        child_original_object['code_statements_before_string_evaluation'] = code_statements_before_string_evaluation.copy()
                        child_original_object = self.recursive_update_rendered_objects(child_original_object)

        # def  asdf(obj , parentobj):
        #     self.recursive_update_rendered_objects(obj, parentobj)
        # self.foreach_rendered_object(original_object, asdf)

        return original_object

    def foreach_rendered_object(self, object, callback):
    
        # a rendered object is either if the object has a for/rendered_objects array
        # or the object itself
        if('rendered_objects' in object):
            for rendered_object in object['rendered_objects']:
                if 'c' in rendered_object:
                    if(type(rendered_object['c']) == list): 
                        for child_original_object in rendered_object['c']:
                            callback(child_original_object, object)
                            
        else:
            if 'c' in object:
                if(type(object['c']) == list): 
                    for child_original_object in object['c']:
                        callback(child_original_object, object)



    def recursive_build_view_objects(self, original_object, parent_view_object = None):

        if not "qt_constructor" in original_object:
            print('skipping dict_object, no qt_constructor property is set!')
            return False

        view_object = View_object(parent_view_object, original_object, self.data)

        if 'c' in original_object:
            if(type(original_object['c']) == list): 
                for child_original_object in original_object['c']:
                    child_view_object = self.recursive_build_view_objects(
                        child_original_object, 
                        view_object
                        ) 
                    if(child_view_object):
                        view_object.child_view_objects.append(
                            child_view_object
                        )

        return view_object
        
    def recursive_pyqt5_addLayout(self, view_object):
        if(view_object.parent_view_object != None):
            for pyqt5_view_object in view_object.pyqt5_view_objects:
                view_object.parent_view_object.pyqt5_view_objects[0].qt_object.addLayout(
                    pyqt5_view_object.qt_layout_great_grand_parent
                    )

        for child_view_object in view_object.child_view_objects:
            self.recursive_pyqt5_addLayout(child_view_object)

    def recursive_update_for_loops(self, pyqt5_view_object):

        for instance in Pyqt5_view_object.instances:
            if(hasattr(instance, 'pyqt5_view_object_children')):
                print(len(instance.pyqt5_view_object_children))
        # sometimes the array data object loses or gains some children
            # print(len(pyqt5_view_object.pyqt5_view_object_children))
            # if(len(pyqt5_view_object.pyqt5_view_object_children) > 1):
            #     self.append_pyqt5_view_object_children(
            #         pyqt5_view_object,
            #         pyqt5_view_object.dict_object,
            #         pyqt5_view_object.pyqt5_view_object_children)
            #     # for pyqt5_view_object_child in enumerate(pyqt5_view_object.pyqt5_view_object_children):
            #     #     # print(pyqt5_view_object_child)
            #     #     self.recursive_update_for_loops(pyqt5_view_object_child)
            # print(len(pyqt5_view_object.pyqt5_view_object_children))
            # for pyqt5_view_object in pyqt5_view_object.pyqt5_view_object_children:
            #     self.recursive_update_for_loops(pyqt5_view_object)

    def append_pyqt5_view_object_children(
        self,
        pyqt5_view_object_parent,
        dict_object,
        pyqt5_view_object_children):
        if (
            pyqt5_view_object_parent != None and 
            'code_statements_before_string_evaluation' in pyqt5_view_object_parent.dict_object
            ):
            print(pyqt5_view_object_parent.qt_class_name)
            code_statements_before_string_evaluation_parent = pyqt5_view_object_parent.dict_object['code_statements_before_string_evaluation']
        else:
            code_statements_before_string_evaluation_parent = []
        
        parts = str(dict_object['for']).split(' in ')

        array_var_name_in_for = parts.pop(len(parts)-1)
        parts = parts.pop(0).split(',')
        value_var_name_in_for = parts.pop(0).strip()
        index_var_name_in_for = parts.pop(0).strip()
        # print(array_var_name_in_for)

        length = self.data.get_return_function_by_string(
            "len("+array_var_name_in_for+")", 
            code_statements_before_string_evaluation_parent
        )()
        print(str(length)+': length of array_var_name_in_for')
        print(str(len(pyqt5_view_object_children))+': length of actual array')
        if(length == len(pyqt5_view_object_children)):
            return False
        # print(length)
        # exit()

        for key in range(len(pyqt5_view_object_children), length):
            single_for_object = dict_object.copy()
            
            # del single_for_object['for']
            
            single_for_object['code_statements_before_string_evaluation'] = code_statements_before_string_evaluation_parent + [str(value_var_name_in_for)+' = '+str(array_var_name_in_for)+'['+str(key)+']']

            pyqt5_view_object = Pyqt5_view_object(single_for_object, self.data)
            pyqt5_view_object_children.append(pyqt5_view_object)
            # print(value)

        return pyqt5_view_object_children

    def foreach_prop_in_oject(self, dict_object, pyqt5_view_object_parent=None):
        if not "qt_constructor" in dict_object:
            print('skipping dict_object, no qt_constructor property is set!')
            return False

        if('for' in dict_object):

            pyqt5_view_object_children = []
            pyqt5_view_object_children = self.append_pyqt5_view_object_children(
                pyqt5_view_object_parent,
                dict_object,
                pyqt5_view_object_children)
            
        else:
            pyqt5_view_object_children = [Pyqt5_view_object(dict_object, self.data)]


        for pyqt5_view_object in pyqt5_view_object_children:

            # pyqt5_view_object = pyqt5_view_object(object, self.data)

            if(pyqt5_view_object.has_children()):
                for obj in pyqt5_view_object.c:
                    self.foreach_prop_in_oject(obj, pyqt5_view_object)

            
            if(
                # pyqt5_view_object.if_condition_is_true() and since we dont clear on re rendering view, the if has to be considered when evaluating the c 
                pyqt5_view_object_parent != None
                ):

                print(pyqt5_view_object_parent.qt_constructor)

                pyqt5_view_object_parent.qt_object.addLayout(pyqt5_view_object.qt_layout_great_grand_parent)
                # if(pyqt5_view_object.is_qt_layout_class_name()):
                # else:
                #     pyqt5_view_object_parent.qt_object.addWidget(pyqt5_view_object.qt_object)
        if (pyqt5_view_object_parent != None ):
            pyqt5_view_object_parent.pyqt5_view_object_children = pyqt5_view_object_children
        
        return pyqt5_view_object_children

class Synced_data_obj():

    intern_propname_prefix = '_'
    def __init__(self, value):
        self._value = value

    def __setattr__(self, name, value) -> None:
        
        # print('Synced_data_obj.setattr value')
        # print(value)

        if(name.startswith(Synced_data_obj.intern_propname_prefix) == False):
            super().__setattr__(Synced_data_obj.intern_propname_prefix+name, value)
            Pyqt5_app.re_render_view()
        else:
            super().__setattr__(name, value)

    def __getattribute__(self, name):

        # print('Synced_data_obj.getattr name')
        # print(name)

        if(name.startswith(Synced_data_obj.intern_propname_prefix) == False):
            return super().__getattribute__(str(Synced_data_obj.intern_propname_prefix+name))
        else: 
            return super().__getattribute__(name)
        # re rendering is only neccessary when setter is called ... Pyqt5_app.re_render_view()


class Yet_more_nested():
    def __init__(self, id) -> None:
        self.id = id
        self.whichstring = Synced_data_obj('im Yet_more_nested, my id is'+str(self.id))
class Some_deep_nested_shit():
    def __init__(self, id) -> None:
        self.id = id
        self.whichstring = Synced_data_obj('im Some_deep_nested_shit, my id is'+str(self.id))
        self.aha = Synced_data_obj('asdf')
        self.yet_more_nested_array = [
            Yet_more_nested(1),
            Yet_more_nested(2)
        ] 
class Camera(): 
    def __init__(self) -> None:
        self.fps = Synced_data_obj(100) # will be data.cameras.fps.value 
        # self.xyz = ... 
        # self.xyz = ... 
        # self.xyz = ... 
        # and so on

class Data():
    def __init__(self) -> None:
        # self.cameras = []
        # self.textasdf = Synced_data_obj('this is text data')
        # self.textforinput = Synced_data_obj('INIT TEXT')
        self.stringarray = [
            Synced_data_obj('stringarray text 1'),
            Synced_data_obj('stringarray text 2'),
        ]
        # self.some_deep_nested_shits = [
        #  Some_deep_nested_shit(1),
        #  Some_deep_nested_shit(2),
        # ]
        # self.sliderval = Synced_data_obj(1)

    def test_synced_obj(self):
        self.textasdf.value = 'test 1'
        time.sleep(1)
        self.textasdf.value = 'test 2'
        time.sleep(1)
        self.textasdf.value = 'test 3'
        time.sleep(1)
        self.textasdf.value = 'test 4'
        time.sleep(1)

    def random_color(self):
        r = lambda: random.randint(0,255)
        rc = ('#%02X%02X%02X' % (r(),r(),r()))
        return str(rc)

    def get_return_function_by_string(self, string, code_statements_before_string_evaluation=[], code_statements_after_string_evaluation=[]):
        return self.get_function_by_string(string, True, code_statements_before_string_evaluation, code_statements_after_string_evaluation)
        
    def get_void_function_by_string(self, string, code_statements_before_string_evaluation=[], code_statements_after_string_evaluation=[]):
        return self.get_function_by_string(string, False, code_statements_before_string_evaluation, code_statements_after_string_evaluation)
        
    def get_function_by_string(self, string, return_evaluated=False, code_statements_before_string_evaluation=[],code_statements_after_string_evaluation=[]):

        funname = 'fun_'+str((int(time.time())))
        funstr = ''
        funstrlines = []
        funstrlines.append('def '+str(funname)+'(self,event=None,**kvargs):')
        # kvargs => key value args


        funstrlines.append('    for key, value in kvargs.items():')
        funstrlines.append('        exec(key+\'=value\')')           

        for property in dir(self):
            # print(property)
            funstrlines.append('    '+property+'='+'self.'+property)           
            # print(property, ":", value)
        
        for statement in code_statements_before_string_evaluation:
            funstrlines.append('    '+str(statement))

        if(return_evaluated):

            varname = 'var_'+str((int(time.time())))
            funstrlines.append('    '+varname+'='+string)
        else:
            funstrlines.append('    '+string)

            
        for statement in code_statements_after_string_evaluation:
            funstrlines.append('    '+str(statement))

        if(return_evaluated):
            funstrlines.append('    return '+'('+varname+')')

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
    def re_render_view():
        for obj in Pyqt5_app.instances:
            obj.render_view_without_reset()

    def __init__(self):
        self.__class__.instances.append(self)

        super().__init__()

        self.initialize_gui()

    def initialize_gui(self):

        self.setWindowTitle('asdf')
        
        self.data = Data()
        
        # if(True):
        #     self.data.cameras.append(Camera())
        
        self.pyqt5_view = Pyqt5_view(self.data)
        
        self.q_h_box_layout = QHBoxLayout()
        self.render_view_from_json()
        self.setLayout(self.q_h_box_layout)
        self.show()


    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())

    def clear_view(self):
        if(hasattr(self, 'render_qt_layout')):
            self.deleteItemsOfLayout(self.render_qt_layout)
                

    def render_view_without_reset(self):
        self.pyqt5_view.render_view_without_reset()

    def render_view_from_json(self):
        if(hasattr(self, 'pyqt5_view')):
            self.clear_view()
            self.render_view = self.pyqt5_view.get_rendered_view_from_json()
            self.q_h_box_layout.addLayout(self.render_view)


if __name__ == '__main__':

    qApplication = QApplication(sys.argv)

    pyqt5_app = Pyqt5_app()

    sys.exit(qApplication.exec_())

"""
        {
            "qt_constructor": "QVBoxLayout",  
            "for": "obj1, index in some_deep_nested_shits",
            "c": [
                {
                    "qt_constructor":"QLabel",
                    "c":"obj1.whichstring.value"
                },
                {
                    "qt_constructor":"QLabel",
                    "for": "obj2, index in obj1.yet_more_nested_array",
                    "c": "'yet_more_nested_array'+str(obj2.whichstring.value)"
                },
            ]

        },
        lets assume 
        some_deep_nested_shits = [o1,o2,o3]
        and
        yet_more_nested_array = [n1,n2,n3,n4]

        would result in 
        {
            "qt_constructor": "QVBoxLayout",  
            "c": [
                {
                    "qt_constructor":"QLabel",
                    "c":"o1"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n1"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n2"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n3"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n4"
                },
            ]

        },
        {
            "qt_constructor": "QVBoxLayout",  
            "c": [
                {
                    "qt_constructor":"QLabel",
                    "c":"o2"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n1"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n2"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n3"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n4"
                },
            ]

        },
        {
            "qt_constructor": "QVBoxLayout",  
            "c": [
                {
                    "qt_constructor":"QLabel",
                    "c":"o3"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n1"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n2"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n3"
                },
                {
                    "qt_constructor":"QLabel",
                    "c": "n4"
                },
            ]

        },
"""