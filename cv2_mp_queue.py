import numpy as np
import cv2
import multiprocessing 
import time
from tkinter import * 
from PIL import Image, ImageTk

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
class Camera:
    def __init__(self, id):
        self.id = id
        self.frame = None
        self.capture = cv2.VideoCapture(self.id)
        self.codec = 0x47504A4D # little endian 'MJPG', M->4D,J->4A,P->50, G->47
        self.width = 1208
        self.height = 720
        self.capture.set(cv2.CAP_PROP_FPS, 30.0)
        self.capture.set(cv2.CAP_PROP_FOURCC, self.codec)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        self.capture.set(cv2.CAP_PROP_EXPOSURE, 1)
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

    def get_frame(self):
        return self.frame


    def start_capture_loop(self, num, arr, man_arr, q):
        while(True):
            ret, self.frame = self.capture.read()
            if ret == True:
                
                if(self.id == 1):
                    q.put([self.frame])
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
        
        # self.window.protocol("WM_DELETE_WINDOW", self.wm_delete_window )

    def start_loop(self, num, arr, man_arr, q):
        while self.window_destroyed == False:
            # img = ImageTk.PhotoImage(Image.open("./image_cam_1.jpg"))      
            # print(img)
            # self.canvas.create_image(20,20, anchor=NW, image=img)   
            frame = q.get()[0]

            img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(1,1, anchor="nw", image=img)
            
            self.window.update()
        
            

            time.sleep(0.01)
            # try:
            # except:
            #     break

    # def wm_delete_window(self):
    #     self.window_destroyed = True


if __name__ == '__main__':

        shared_process_data = Shared_process_data()
        cam1 = Camera(1)
        cam3 = Camera(3)
        tkinter_stuff = Tkinter_stuff(cam1)
        q = multiprocessing.Queue()
        frame = []
        
        num = multiprocessing.Value('d', 11.2)
        arr = multiprocessing.Array('i', [0])
        man_arr = multiprocessing.Manager().list()

        p3= multiprocessing.Process(target = tkinter_stuff.start_loop, args=(num, arr, man_arr, q,))
        p1= multiprocessing.Process(target = cam1.start_capture_loop, args=(num, arr, man_arr, q,))
        p2= multiprocessing.Process(target = cam3.start_capture_loop, args=(num, arr, man_arr, q,))
        p1.start() 
        p2.start()
        p3.start()
        p1.join()
        p2.join()

        # window = Tk()
        # canvas = Canvas(window, width=1280, height=720, background='#333')
        # canvas.grid(row=0, column=0)
        # canvas.pack(expand=YES, fill=BOTH)
        # while True: 

        #     # frame = q.get()[0]
        #     img = ImageTk.PhotoImage(image=Image.fromarray(frame))
        #     canvas.create_image(1,1, anchor="nw", image=img)
            
        #     window.update()






        # p3.join()


        print(cam1.frame)