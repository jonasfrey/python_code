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

def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


class CaptureThread(QThread):
    
    update_frame = pyqtSignal(np.ndarray)

    def __init__(self, capture):
        super(CaptureThread, self).__init__()
        self.capture = capture
        self.frame = None
        self.frame_ok = None

    def run(self):
        while True:
            self.frame_ok, self.frame = self.capture.read()
            if self.frame_ok:
                self.update_frame.emit(self.frame)


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


class Camera:
    def __init__(self, id):
        self.camera_options = []
        self.on_update_frame = None
        self.id = id
        self.frame = None
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
        self.axis = "x"

        self.t = 0
        self.fps = 0
        self.this_ts = 0
        self.last_ts = 0
        self.delta_ts = 0
        self.overlay_string = ""
        self.on_frame_debug_props = [
            "width", 
            "height", 
            "fps", 
        ]
        self.file_saved = False


        self.capture_thread = CaptureThread(self.capture)
        # connect its signal to the update_image slot
        self.capture_thread.update_frame.connect(self.update_frame)
        # start the thread
        self.capture_thread.start()


    def update_frame(self, frame):
        self.frame = frame
        self.frame = self.frame
        cv_img = self.frame
        width, height, prop = cv_img.shape
        texted_cv_img = cv2.putText(img=np.copy(cv_img),
         text=str(self.axis)+"_cam",
         org=(int(width/2),
            int(height/2)),
        fontFace=3,
         fontScale=1,
         color=(0,255,128), 
         thickness=5)

        self.frame = cv2.addWeighted(cv_img, 0.5, texted_cv_img, 0.5, 1.0)
        update_frame_function = getattr(self, "on_update_frame")
        if update_frame_function != None: 
            update_frame_function(self)
            

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

class App(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label1 = QLabel(self)
        self.image_label1.mousePressEvent = self.img1clicked
        self.image_label1.resize(self.disply_width, self.display_height)
     
        self.image_label3 = QLabel(self)
        self.image_label3.resize(self.disply_width, self.display_height)
        
        image_cam_1_overlay = []
        image_cam_3_overlay = []
        # create a text label
        self.textLabel = QLabel('Webcams')


        self.main_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        
        self.left_box = QVBoxLayout()
        self.main_layout.addLayout(self.left_box)
        self.right_box = QVBoxLayout()
        self.main_layout.addLayout(self.right_box)

        self.left_box.addWidget(self.image_label1)
        self.left_box.addWidget(self.image_label3)


        #self.setLayout(self.main_layout)

        image_cam_1_overlay = []
        image_cam_3_overlay = []

        self.sliders = []

        
        for (obj) in self.data.c1.camera_options:
            if( "int" in obj.datatype): 
                textLabel = QLabel(obj.name)
                self.right_box.addWidget(textLabel)
                slider = QSlider(Qt.Horizontal)
                slider.setFocusPolicy(Qt.StrongFocus)
                slider.setTickPosition(QSlider.TicksBothSides)
                slider.setMinimum(int(obj.min))
                slider.setMaximum(int(obj.max))
                slider.setSingleStep(1)
                #print(obj.name)
                path = "c1."+str(obj.name)
                print(path)
                slider.valueChanged.connect(
                    lambda val: rsetattr(self.data, path, val)
                )
                #slider.valueChanged.connect(self.get_on_value_changed_function("c1."+str(obj.name)))
                self.right_box.addWidget(slider)
                self.sliders.append(slider)

        self.setLayout(self.main_layout)


    def img1clicked(self, click_event):

        print("click")

    def update_image(self, cv_img, id):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        img_label = getattr(self, "image_label"+str(id))
        img_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        #cv_img = cv_img * self.slider.value()
        # im = Image.fromarray(cv_img)
        # fontpath = "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"
        # font = ImageFont.truetype(fontpath, 25)
        # draw = ImageDraw.Draw(im)
        # draw.text((0,0), "This is a test", (255,255,0), font=font)
        # cv_img = np.asarray(draw)


        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    

class Data: 
    def __init__(self):
        self.initialized = True

if __name__=="__main__":
    c1 = Camera(1)
    c3 = Camera(3)
    data = Data()
    data.c1 = c1
    data.c3 = c3
    app = QApplication(sys.argv)
    a = App(data)

    def cam_on_update_frame(self):

        a.update_image(self.frame, self.id)
    
    c1.on_update_frame = cam_on_update_frame
    c3.on_update_frame = cam_on_update_frame

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    a.show()
    sys.exit(app.exec_())