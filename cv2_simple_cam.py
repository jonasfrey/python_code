from threading import current_thread
import numpy as np
import cv2
import mouse
import random
import sys
from scipy import fftpack

class Imagemanipulation_functions_object:
    
    @property
    def names(self):
        current_function_name =sys._getframe().f_code.co_name
        strings = []
        for val in dir(self):
            if not val.startswith('__') and not val == current_function_name:
                strings.append(val)

        return strings

    def original_frame(self, np_array):
        return np_array
    
    def brightness(self, np_array):
        #print( (mouse.get_position()[1] / 1080))
        # return np_array + (mouse.get_position()[1] / 1080)
        np_array = np.apply_along_axis(lambda x: (x+(mouse.get_position()[1] / 1080)), 0, np_array)
        np_array = np.apply_along_axis(lambda x: (x+(mouse.get_position()[1] / 1080)), 1, np_array)
        return np_array

    """todo"""
    def multiplied_by_itself_mouse(self, np_array):
        return np_array * np_array * (mouse.get_position()[1] / 1080)

    def multiply_array_with_random(self, np_array):
        return np_array * (mouse.get_position()[1] / 1080) * random.random() 

    def mirror_x(self, np_array):
        npacp = np_array.copy()
        np_array_flipped = npacp[::, ::-1]

        height, width, channel = np_array.shape

        np_array[::, int(width/2):] =  (
            np_array_flipped[::, int(width/2):]
        )
        # np_array[int(height/2)::] = 0
        return np_array

    def mirror_y(self, np_array):
        npacp = np_array.copy()
        np_array_flipped = npacp[::-1, ::]

        height, width, channel = np_array.shape

        np_array[int(height/2):, ::] =  (
            np_array_flipped[int(height/2):, ::]
        )
        
        return np_array

    def mirror_x_y(self, np_array):
        mirrored_x = self.mirror_x(np_array)
        mirrored_y = self.mirror_y(mirrored_x)
        return mirrored_y

    # def gaussian_blur(self, np_array):
        
    #     kernel = np.array([
    #         [ 1.0, 2.0, 1.0 ], 
    #         [ 2.0, 4.0, 2.0 ], 
    #         [ 1.0, 2.0, 1.0 ]
    #         ]
    #     ) # Here you would insert your actual kernel of any size
    #     np_array = np.apply_along_axis(lambda x: np.convolve(x, kernel, mode='same'), 0, np_array)
    #     np_array = np.apply_along_axis(lambda x: np.convolve(x, kernel, mode='same'), 1, np_array)
    #     return np_array

    def cv2_blur(self, np_array):
        ksize=int(22 *(mouse.get_position()[1] / 1080)) | 1
        np_array = cv2.blur(np_array, (ksize, ksize)) 
        return np_array
    def gaussian_blur_fft(self, np_array):

        t = np.linspace(-10, 10, 30)
        bump = np.exp(-0.1*t**2)
        bump /= np.trapz(bump) # normalize the integral to 1

        # make a 2-D kernel out of it
        kernel = bump[:, np.newaxis] * bump[np.newaxis, :]
        img = np_array
        kernel_ft = fftpack.fft2(kernel, shape=img.shape[:2], axes=(0, 1))

        # convolve
        img_ft = fftpack.fft2(img, axes=(0, 1))
        # the 'newaxis' is to match to color direction
        img2_ft = kernel_ft[:, :, np.newaxis] * img_ft
        img2 = fftpack.ifft2(img2_ft, axes=(0, 1)).real

        # clip values to range
        img2 = np.clip(img2, 0, 1)
        return img2

    def apply_along_axis(self, np_array):
        np_array = np.apply_along_axis(lambda x: x+random.random(), 0, np_array)
        return np_array


class Frame:
    imagemanipulation_function_name_prefix_separator='_'
    def __init__(self, data):
        self._data = data
        self.imagemanipulation_functions_object = Imagemanipulation_functions_object()
        self.last_datImagemanipulation_functionsa = self.data 
        self.last_data_different = False
        self.active_imagemanipulation_function_index = 0


    @property 
    def frame_manipulated(self):
        lenght = len(self.imagemanipulation_functions_object.names)
        return getattr(
            self.imagemanipulation_functions_object,
            self.imagemanipulation_functions_object.names[
                self.active_imagemanipulation_function_index % lenght
            ]
        )(self.data)
    @property
    def data(self):
        return self._data 

    @data.setter
    def data(self, value):
        self.last_data = self.data
        # self.last_data_different = value == self.last_data
        self.last_data_different = True # hard coded P
        self._data = value
        return True
  

cap = cv2.VideoCapture(3)

f = Frame(np.zeros((10,10),np.uint8))

while True:
    ret, frame = cap.read()
    f.data = frame

    cv2.imshow('Input',f.frame_manipulated)

    c = cv2.waitKey(1)
    print(c)

    if c == 32:#spacebar 27
        f.active_imagemanipulation_function_index += 1

    if c == 27:
        break




cap.release()
cv2.destroyAllWindows()