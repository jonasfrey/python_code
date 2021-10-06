import cv2
import pyautogui
import time
import colorsys
from tkinter import * 
import numpy as np

class Rect: 
    def __init__(self, x,y,w,h,fill,outline):
        self._w = w
        self._h = h
        self._x = x
        self._y = y
        self.x = x
        self.y = y
        self.fill = fill
        self.outline = outline
    

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value
        return True

    @property
    def h(self):
        return self._h
    
    @h.setter
    def h(self, value):
        self._h = value
        return True

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._x1 = value
        self._x2 = self._x + self._w
        return True
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._y1 = value
        self._y2 = self._y1 + self._h
        return True

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value
        self._x2 = self._x1 + self._w
        return True

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        self._h = value
        self._y2 = self._y1 + self._h
        return True


    @property
    def x1(self):
        return self._x1
    @property
    def x2(self):
        return self._x2
    @property
    def y1(self):
        return self._y1
    @property
    def y2(self):
        return self._y2




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



class Point_2_d:
    def __init__(self, x, y): 
        self._x = x
        self._y = y

    @property
    def x(self):
        """I'm the 'x' property."""
        print("getter of x called")
        return self._x

    @x.setter
    def x(self, value):
        print("setter of x called")
        self._x = value

    @x.deleter
    def x(self):
        print("deleter of x called")
        del self._x

    @property
    def y(self):
        """I'm the 'y' property."""
        print("getter of y called")
        return self._y

    @y.setter
    def y(self, value):
        print("setter of y called")
        self._y = value

    @y.deleter
    def y(self):
        print("deleter of y called")
        del self._y




#capture = cv2.VideoCapture("http://11.23.58.105:8080/video")
#capture = cv2.VideoCapture("http://11.23.58.102:8080/video")
capture1 = cv2.VideoCapture(1)
capture2 = cv2.VideoCapture(3)

capture1.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
capture1.set(cv2.CAP_PROP_EXPOSURE, -7.0)

pen = Pen()

delta_n_white_pix = 0
last_n_white_pix = None
current_n_white_pix = 0


window = Tk()
    
canvas = Canvas(window, width=1920, height=1080, background='#333')
canvas.grid(row=0, column=0)
canvas.create_line(100,100, 300,100, 200,300, 100,100, fill="red", width=5)
color_range_rects = []
# window.mainloop() -> manual render window.update()

#canvas.create_line(100,100, 300,100, 200,300, 100,100, fill="red", width=5)
for hue in range(0,180):
    w = 2
    x = hue*w
    y = 0
    x2 = (hue*w)+w
    h = 30
    y2 = h
    cur_rgb_col = colorsys.hsv_to_rgb((1/(180*2))*x,1,1)
    cur_hex_col = (
        hex(int(cur_rgb_col[0]*255))[2:].zfill(2)+ 
        hex(int(cur_rgb_col[1]*255))[2:].zfill(2)+ 
        hex(int(cur_rgb_col[2]*255))[2:].zfill(2)
        )
    color_range_rects.append(
        Rect(x,y,w,h,"#"+str(cur_hex_col), "")
    )
    #canvas.create_rectangle(x, y, x2, y2,outline="", fill="#"+str(cur_hex_col))


mouse_rect = Rect(180,0,2,30,"", "#000")

t = 0


unnormalized_max_h = 180
unnormalized_max_s = 255
unnormalized_max_v = 255
unnormalized_max_l = 255

