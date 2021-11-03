from threading import current_thread
import numpy as np
import cv2
import mouse
import random
import sys
from scipy import fftpack

class Imagemanipulation_functions_object:
    
    def __init__(self, frame):
        self.frame = frame

    @property
    def names(self):
        current_function_name =sys._getframe().f_code.co_name
        strings = []
        for val in dir(self):
            if not val.startswith('__') and not val == current_function_name and callable(getattr(self, val)):
                strings.append(val)

        return strings

    def original_frame(self, array_np_arrays):
        return array_np_arrays[-1]

    def frame_fourth_dimension_time(self, array_np_arrays):
        sliceslen = self.frame.array_np_arrays_max_len
        if(len(array_np_arrays)<sliceslen):
            return array_np_arrays[-1]
        last_np_array = array_np_arrays[-1].copy()

        height, width, asdf= last_np_array.shape
        for i in range(0, sliceslen-1):
            last_np_array[:, (i)*int(width/sliceslen):(i+1)*int(width/sliceslen)] = array_np_arrays[i][:, (i)*int(width/sliceslen):(i+1)*int(width/sliceslen)]

         
        return last_np_array

    def frame_fourth_dimension_time_two(self, a_np_frames):
        
        n_slices_len = 50

        a_last_np_frame = a_np_frames[-1].copy()

        height, width, asdf = a_last_np_frame.shape

        for i in range(0, n_slices_len):

            n_from = (i)*int(width/n_slices_len)
            n_to = (i+1)*int(width/n_slices_len)
            a_last_np_frame[n_from:n_to] = (
                a_np_frames[(len(a_np_frames)-2)-i][(i)*int(width/n_slices_len):(i+1)*int(width/n_slices_len)]
            )

         
        return a_last_np_frame

    
    # def radial_expanding_matrix_transformation_scale(self, a_np_frames):
    #     # rad = radius , min = minimum, max = maximum
    #     n_rad_min = 0
    #     n_rad_max = 50 
    #     n_step_per_rad = 10
    #     a_last_np_frame = a_np_frames[-1]

    #     for n_rad_i in range(n_rad_min, n_rad_max): 
    #         n_rad_i_rev = n_rad_max - n_rad_i
            
    #         n_rad_current = n_rad_i * n_step_per_rad
    #         n_width = n_rad_current
    #         n_height = n_rad_current
    #         a_last_np_frame_subframe = a_last_np_frame[0:n_width, 0:n_height]
            
    #         height, width, x = a_last_np_frame_subframe.shape

    #         a_last_np_frame[0:n_width, 0:n_height] = (
    #             # matrix transformation scaling
    #             cv2.resize(a_last_np_frame_subframe, dsize=(height * n_rad_i, width* n_rad_i), interpolation=cv2.INTER_CUBIC)
    #         )
                
    #     return a_last_np_frame

    def loop_scale_test(self, a_np_frames):

        a_last_np_frame = a_np_frames[-1]
        a_last_np_frame_copy = np.copy(a_last_np_frame)
        height, width, x = a_last_np_frame.shape
        n_max = 50
        
        for n_i in range(1, n_max):
            n_width_subframe = width / n_max
            a_last_np_frame_subframe = a_last_np_frame[int((n_i-1)*n_width_subframe):int(n_i*n_width_subframe)]    
            
            # ksize = int( n_i*n_max*0.1 ) | 1
            # a_last_np_frame_subframe_blurred = cv2.blur(a_last_np_frame_copy, (ksize, ksize))

            a_last_np_frame_subframe_blurred = cv2.resize(
                a_last_np_frame_copy,
                dsize=(
                    int(width*((n_i/10)+1)),
                    height
                    ),
                    interpolation=cv2.INTER_CUBIC
                )

            a_last_np_frame_copy[int((n_i-1)*n_width_subframe):int(n_i*n_width_subframe), 0:height] = (
                a_last_np_frame_subframe_blurred[
                    int((n_i-1)*n_width_subframe):int(n_i*n_width_subframe),
                    0:height
                    ]
            )
        
        return a_last_np_frame_copy

    def scale_with_mouse_y_position(self, a_np_frames):

        a_last_np_frame = a_np_frames[-1]
        height, width, x = a_last_np_frame.shape
        mouse_pos_y_normalized = (mouse.get_position()[1] / 1080)
        return cv2.resize(a_last_np_frame, dsize=(int(width*mouse_pos_y_normalized), int(height*mouse_pos_y_normalized) ), interpolation=cv2.INTER_CUBIC)

    
    def brightness(self, array_np_arrays):
        #print( (mouse.get_position()[1] / 1080))
        # return np_array + (mouse.get_position()[1] / 1080)
        np_array = np.apply_along_axis(lambda x: (x+(mouse.get_position()[1] / 1080)), 0, array_np_arrays[-1])
        np_array = np.apply_along_axis(lambda x: (x+(mouse.get_position()[1] / 1080)), 1, np_array)
        return np_array

    """todo"""
    def multiplied_by_itself_mouse(self, array_np_arrays):
        return array_np_arrays[-1] * array_np_arrays[-1] * (mouse.get_position()[1] / 1080)

    def multiply_array_with_random(self, array_np_arrays):
        return array_np_arrays[-1] * (mouse.get_position()[1] / 1080) * random.random() 

    def mirror_x(self, array_np_arrays):

        npacp = array_np_arrays[-1].copy()
        np_array_flipped = npacp[::, ::-1]

        height, width = array_np_arrays[-1].shape[:2]

        array_np_arrays[-1][::, int(width/2):] =  (
            np_array_flipped[::, int(width/2):]
        )
        # np_array[int(height/2)::] = 0
        return array_np_arrays[-1]

    # def mirror_y(self, array_np_arrays):
    #     npacp = array_np_arrays[-1].copy()
    #     np_array_flipped = npacp[::-1, ::]

    #     height = array_np_arrays[-1].shape[:1]

    #     array_np_arrays[-1][int(height/2):, ::] =  (
    #         np_array_flipped[int(height/2):, ::]
    #     )
        
    #     return array_np_arrays[-1]

    # def mirror_x_y(self, array_np_arrays):
    #     mirrored_x = self.mirror_x(array_np_arrays[-1])
    #     mirrored_y = self.mirror_y(mirrored_x)
    #     return mirrored_y

    # def gaussian_blur(self, array_np_arrays):
        
    #     kernel = np.array([
    #         [ 1.0, 2.0, 1.0 ], 
    #         [ 2.0, 4.0, 2.0 ], 
    #         [ 1.0, 2.0, 1.0 ]
    #         ]
    #     ) # Here you would insert your actual kernel of any size
    #     np_array = np.apply_along_axis(lambda x: np.convolve(x, kernel, mode='same'), 0, np_array)
    #     np_array = np.apply_along_axis(lambda x: np.convolve(x, kernel, mode='same'), 1, np_array)
    #     return np_array

    def cv2_blur(self, array_np_arrays):
        ksize=int(22 *(mouse.get_position()[1] / 1080)) | 1
        np_array = cv2.blur(array_np_arrays[-1], (ksize, ksize)) 
        return np_array
    # def gaussian_blur_fft(self, array_np_arrays):

    #     t = np.linspace(-10, 10, 30)
    #     bump = np.exp(-0.1*t**2)
    #     bump /= np.trapz(bump) # normalize the integral to 1

    #     # make a 2-D kernel out of it
    #     kernel = bump[:, np.newaxis] * bump[np.newaxis, :]
    #     img = array_np_arrays[-1]
    #     kernel_ft = fftpack.fft2(kernel, shape=img.shape[:2], axes=(0, 1))

    #     # convolve
    #     img_ft = fftpack.fft2(img, axes=(0, 1))
    #     # the 'newaxis' is to match to color direction
    #     img2_ft = kernel_ft[:, :, np.newaxis] * img_ft
    #     img2 = fftpack.ifft2(img2_ft, axes=(0, 1)).real

    #     # clip values to range
    #     img2 = np.clip(img2, 0, 1)
    #     return img2

    def apply_along_axis(self, array_np_arrays):
        np_array = np.apply_along_axis(lambda x: x+random.random(), 0, array_np_arrays[-1])
        return np_array


