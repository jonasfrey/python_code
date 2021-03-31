import hid
#import win32api, win32con
import pyautogui
import time
import json 

pyautogui.moveTo(100, 150)



#Bus 003 Device 044: ID 056a:0374 Wacom Co., Ltd CTL-4100 [Intuos (S)]
VENDOR_ID = 0x056a # 
PRODUCT_ID = 0x0374 # 

device = hid.device()
device.open(VENDOR_ID, PRODUCT_ID)
print('Connected to ADU{}\n'.format(PRODUCT_ID))


print("Manufacturer: %s" % device.get_manufacturer_string())
print("Product: %s" % device.get_product_string())
print("Serial No: %s" % device.get_serial_number_string())

class Input_Value: 
    def __init__(self, value = False, bit_value = 0b00000000):
        self.value = value
        self.bit_value = bit_value

class Pen:
    def __init__(self):
        self.hovered_far = Input_Value(False, 0b01000000)
        self.hovered_close = Input_Value(False, 0b00100000)
        self.touch = Input_Value(False, 0b00000001)
        self.button_tip = Input_Value(False, 0b00000010)
        self.button_pipe = Input_Value(False, 0b00000100)

    def set_input_values(self, bin_num):
        
        self.touch.value = (bin_num & self.touch.bit_value) > 0
        self.button_tip.value = (bin_num & self.button_tip.bit_value) > 0
        self.button_pipe.value = (bin_num & self.button_pipe.bit_value) > 0


class Tablet:
    def __init__(self, pen):
        self.button_left_rounded = Input_Value(False, 0b00000001)
        self.button_left_rectangular = Input_Value(False, 0b00000010)
        self.button_right_rectangular = Input_Value(False, 0b00000100)
        self.button_right_rounded = Input_Value(False, 0b00001000)

        self.pen_hovered_far = Input_Value(False, 0b01000000)
        self.pen_hovered_close = Input_Value(False, 0b00100000)
        self.pen_touch = Input_Value(False, 0b00000001)

        self.pen = pen

    def set_input_values(self, bin_num):
        #check if pen hovered #todo only true if every 1 bit exists in bin_num
        print((bin_num & self.pen_hovered_far.bit_value))
        print(bin_num)

        self.pen_hovered_far.value = (bin_num & self.pen_hovered_far.bit_value) > 0
        self.pen_hovered_close.value = (bin_num & self.pen_hovered_close.bit_value) > 0

        self.pen.hovered_far = self.pen_hovered_far
        self.pen.hovered_close = self.pen_hovered_close

        # pen is hovered
        if(self.pen_hovered_far.value == True or self.pen_hovered_close.value == True):
        # pen is not hovered
            self.pen.set_input_values(bin_num)

        else:
            self.button_left_rounded.value = (bin_num & self.button_left_rounded.bit_value) > 0
            self.button_left_rectangular.value = (bin_num & self.button_left_rectangular.bit_value) > 0
            self.button_right_rectangular.value = (bin_num & self.button_right_rectangular.bit_value) > 0
            self.button_right_rounded.value = (bin_num & self.button_right_rounded.bit_value) > 0
    def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, 
                sort_keys=True, indent=4)

pen = Pen()
tablet = Tablet(pen)

def get_bar_str(min, max, val):
    str_str = ""
    for key in range(0,max): 
        if(key <= val):
            str_str+= "■"
        else:
            str_str+= " "

    return bin(val)[2:].zfill(len(bin(max)[2:])) +"|" + "["+str_str+"]"

time_then = round(time.time() * 1000)
try:
    while True:
        time_now = round(time.time() * 1000)
        delta_time = time_now - time_then 

        if delta_time > 1000/60 or True:  #1000ms / 60 fps
            d = device.read(16)
            if d:
                print("######## output #########")
                bin_8_1 = bin(d[2])[2:]
                bin_8_2 = bin(d[3])[2:]
                binary_two_and_three = "0b"+str(bin_8_2).zfill(8)+str(bin_8_1).zfill(8)

                # print(bin_8_1)
                # print(bin_8_2)
                # print(binary_two_and_three)
                value_x_axis = int(binary_two_and_three, 2)
                # print(int(binary_two_and_three, 2))

                bin_8_1 = bin(d[5])[2:]
                bin_8_2 = bin(d[6])[2:]
                binary_two_and_three = "0b"+str(bin_8_2).zfill(8)+str(bin_8_1).zfill(8)
                value_y_axis = int(binary_two_and_three, 2)
                screen_width = pyautogui.size()[0]
                screen_height = pyautogui.size()[1]
                # if two monitors 
                screen_width = screen_width - 1920
                value_x_axis_max = 15200
                value_y_axis_max = 9500

                # pyautogui.moveTo((screen_width / value_x_axis_max) * value_x_axis + 1920, (screen_height / value_y_axis_max) * value_y_axis)

                # print(value_x_axis, value_y_axis)
                # print(screen_width, screen_height)
                
                
                # screen_width = win32api.GetSystemMetrics(0)
                # screen_height = win32api.GetSystemMetrics(1)

                #win32api.SetCursorPos((0,0))

                # for (key, val) in enumerate(d):
                #     print("idx:"+ str(key) +" " +get_bar_str(0,255,val))


                tablet_8_bit_num = d[1]
                tablet.set_input_values(tablet_8_bit_num)
                print((tablet.toJSON()))

                #print('read: "{}"'.format(d))
                time_then = round(time.time() * 1000)

except KeyboardInterrupt:
    device.close()
    print('interrupted!')