frame_ts_ms = 0
last_frame_ts_ms = 0
last_frame_ts_ms_frame_ts_ms_delta_ms = 0
while(True):
    t+=1
    frame_ts_ms = round(time.time() * 1000)
    last_frame_ts_ms_frame_ts_ms_delta_ms = abs(frame_ts_ms-last_frame_ts_ms) 
    last_frame_ts_ms = frame_ts_ms
    print("last_frame_ts_ms_frame_ts_ms_delta_ms: "+str(last_frame_ts_ms_frame_ts_ms_delta_ms))

    canvas.delete("all")

    #mouse_rect.x = (t % 100)
    rects = color_range_rects+[mouse_rect]
    for obj in rects:
        canvas.create_rectangle(
        obj.x1,
        obj.y1,
        obj.x2,
        obj.y2,
        outline=obj.outline,
        fill=obj.fill
        )

    _, frame1 = capture1.read()
    _, frame2 = capture2.read()

    frame1_hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    frame2_hsv = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

    frame1_hsl = cv2.cvtColor(frame1, cv2.COLOR_BGR2HLS)
    frame2_hsl = cv2.cvtColor(frame2, cv2.COLOR_BGR2HLS)



        # blue arduino led 
    hue_plus_minus = 1/10 # plus minus 1/10 of circle
    hue_base = 2/3
    hue_base = (pyautogui.position()[1]) / 1080; 


    low_h = (hue_base-(1/10)) - hue_plus_minus # blue starts at two third, 120degrees(if full = 360deg) -(+- certain number) 1/3 of circle
    low_s = 0 # we want full saturation 
    low_v = 0.9 # we start at 1/8 , very dark color almost black
    
    high_h = (hue_base-(1/10)) + hue_plus_minus # blue ends at 240 plus certain degrees
    high_s = 0.05 # we want full saturation 
    high_v = 1 # we end at 8/8 ,so full color green

    low_h = (hue_base-(1/10)) - hue_plus_minus # blue starts at two third, 120degrees(if full = 360deg) -(+- certain number) 1/3 of circle
    low_s = 0 # we want full saturation 
    low_v = 1 # we start at 1/8 , very dark color almost black
    
    high_h = (hue_base-(1/10)) + hue_plus_minus # blue ends at 240 plus certain degrees
    #high_s = 0.2 # we want full saturation 
    high_v = 1 # we end at 8/8 ,so full color green
    high_s = (pyautogui.position()[0]) / 1920; 


    hue_base = 2/3

    hue_plus_minus = ((pyautogui.position()[1]) / 1080)


    low_h = ((pyautogui.position()[0]) / (1920*2)) - (hue_plus_minus/2) # blue starts at two third, 120degrees(if full = 360deg) -(+- certain number) 1/3 of circle
    low_s = 0  
    low_l = 0

    high_h = ((pyautogui.position()[0]) / (1920*2)) + (hue_plus_minus/2) # blue start
    high_s = 1 
    high_l = 1 

    #x -> hue
    mouse_rect.x = ((pyautogui.position()[0]) / (1920*2)) * 360
    #y -> hue plus minus
    mouse_rect.w = ((pyautogui.position()[1]) / 1080) * 360

    capture2.set(cv2.CAP_PROP_EXPOSURE, ((pyautogui.position()[0]) / (1920*2))*40) 
    capture1.set(cv2.CAP_PROP_EXPOSURE, ((pyautogui.position()[0]) / (1920*2))*40) 

    mask_frame1_hue = cv2.inRange(
        frame1_hsl,
            (
            unnormalized_max_h * low_h,
            unnormalized_max_s * low_s,
            unnormalized_max_l * low_l
            ),
            (
            unnormalized_max_h * high_h,
            unnormalized_max_s * high_s,
            unnormalized_max_l * high_l
            )
        )

    cv2.imshow('mask_frame1_hue', mask_frame1_hue)
    cv2.imshow('f1', frame1)
    

    hue_base = 2/3
    hue_plus_minus = 1/3 # plus minus 1/10 of circle

    #trying to get only the bright pixels
    # low_h = ((pyautogui.position()[1]) / 1080)-0.1  # blue starts at two third, 120degrees(if full = 360deg) -(+- certain number) 1/3 of circle
    # low_s = 0 # we want full saturation 
    # low_l = 0.5

    
    # high_h = ((pyautogui.position()[1]) / 1080)+0.1 # blue ends at 240 plus certain degrees    
    # high_l = 1 # we end at 8/8 ,so full color green
    # high_s = 1; 

    # print("low_h: "+str(low_h))
    # print("high_h: "+str(high_h))

    low_h =0.492;  
    low_s = 0 
    low_l = 0.5

    
    high_h = 0.692    
    high_l = 1 
    high_s = 1; 
    mask1 = cv2.inRange(
        frame1_hsl,
            (
            unnormalized_max_h * low_h,
            unnormalized_max_s * low_s,
            unnormalized_max_l * low_l
            ),
            (
            unnormalized_max_h * high_h,
            unnormalized_max_s * high_s,
            unnormalized_max_l * high_l
            )
        )

    rgb_mask_blue_frame_1 = cv2.inRange(
        frame1,
            (
            255 * 00,
            255 * 0.5,
            255 * 0.5
            ),
            (
            255 * 0,
            255 * 1,
            255 * 1
            )
        )
    #cv2.imshow('rgb_mask_blue_frame_1', rgb_mask_blue_frame_1)
    
    current_n_white_pix = np.sum(mask1 == 255)
    if(last_n_white_pix == None):
        last_n_white_pix = current_n_white_pix

    delta_n_white_pix = abs(current_n_white_pix-last_n_white_pix)

    if(delta_n_white_pix > 2000):
        pen.light_on = not(pen.light_on)

    last_n_white_pix = current_n_white_pix

    #print("delta_n_white_pix: "+str(delta_n_white_pix))

    res = cv2.bitwise_and(frame1,frame1,mask = mask1)


    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    # cv2.circle(frame1, maxLoc, 5, (255, 0, 0), 2)
    # # display the results of the naive attempt
    # cv2.imshow("Naive", frame1)

    # only_white=gray
    # only_white[320:,:]=0
    # only_white[:,230:]=0


    # cv2.imshow("only_white", only_white)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    cv2.circle(frame1, maxLoc, 2, (255, 0, 0), 2)
    #cv2.imshow("Robust", frame1)


    #cv2.imshow('test_window_name_frame', mask1)
    #cv2.imshow('test_window_name_frame', res)

    window.update()

    if(cv2.waitKey(1) == ord("q")):
        break

capture1.release()
capture2.release()

cv2.destroyAllWindows()