class Frame:
    imagemanipulation_function_name_prefix_separator='_'
    def __init__(self, data):

        self.array_np_arrays = []
        self.array_np_arrays_max_len = 100

        self._data = data
        self.imagemanipulation_functions_object = Imagemanipulation_functions_object(self)
        self.last_datImagemanipulation_functionsa = self.data 
        self.last_data_different = False
        self.active_imagemanipulation_function_index = 0


    @property 
    def frame_manipulated(self):
        # fun = funciton
        lenght = len(self.imagemanipulation_functions_object.names)
        s_imagemanipulation_fun_name = self.imagemanipulation_functions_object.names[
                self.active_imagemanipulation_function_index % lenght
            ]
        print(s_imagemanipulation_fun_name)
        imagemanipulation_function = getattr(
            self.imagemanipulation_functions_object,
            s_imagemanipulation_fun_name
        )
        #print(self.imagemanipulation_functions_object.names)
        return imagemanipulation_function(self.array_np_arrays)
    @property
    def data(self):
        return self._data 

    @data.setter
    def data(self, value):
        if(len(self.array_np_arrays) >= self.array_np_arrays_max_len):
            self.array_np_arrays.pop(0)
                    
        self.array_np_arrays.append(value)

        self.last_data = self.data
        # self.last_data_different = value == self.last_data
        self.last_data_different = True # hard coded P
        self._data = value
        return True
  

cap = cv2.VideoCapture(1)

f = Frame(np.zeros((10,10),np.uint8))

while True:
    ret, frame = cap.read()
    f.data = frame

    cv2.imshow('Input',f.frame_manipulated)

    c = cv2.waitKey(1)
    # print(c)

    if c == 32:#spacebar 27
        f.active_imagemanipulation_function_index += 1

    if c == 27:
        break




cap.release()
cv2.destroyAllWindows()