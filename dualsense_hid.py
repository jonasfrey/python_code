import hid
#import win32api, win32con
import pyautogui
import time
import json 
import os
import math


#dualsense 
VENDOR_ID = 0x054c # 
PRODUCT_ID = 0x0ce6 # 

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
    min = int(min)
    max = int(max)
    val = int(val)
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
            d = device.read(64)
            if d:
                os.system('cls||clear')

                print("######## output #########")

                str_str = ""
                for (key, val) in enumerate(d):
                    if(key == 14):
                        str_str += ("idx:"+ str(key) +" " +get_bar_str(0,255,val))
                        str_str += "\n"

                print(str_str)
                # print(str_str)
                # #print(chr(27) + "[2J")
                # time.sleep(0.1)


                bin_8_1 = bin(d[15])[2:]
                bin_8_2 = bin(d[16])[2:]
                binary_two_and_three = "0b"+str(bin_8_2).zfill(8)+str(bin_8_1).zfill(8)

                # print(bin_8_1)
                # print(bin_8_2)
                # print(binary_two_and_three)
                value_16_bit_at_index_17_and_18 = int(binary_two_and_three, 2)
                bar_string = get_bar_str( 0, 255, (255/pow(2, 16))*value_16_bit_at_index_17_and_18 )
                print(bar_string)


except KeyboardInterrupt:
    device.close()
    print('interrupted!')