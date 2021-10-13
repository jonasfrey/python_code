import numpy as np
import cv2


class Frame:

    def __init__(self, data):
        self._data = data
        self.last_data = self.data 
        self.last_data_different = False

    
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
    
    @property
    def gaussian_blurred(self):

        attset = hasattr(self, '_gaussian_blurred')

        if(self.last_data_different or not attset):
            self._gaussian_blurred = self.gaussian_blur()
            
        return self._gaussian_blurred
    
    # def __getattribute__(self, name):
    #     if(hasattr(self, name)):
    #         attr = super().__getattribute__(name)
    #         hasattr(attr, '__call__'):


    def gaussian_blur(self, kernel_size=3):
        dcp = self.data.copy()
        kernel = np.array(
            [
            [ 1.0, 2.0, 1.0 ], 
            [ 2.0, 4.0, 2.0 ], 
            [ 1.0, 2.0, 1.0 ]
            ]
            )
        kernel = kernel * 0.001
        kernel = kernel / np.sum(kernel)
        arraylist = []
        for y in range(3):
            temparray = np.copy(self.data)
            temparray = np.roll(temparray, y - 1, axis=0)
            for x in range(3):
                temparray_X = dcp.copy()
                temparray_X = np.roll(temparray_X, x - 1, axis=1)*kernel[y,x]
                arraylist.append(temparray_X)

        arraylist = np.array(arraylist)
        arraylist_sum = np.sum(arraylist, axis=0)

        
        return arraylist_sum

        dcp = self.data.copy()

        return dcp          

cap = cv2.VideoCapture(0)

f = Frame(np.zeros((10,10),np.uint8))

while True:
    ret, frame = cap.read()
    f.data = frame

    cv2.imshow('Input',f.gaussian_blurred)

    c = cv2.waitKey(1)
    if c == 27:
        break




cap.release()
cv2.destroyAllWindows()