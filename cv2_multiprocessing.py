
import numpy as np
import cv2
import os
import multiprocessing 
import time
from PIL import Image, ImageTk
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class Queue_object:
    def __init__(self, name, data):
        self.name = name
        self.data = data

class Shared_process_data:
    def __init__(self):
        self._bool = False
        self.this_ts =0 
        self.delta_ts =0 
        self.last_ts =0 
        self.frame = None

    @property
    def bool(self):
        return self._bool

    @bool.setter
    def bool(self,value):
        self.update_delta_ts()
        # print("bool has changed: "+str(value))
        # print("1000/delta_ts" + str(1000/self.delta_ts))
        self._bool = value
    
    def update_delta_ts(self):
        self.this_ts = round(time.time() * 1000)
        self.delta_ts = abs(self.this_ts - self.last_ts)
        self.last_ts = self.this_ts

class Light: 
    def __init__(self):
        self.is_on = False

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

        self.exposure_absolute = 1

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

        #print("settattr called")
        # setattr(self,name,value)
        # pass

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


    def start_capture_loop(self, num, arr, man_arr, q):
        while(True):
            ret, self.frame = self.capture.read()
            if ret == True:
                self.t += 1
                if(self.t == 100):
                    
                    self.exposure_absolute = 100
                    self.gain = 22
                
                if(self.id == 1):
                    

                    queue_object = Queue_object(
                        str(self.id)+".frame", 
                        self.frame)
                    
                    #print(hasattr(q, "get"))


                    if(q.empty() == False):
                        
                        qdata = q.get()
                    
                        print(qdata.name)

                    q.put(queue_object)

                    #shared_process_data = q.get()[0]
                    # num.value += 2.2
                    # #print(self.frame)
                    # #print(np.asarray(self.frame))
                    # man_arr.append(len(man_arr) % 255)
                    # man_arr.append(len(man_arr) % 255)
                    # man_arr.append(len(man_arr) % 255)
                    # man_arr = np.asarray(self.frame)
                    #print(q.get())
                    #shared_process_data.frame = self.frame
                    #q.put([self.frame])
                    #frame = self.frame
                    #shared_process_data.bool = False
                    #shared_process_data.frame = self.frame
                    #print(shared_process_data)
                # else:
                #     q.put([self.frame])
                    #frame = self.frame
                    #shared_process_data.bool = True

                self.this_ts = round(time.time() * 1000)
                self.delta_ts = abs(self.this_ts - self.last_ts)
                self.last_ts = self.this_ts
                self.fps = int(1000/self.delta_ts)
                self.overlay_string = ""
                self.overlay_string += f"width: {self.width}\n"
                self.overlay_string += f"height: {self.height}\n"
                self.overlay_string += f"fps: {self.fps}\n"
                for (key,value) in enumerate(self.on_frame_debug_props): 
                    cv2.putText(
                        self.frame,
                        str(value + " : "+ str(getattr(self, value))),
                        #"asdf",
                        (20,20+int(int(key)*20)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.5, 
                        (0,255,0),
                        2
                    )                
                # if(self.file_saved == False):
                #     # Filename
                #     print("image saved")
                #     filename = './image_cam_'+str(self.id)+'.jpg'
                #     # Using cv2.imwrite() method
                #     # Saving the image
                #     hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
                #     # value = 42 #whatever value you want to add
                #     # cv2.add(hsv[:,:,2], value, hsv[:,:,2])
                #     # brighter_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
                #     brighter_frame= cv2.add(self.frame,np.array([50.0]))
                #     cv2.imwrite(filename, brighter_frame)
                #     status = cv2.imwrite(filename,self.frame)
                #     print("Image written to file-system : ",status)

                #     self.file_saved = True

                cv2.imshow('frame '+str(self.id),self.frame)

                #print('frame fps: '+str(1000/self.delta_ts))

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else :
                break

        self.capture.release()
        cv2.destroyAllWindows()


class Tkinter_stuff:
    def __init__(self, cam):
        self.cam = cam
        self.window = Tk()
        self.canvas = Canvas(self.window, width=1280, height=720, background='#333')
        self.canvas.grid(row=0, column=0)
        self.canvas.pack(expand=YES, fill=BOTH)
        self.window_destroyed = False
        
        #quit_button_window = self.canvas.create_window(10, 10, anchor='nw', window=quit_button)    


    def init_gui(self):
        
        quit_button = Button(
            text = "X",
            command = lambda : self.q.put((Queue_object("camera_one_is_x", True))),
            anchor = 'w',
            width = 10,
            activebackground = "#33B5E5",
            borderwidth=10,
            background = "#333"
            )
        quit_button.pack()
        
        #quit_button_window = self.canvas.create_window(10, 10, anchor='nw', window=quit_button)    
        quit_button = Button(
            self.window,
            text = "Y",
            command = lambda : self.q.put((Queue_object("camera_one_is_y", True))),
            anchor = 'w',
            width = 10,
            activebackground = "#33B5E5",
            borderwidth=0,
            )
        quit_button.pack()
        # self.window.protocol("WM_DELETE_WINDOW", self.wm_delete_window )

    def start_loop(self, num, arr, man_arr, q):
        self.q = q 
        self.init_gui()
        while self.window_destroyed == False:
            # img = ImageTk.PhotoImage(Image.open("./image_cam_1.jpg"))      
            # print(img)
            # self.canvas.create_image(20,20, anchor=NW, image=img)   
            #print(q.get())
            
            # frame = q.get()[0]
            queue_object = q.get()


            
            # print(q_data)
            #print(queue_object.name)
            
            if(queue_object.name == "1.frame"):
                data = np.copy(queue_object.data)
                img = ImageTk.PhotoImage(image=Image.fromarray(data))
                self.canvas.create_image(1,1, anchor="nw", image=img)
            else: 
                q.put(queue_object)
                # print(queue_object.name)
            # if(len(q_data)> 0):
            # q.task_done()
            # try: 
            # # if(queue_object): 
            # except:
            #     print("error")

            self.window.update()
        
            

            time.sleep(0.005)
            # try:
            # except:
            #     break

    # def wm_delete_window(self):
    #     self.window_destroyed = True


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This is an example button')
        button.move(100,70)
        button.clicked.connect(self.on_click)
        
        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')


if __name__ == '__main__':

        app = QApplication(sys.argv)
        ex = App()


        shared_process_data = Shared_process_data()
        cam1 = Camera(1)
        cam3 = Camera(3)
        # tkinter_stuff = Tkinter_stuff(cam1)
        q = multiprocessing.Queue()
        
        num = multiprocessing.Value('d', 11.2)
        arr = multiprocessing.Array('i', [0])
        man_arr = multiprocessing.Manager().list()
        #frame = []
        # p3= multiprocessing.Process(target = tkinter_stuff.start_loop, args=(num, arr, man_arr, q,))
        p1= multiprocessing.Process(target = cam1.start_capture_loop, args=(num, arr, man_arr, q,))
        p2= multiprocessing.Process(target = cam3.start_capture_loop, args=(num, arr, man_arr, q,))
        p1.start() 
        p2.start()
        # p3.start()
        p1.join()
        p2.join()

        print(cam1.frame)

        sys.exit(app.exec_())




