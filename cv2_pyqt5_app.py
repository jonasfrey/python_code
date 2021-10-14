from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QApplication, QLabel, QVBoxLayout, QPushButton, QSlider
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
import os 
import signal
from PIL import Image, ImageFont, ImageDraw
import functools
import time
import glob

from sip import settracemask


def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


class CaptureThread(QThread):
    
    update_frame = pyqtSignal(np.ndarray, int)

    def __init__(self, capture):
        super(CaptureThread, self).__init__()
        self.capture = capture
        self.frame = None
        self.frame_ok = None
        self.frame_id = 0

    def run(self):
        while True:
            self.frame_ok, self.frame = self.capture.read()
            if self.frame_ok:
                self.frame_id+=1
                self.update_frame.emit(self.frame, self.frame_id)


        self.capture.release()
        cv2.destroyAllWindows()


class Camera_option: 
    def __init__(self, camera):
        self.camera = camera
        self.name = ""
        self.min = None
        self.max = None
        self.step = None
        self.default = None
        self.value = None

    @property
    def value(self):
        return self._value
        
    @value.setter
    def value(self,value):
        #special case/bug, exposure_absolute only works if 
        #exposure_auto is set to
        # exposure_auto=3 (auto)
        # and then
        # exposure_auto=1 (manual)
        #print(self.name)
        if(self.name == "exposure_absolute"):
            self.camera.set_v4l2_option("exposure_auto", 3)
            self.camera.set_v4l2_option("exposure_auto", 1)

        if value != None:
            self.camera.set_v4l2_option(self.name, value)
            
        self._value = value
        return True

class Cv2_frame: 
    def __init__(self, data, camera):
        self.data = data
        self.camera = camera

    #property 
    def name(self):
        return self.__class__.__name__

    @property 
    def frame_id(self):
        return self.camera.frame_id

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, value):
        self._data = self.manipulate_data(value)
        return True

    def manipulate_data(self, data):
        return data 

class Cv2_frame_original(Cv2_frame):
    def __init__(self, data, camera):
        super().__init__(data, camera) # alias for Cv2_frame.init(data)
     
    def manipulate_data(self, data):    
        return data

class Cv2_frame_fancy(Cv2_frame):
    def __init__(self, data, camera):
        super().__init__(data, camera) # alias for Cv2_frame.init(data)
    
    def manipulate_data(self, data):
        # set green and red channels to 0
        try: 
            t = self.camera.frame_id
            w = self.camera.width
        except:
            t = 1
            w = 1

        size = 200
        for i in range(0, size):
            data[:, (t*5+i)%w, 0] = 0+((255/size)*i)

        return data

class Cv2_frame_blue_channel(Cv2_frame):
    def __init__(self, data, camera):
        super().__init__(data, camera) # alias for Cv2_frame.init(data)
 
    def manipulate_data(self, data):
        # set green and red channels to 0
        data[:, :, 1] = 0
        data[:, :, 2] = 0

        cv2.putText(
            data,
            "Cv2_frame_blue_channel",
            (222, 222),
            cv2.FONT_HERSHEY_SIMPLEX, 
            2, 
            (0,255,0),
            2
        ) 
        data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)

        return data


class Cv2_frame_only_red_channel_gray_blurred_light_pixels_only_eroded_dilated(Cv2_frame):
    def __init__(self, data, camera):
        super().__init__(data, camera) # alias for Cv2_frame.init(data)


    def manipulate_data(self, data):
        # set green and red channels to 0
        only_red_channel_mask = data
        
        # set blue and green channels to 0
        only_red_channel_mask[:, :, 0] = 0
        only_red_channel_mask[:, :, 1] = 0

        only_red_channel_gray = cv2.cvtColor(
            only_red_channel_mask,
            cv2.COLOR_BGR2GRAY
            )
        only_red_channel_gray_blurred = cv2.GaussianBlur(
            only_red_channel_gray,
            (
                # int(((pyautogui.position()[1]) / 1080)*50) | 1, 
                # int(((pyautogui.position()[1]) / 1080)*50) | 1
                41,41
            ),
            0
            )
        # cv2.imshow(
        #     'only_red_channel_gray_blurred'+str(self.id),
        #     only_red_channel_gray_blurred
        # )
        only_red_channel_gray_blurred_light_pixels_only = cv2.threshold(
            only_red_channel_gray_blurred, 
            # int(((pyautogui.position()[1]) / 1080)*255),
            18,
            255, 
            cv2.THRESH_BINARY
            )[1]

        only_red_channel_gray_blurred_light_pixels_only_eroded = cv2.erode(
            only_red_channel_gray_blurred_light_pixels_only,
            None,
            iterations=2
            )
        only_red_channel_gray_blurred_light_pixels_only_eroded_dilated = cv2.dilate(
            only_red_channel_gray_blurred_light_pixels_only_eroded,
            None,
            iterations=4
            )

        only_red_channel_gray_blurred_light_pixels_only_eroded_dilated = cv2.putText(
            only_red_channel_gray_blurred_light_pixels_only_eroded_dilated,
            "red chnl gray blurred light pixels eroded dialated",
            (222, 222),
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (222,255,222),
            1
        ) 

        return only_red_channel_gray_blurred_light_pixels_only_eroded_dilated

