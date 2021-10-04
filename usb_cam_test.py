import cv2
import pyautogui
import time
import os
import numpy as np

from tkinter import * 


class Point_2_d:
    def __init__(self, x, y): 
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        del self._x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @y.deleter
    def y(self):
        del self._y



class Pen:
    def __init__(self):
        self.point_2_d = Point_2_d(0,0)
        self._light_on = False
        self.last_light_on_ts_ms = 0
        self.current_light_on_ts = 0
        self.current_light_on_last_light_on_delta_ts_ms = 0
        self.multiple_light_on_threshhold_ms = 100
        self.multiple_light_on_counter = 0
        self.on_2_click_function_name_aliases = [
            "on_double_click",
            "on_double_ligth"
        ]
        self.tkinter_points = []
        # self.on_3_click_function_name_aliases = [
        #     "on_triple_click",
        #     "on_triple_ligth"
        # ]


    @property 
    def light_on(self): 
        return self._light_on

    @light_on.setter
    def light_on(self, value):
        if(self.light_on != value and value == True):
            print("click!!!")
            self.current_light_on_ts = round(time.time() * 1000)
            self.current_light_on_last_light_on_delta_ts_ms = abs(
                self.current_light_on_ts - self.last_light_on_ts_ms
            )
            if(self.current_light_on_last_light_on_delta_ts_ms < self.multiple_light_on_threshhold_ms):
                self.multiple_light_on_counter+=1
            else: 
                self.multiple_light_on_counter = 0

            if(self.multiple_light_on_counter == 2):
                for string in self.on_2_click_function_name_aliases: 
                    if(hasattr(self, string)):
                        fun = getattr(self, string)
                        if(callable(fun)): 
                            fun()

            self.last_light_on_ts_ms = self.current_light_on_ts
        
        self._light_on = value




# seems not to work, cv2 is overwriting the settings ... 
# commands = []
# commands.append("v4l2-ctl -d /dev/video1 -c exposure_auto=1")
# commands.append("v4l2-ctl -d /dev/video1 -c exposure_absolute=1")
# commands.append("v4l2-ctl -d /dev/video1 -c exposure_auto_priority=0")
# command = " && ".join(commands)
# print(command)
# os.system(command)

pen = Pen()

window = Tk()
canvas = Canvas(window, width=1920, height=1080, background='#333')
canvas.grid(row=0, column=0)
canvas.create_line(100,100, 300,100, 200,300, 100,100, fill="red", width=3)


class Mask:
    def __init__(
            self,
            frame,
            name,
            low_h_normalized,
            low_s_normalized,
            low_l_normalized,
            high_h_normalized,
            high_s_normalized,
            high_l_normalized
            ): 

        self.h_max = 180
        self.s_max = 255
        self.l_max = 255

        self.data = np.array([])
        self.name = name 
        self.color_space = "hsl"
        self.hsl_original_data = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
        self.low_h_normalized = low_h_normalized
        self.low_s_normalized = low_s_normalized
        self.low_l_normalized = low_l_normalized
        self.high_h_normalized = high_h_normalized
        self.high_s_normalized = high_s_normalized
        self.high_l_normalized = high_l_normalized
        self.set_data()

    def low_and_high_set(self): 
        return (
            hasattr(self, "low_h") and
            hasattr(self, "low_s") and
            hasattr(self, "low_l") and
            hasattr(self, "high_h") and
            hasattr(self, "high_s") and
            hasattr(self, "high_l") 
        )
    def set_data(self):
        if(
            self.low_and_high_set()
        ):
            self.data = cv2.inRange(
                self.hsl_original_data,
                (
                    self.low_h,
                    self.low_s,
                    self.low_l,
                ),
                (
                    self.high_h,
                    self.high_s,
                    self.high_l,
                )
            )

    @property
    def low_h_normalized(self):
        return self._low_h_normalized

    @low_h_normalized.setter
    def low_h_normalized(self, value):
        self._low_h_normalized = value
        self.low_h = self._low_h_normalized * self.h_max
        self.set_data()
        return True

    @property
    def low_s_normalized(self):
        return self._low_s_normalized

    @low_s_normalized.setter
    def low_s_normalized(self, value):
        self._low_s_normalized = value
        self.low_s = self._low_s_normalized * self.s_max
        self.set_data()
        return True

    @property
    def low_l_normalized(self):
        return self._low_l_normalized

    @low_l_normalized.setter
    def low_l_normalized(self, value):
        self._low_l_normalized = value
        self.low_l = self._low_l_normalized * self.l_max
        self.set_data()
        return True


    @property
    def high_h_normalized(self):
        return self._high_h_normalized

    @high_h_normalized.setter
    def high_h_normalized(self, value):
        self._high_h_normalized = value
        self.high_h = self._high_h_normalized * self.h_max
        self.set_data()
        return True

    @property
    def high_s_normalized(self):
        return self._high_s_normalized

    @high_s_normalized.setter
    def high_s_normalized(self, value):
        self._high_s_normalized = value
        self.high_s = self._high_s_normalized * self.s_max
        self.set_data()
        return True

    @property
    def high_l_normalized(self):
        return self._high_l_normalized

    @high_l_normalized.setter
    def high_l_normalized(self, value):
        self._high_l_normalized = value
        self.high_l = self._high_l_normalized * self.l_max
        self.set_data()
        return True