class Camera:
    instance_counter = 0
    axiss = ["x", "y"]
    def __init__(self, id, app):
        Camera.instance_counter+=1
        self.camera_options = []
        self.app = app
        self.id = id
        self.capture = cv2.VideoCapture(self.id)
        
        self.init_camera_options()

        self.codec = 0x47504A4D # little endian 'MJPG', M->4D,J->4A,P->50, G->47
        self.width = 1208
        self.height = 720
        self.capture.set(cv2.CAP_PROP_FPS, 30.0)
        self.capture.set(cv2.CAP_PROP_FOURCC, self.codec)

        
        self.set_camera_options_to_default()
        self.exposure_auto = 3
        self.exposure_auto = 1
        self.exposure_absolute = 1
        self.axis_index = (Camera.instance_counter - 1) % len(Camera.axiss)

        self.t = 0
        self.fps = 0
        self.frame_this_ts = 0
        self.frame_last_ts = 0
        self.frame_delta_ts = 0
        self.frame = 255 * np.ones((1000,1000,3), np.uint8)
        self.overlay_string = ""
        numpy_zeros = np.zeros([2,2,3],dtype=np.uint8)
        cv2_frame_original = Cv2_frame_original(numpy_zeros.copy(), self)
        self.cv2_frames = [
            cv2_frame_original,
            Cv2_frame_blue_channel(numpy_zeros.copy(), self),
            Cv2_frame_fancy(numpy_zeros.copy(), self),
            Cv2_frame_only_red_channel_gray_blurred_light_pixels_only_eroded_dilated(numpy_zeros.copy(), self)
        ]
        self.cv2_frame_current_index = 0


        self.on_frame_debug_props = [
            "cv2_frame_current_object.name",
            "width", 
            "height", 
            "fps", 
            "axis",
            "frame_delta_ts"
        ]
        self.debug_font_size = 1
        self.file_saved = False

        self.capture_thread = CaptureThread(self.capture)
        # connect its signal to the update_image slot
        self.capture_thread.update_frame.connect(self.update_frame)
        # start the thread
        self.capture_thread.start()


    def switch_axis(self):
        self.axis_index += 1

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, value):
        try:
            for val, index in Camera.axiss: 
                if(val == value):
                    axiss_index = index

            self._axis_index = index 
        except: 
            print("axis invalid, valid is "+" or ".join(Camera.axiss))

        return True

    @property
    def axis_index(self):
        return self._axis_index

    @axis_index.setter
    def axis_index(self, value):
        self._axis_index = (value)%len(Camera.axiss)
        self._axis = Camera.axiss[self.axis_index] 
        return True


    @property
    def cv2_frame_current_index(self):
        return self._cv2_frame_current_index

    @cv2_frame_current_index.setter
    def cv2_frame_current_index(self, value):
        
        self._cv2_frame_current_index = value % len(self.cv2_frames)
        self.cv2_frame_current_object = self.cv2_frames[self._cv2_frame_current_index]

        return True

    def update_frame(self, frame, frame_id):
        
        # for obj in self.cv2_frames:
        #     obj.data = frame.copy()
        self.frame_id = frame_id
        
        self.cv2_frame_current_object.data = frame.copy()

        self.frame = self.cv2_frame_current_object.data

        setattr(self.app, "labelimage_"+str(self.id), self.frame)

        self.frame_this_ts = round(time.time() * 1000)
        self.frame_delta_ts = abs(self.frame_this_ts - self.frame_last_ts)
        self.frame_last_ts = self.frame_this_ts
        self.fps = int(1000/self.frame_delta_ts)
        self.overlay_string = ""
        self.overlay_string += f"width: {self.width}\n"
        self.overlay_string += f"height: {self.height}\n"
        self.overlay_string += f"fps: {self.fps}\n"
        font_size_base = 28

        #n_channels = 3
        #transparent_img = np.zeros((self.width, self.height, n_channels), dtype=np.uint8)

        for (key,value) in enumerate(self.on_frame_debug_props): 
            cv2.putText(
                 #transparent_img,
                 self.frame,
                str(value + " : "+ str(rgetattr(self, value))),
                (font_size_base,font_size_base*3+int(int(key)*(font_size_base * self.debug_font_size))), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                self.debug_font_size, 
                (255,255,255),
                2
            ) 


    def set_camera_options_to_default(self):
        for obj in self.camera_options: 
            obj.value = obj.default
        
    def init_camera_options(self):
        options_string = self.get_v4l2_cam_controls()
        separator = "\n"
        options_arr = str(options_string).split(separator)
        for oline in options_arr:
            
            if(len(oline)) == 0:
                continue

            parts = oline.split(":")
            camera_option = Camera_option(self)
            name, register, datatype = parts[0].split()
            camera_option.name = name
            camera_option.register = register
            camera_option.datatype = datatype
            #print(name, register, datatype)
            
            vals = parts[1].split()
            for val in vals: 
                name, val = val.split("=")
                setattr(camera_option, name, val)

            self.camera_options.append(camera_option)



    def __setattr__(self, name, value):
        
        super(Camera, self).__setattr__(name, value)

        for obj in self.camera_options: 
            if(obj.name == name):
                obj.value = value

    def set_manual_width(self, w):
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        return

    def set_manual_height(self, h):
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        return

    def set_v4l2_options(self, options):
        for op in options:
            self.set_v4l2_option(op[0], op[1])

    def set_v4l2_option(self, option_name, value):
        os.system(
            (
                "v4l2-ctl --device /dev/video"+str(self.id)+" -c "+str(option_name)+"="+str(value)
            ),
        )

    @property 
    def width(self):
        return self._width

    @width.setter 
    def width(self,value):
        self._width = value
        self.set_manual_width(value)
        return True

    @property 
    def height(self):
        return self._height

    @height.setter 
    def height(self,value):
        self._height = value
        self.set_manual_height(value)
        return True
        
    def set_manual_exposure(self, dev_video_id, exposure_time):
        commands = [
         ("v4l2-ctl --device /dev/video"+str(dev_video_id)+" -c exposure_auto=3"),
         ("v4l2-ctl --device /dev/video"+str(dev_video_id)+" -c exposure_auto=1"),
         ("v4l2-ctl --device /dev/video"+str(dev_video_id)+" -c exposure_absolute="+str(exposure_time))
        ]
        for c in commands: 
            stream = os.popen(c)
            output = stream.read()
            os.system(c)

    def do_system_calls_by_array_of_strings(self, array):
        std_out_str = ""
        for c in array: 
            stream = os.popen(c)
            std_out_str += stream.read()

        return std_out_str

    def get_v4l2_cam_controls(self):
        return self.get_v4l2("-l")

    def get_v4l2_cam_info(self):
        return self.get_v4l2("--all")
        
    def get_v4l2(self, arg):
        commands = [
         str("v4l2-ctl --device /dev/video"+str(self.id)+" "+arg),
        ]
        return self.do_system_calls_by_array_of_strings(commands)

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

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.gui_objects = []
        self.cameras = []
        self.setup_gui()

    def setup_gui(self):
        self._window_title = "Cv2 pyqt app"
        self.disply_width = 888
        self.display_height = 500

  
        # create a text label
        self.textLabel = QLabel('Webcams')

        self.main_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        
        self.left_box = QVBoxLayout()
        self.main_layout.addLayout(self.left_box)
        self.right_box = QVBoxLayout()
        self.main_layout.addLayout(self.right_box)
            

        # if(len(self.cameras) > 0):
        #     self.left_box.addWidget(self.image_label1)

        #     def img1_click(event):
        #         self.cameras[0].cv2_frame_current_index += 1

        #         #lambda val: [ self.cameras[0].switch_axis(),self.cameras[1].switch_axis(),  ]

        #     self.image_label1.mousePressEvent = img1_click

        #     button = QPushButton('switch camera axis x <-> y')
        #     self.left_box.addWidget(button)
        #     button.clicked.connect(
        #         lambda val: [ self.cameras[0].switch_axis(),self.cameras[1].switch_axis(),  ]
        #     )
        #     self.left_box.addWidget(self.image_label5)


        #     #self.setLayout(self.main_layout)

        #     self.sliders = []

            
        #     for (obj) in self.cameras[0].camera_options:
        #         if( "int" in obj.datatype): 
        #             textLabel = QLabel(obj.name)
        #             self.right_box.addWidget(textLabel)
        #             slider = QSlider(Qt.Horizontal)
        #             slider.setFocusPolicy(Qt.StrongFocus)
        #             slider.setTickPosition(QSlider.TicksBothSides)
        #             slider.setMinimum(int(obj.min))
        #             slider.setMaximum(int(obj.max))
        #             slider.setSingleStep(1)
        #             #print(obj.name)
        #             path1 = "c1."+str(obj.name)
        #             path3 = "c3."+str(obj.name)

        #             slider.valueChanged.connect(
        #                 lambda val: [ rsetattr(self.data, path1, val), rsetattr(self.data, path3, val) ]
        #             )
        #             #slider.valueChanged.connect(self.get_on_value_changed_function("c1."+str(obj.name)))
        #             self.right_box.addWidget(slider)
        #             self.sliders.append(slider)

        self.setLayout(self.main_layout)

    def setup_cam_gui(self):
        for cam in self.cameras: 
            setattr(self, "label_cam_id"+str(cam.id), "cam_id:"+str(cam.id))
            gui_object_name = "labelimage_"+str(cam.id)
            setattr(self, gui_object_name ,cam.frame)
            gui_object = list(filter(lambda x: x.name == gui_object_name, self.gui_objects))[0]


            setattr(gui_object, 'width',100)
            setattr(gui_object, 'height',100)

            # setattr(self, str(cam.id), "cam_id:"+str(cam.id))

    """
    checks if property name begins with 
    """
    def __setattr__(self,name, value):
        #setattr(self, name, value) #->RecursionError: maximum recursion depth exceeded while calling
        #self.__dict__[name] = value
        super().__setattr__(name, value)
        parts = name.split("_")
        prefix = parts[0]
        name = "_".join(parts)
        
        gui_objects = list(filter(lambda x: x.name == name and x.type == prefix, self.gui_objects))

        if(prefix in Gui_object.types): 
            if(len(gui_objects) > 0):
                gui_object = gui_objects[0]
                gui_object.value = value
            else: 
                gui_object = Gui_object(name, value, prefix)
                self.right_box.addWidget(gui_object.q_object)
                self.gui_objects.append(gui_object)



    @property 
    def window_title(self):
        return self._window_title 
    
    @window_title.setter
    def window_title(self, value):
        self._window_title = value
        self.setWindowTitle(self._window_title)
        

    @property 
    def cameras(self):
        return self._cameras 
    
    @cameras.setter
    def cameras(self, value):
        self._cameras = value
        self.setup_cam_gui()

    def img1clicked(self, click_event):

        print("click")

    def update_image(self, cv_img, id):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        img_label = getattr(self, "image_label"+str(id))
        img_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""

        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(22,22, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    

if __name__=="__main__":


    paths = glob.glob("/dev/video*")

    captures = []
    cameras = []


    qapp = QApplication(sys.argv)

    app = App()
    app.window_title = "CV2 PyQt5 App"

    for path in paths: 
        num = int(path[-1])
        if num == 0:
            continue
        #print(num)
        cap = cv2.VideoCapture(num)
        captures.append(cap)
        capture_possilble = captures[-1].isOpened()
        if capture_possilble: 
            cap.release()
            c = Camera(num, app)
            cameras.append(c)

    app.cameras = cameras


    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app.show()
    sys.exit(qapp.exec_())