class Camera:
    def __init__(
            self,
            axis, 
            id
            ): 


        #print("fps: "+str(fps))


        self.axis = axis
        self.id = id

        self.light_detected = False
        self.light_detected_coordinates = (0,0)


        self.last_bigger_mask = np.array([[]])
        self.bigger_mask = np.array([[]])
        self.last_bigger_mask_color = ""

        self.frame_ts_ms = 0
        self.last_frame_ts_ms = 0
        self.last_frame_ts_ms_frame_ts_ms_delta_ms = 0
        self.fps = 0

        #capture = cv2.VideoCapture("http://11.23.58.105:8080/video")
        #capture = cv2.VideoCapture("http://11.23.58.102:8080/video")
        #capture = cv2.VideoCapture(1)
        self.capture = cv2.VideoCapture(self.id)
        # print(cv2.getBuildInformation())
        self.capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        self.capture.set(cv2.CAP_PROP_EXPOSURE, 2)
        self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        width = 1280
        height = 720
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        # $ v4l2-ctl -d /dev/video3 -l
        #
        #                      brightness 0x00980900 (int)    : min=-64 max=64 step=1 default=0 value=0
        #                        contrast 0x00980901 (int)    : min=0 max=64 step=1 default=32 value=32
        #                      saturation 0x00980902 (int)    : min=0 max=128 step=1 default=75 value=75
        #                             hue 0x00980903 (int)    : min=-40 max=40 step=1 default=0 value=0
        #  white_balance_temperature_auto 0x0098090c (bool)   : default=1 value=1
        #                           gamma 0x00980910 (int)    : min=72 max=500 step=1 default=120 value=72
        #                            gain 0x00980913 (int)    : min=0 max=100 step=1 default=0 value=0
        #            power_line_frequency 0x00980918 (menu)   : min=0 max=2 default=2 value=2
        #       white_balance_temperature 0x0098091a (int)    : min=2800 max=6500 step=1 default=4600 value=4600 flags=inactive
        #                       sharpness 0x0098091b (int)    : min=0 max=6 step=1 default=3 value=3
        #          backlight_compensation 0x0098091c (int)    : min=0 max=2 step=1 default=1 value=1
        #                   exposure_auto 0x009a0901 (menu)   : min=0 max=3 default=3 value=1
        #               exposure_absolute 0x009a0902 (int)    : min=1 max=5000 step=1 default=157 value=5000
        #          exposure_auto_priority 0x009a0903 (bool)   : default=0 value=0

    def detect_fps(self):
        #detect fps
        self.last_frame_ts_ms_frame_ts_ms_delta_ms = abs(self.frame_ts_ms-self.last_frame_ts_ms) 
        self.last_frame_ts_ms = self.frame_ts_ms
        self.fps = 1000.0/self.last_frame_ts_ms_frame_ts_ms_delta_ms

    def do_capture(self):
        _, self.frame = self.capture.read()
        self.frame_ts_ms = round(time.time() * 1000)
        self.detect_fps()


        self.masks = self.get_masks()

        blue_mask = list(filter(lambda x: x.name == "blue", self.masks))[0]
        red_mask1 = list(filter(lambda x: x.name == "red1", self.masks))[0]
        red_mask2 = list(filter(lambda x: x.name == "red2", self.masks))[0]

        blue_mask_data = blue_mask.data 
        red_mask_data = red_mask1.data + red_mask2.data

        # blue_mask_bitwise_and_frame = cv2.bitwise_and(self.frame,self.frame,mask = blue_mask_data)
        # cv2.imshow('blue_mask', blue_mask_data)
        # cv2.imshow('blue_mask_bitwise_and_frame', blue_mask_bitwise_and_frame)

        # red_mask_bitwise_and_frame = cv2.bitwise_and(self.frame,self.frame,mask = red_mask_data)
        # cv2.imshow('red_mask', red_mask_data)
        # cv2.imshow('red_mask_bitwise_and_frame', red_mask_bitwise_and_frame)

        blue_mask_data_sum = np.sum(blue_mask_data == 255)
        red_mask_data_sum = np.sum(red_mask_data == 255)

        if(blue_mask_data_sum > red_mask_data_sum):
            #print("bigger_mask => blue")
            self.bigger_mask = blue_mask_data
            self.bigger_mask_color = "blue"

        else: 
            #print("bigger_mask => red")
            self.bigger_mask = red_mask_data
            self.bigger_mask_color = "red"

        #best would be if red and blue changes every frame. 
        # with that we could bitwise and both masks blue and red 
        # and be pretty sure, it is our custom pen! 
        # unless a police car with flashing blue red light drives by the window
        #  and causes a missinterpretation of the frame XD
        self.last_mask_different_color = False
        if(self.bigger_mask_color != self.last_bigger_mask_color):
            self.last_mask_different_color = True
            # print("last mask was different color: 1")
        else: 
            self.last_mask_different_color = True
            # print("last mask was different color: 0")

        self.bigger_mask_bitwise_and_last_bigger_mask = cv2.bitwise_and(
            self.bigger_mask,
            self.bigger_mask,
            mask=self.last_bigger_mask)

        self.last_bigger_mask = self.bigger_mask


        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(
            self.bigger_mask_bitwise_and_last_bigger_mask
            )

        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(
            gray
            )

        cv2.circle(self.frame, maxLoc, 2, (255, 0, 0), 2)

        self.bigger_mask_bitwise_and_last_bigger_mask_sum = np.sum(
            self.bigger_mask_bitwise_and_last_bigger_mask == 255
            )
        self.click_treshhold = 50
        
        if(self.bigger_mask_bitwise_and_last_bigger_mask_sum > 50):
            print("light on!!!!")
            self.light_detected = True
            self.light_detected_coordinates = maxLoc
            
        self.light_detected = True
        self.light_detected_coordinates = maxLoc
        
        #print(maxLoc)
        #print("bigger_mask_bitwise_and_last_bigger_mask_sum: "+str(bigger_mask_bitwise_and_last_bigger_mask_sum))
        
        cv2.imshow('original_frame_cam_id_'+str(self.id), self.frame)
        #cv2.imshow('test_window_name_frame2', frame2)
        
        self.last_bigger_mask_color = self.bigger_mask_color

    def get_masks(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        hsl = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HLS)

        blue_mask = Mask(
            self.frame, 
            "blue", 
            1/3, 0.04, 0.04, # low h s l all normalized
            2/3, 1, 1 # high h s l all normalized
        )

        red_mask_1 = Mask(
            self.frame, 
            "red1", 
            0, 0.04, 0.04, # low h s l all normalized
            1/6, 1, 1 # high h s l all normalized
        )
        red_mask_2 = Mask(
            self.frame, 
            "red2", 
            5/6, 0.04, 0.04, # low h s l all normalized
            6/6, 1, 1 # high h s l all normalized
        )

        return [blue_mask, red_mask_1, red_mask_2] 

cam_x = Camera("x", 1)
cam_y = Camera("y", 3)

while(True):


    canvas.delete("all")
    if(len(pen.tkinter_points) > 4):
        canvas.create_line(pen.tkinter_points, fill="red", width=3)


    cam_x.do_capture()
    cam_y.do_capture()

    if(cam_x.light_detected and cam_y.light_detected):
        pen.light_on = True
        pen.point_2_d.x = cam_x.light_detected_coordinates[0]
        pen.point_2_d.y = cam_y.light_detected_coordinates[0] ## we still have to take the x coord, since the camera is turned 90 degrees but not the image
        
        pen.tkinter_points.append(pen.point_2_d.x)
        pen.tkinter_points.append(pen.point_2_d.y)

    else: 
        pen.light_on = False

    window.update()

    if(cv2.waitKey(1) == ord("q")):
        break

cam_x.capture.release()
cam_y.capture.release()

cv2.destroyAllWindows()
