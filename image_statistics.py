from PIL import Image
import numpy as np
import astropy.io.fits as fits
from numpy.ma import count
from scipy import stats
import math 
import matplotlib.pyplot as plt
import cv2


class Image_Statistics:
    
    def __init__(self, url_or_array):
        print(url_or_array)
        if(isinstance(url_or_array, str)):
            self.url = url_or_array
            self.data_unit16 = fits.open(self.url)[0].data
            maxval=np.amax(self.data_unit16)
            self.data_float64_normalized_by_max=self.data_unit16/maxval
            self.data_float64_normalized_by_uint16=self.data_unit16/pow(2,16)
            self.array = self.data_float64_normalized_by_uint16
            ##print(self.data_float64_normalized_by_max)
            ##print(self.data_float64_normalized_by_uint16)
        else :
            self.array = url_or_array

        self.np_array_2d = np.array(self.array)
        self.np_array_1d = self.np_array_2d.ravel()

        self.set_statistics_by_array(self.np_array_1d)
        #print(self.np_array)
        #print(self.__dict__)
        
        self.downscaled_np_array_2d = self.np_array_2d[::2]

        #print(self.array)

        imageVar = cv2.Laplacian( self.np_array_2d, cv2.CV_64F).var()
        print(imageVar)
        imageVar = cv2.Laplacian( self.np_array_1d, cv2.CV_64F).var()
        print(imageVar)

        # plt.imshow(self.array, interpolation='nearest', cmap = 'gray')
        # plt.show()

        # img = Image.fromarray(self.array, 'L')
        # img.save('my.png')
        # img.show()
        # exit()

        # self.downscaled_np_array_1d = self.downscaled_np_array_2d.flatten()

        # self.downscaled_np_array_1d = self.downscaled_np_array_1d[::32]




        # print(len(self.downscaled_np_array_1d))
        # # print(len(self.test_array))

        # plt.plot(self.downscaled_np_array_1d)
        # plt.ylabel('some numbers')
        # plt.show()

        # # print(len(self.np_array))
        # width = int(math.sqrt(len(self.downscaled_np_array_1d)))
        # print(width)
        # self.downscaled_np_array_2d = np.reshape(self.downscaled_np_array_1d, (-1, width))
        # # print(self.test_array_2d)
        # #self.downscaled_np_array_2d = self.downscaled_np_array_2d * pow(2,16)

        # img = Image.fromarray(self.downscaled_np_array_1d.reshape(width,width), 'L')
        # img.save('my.png')
        # img.show()

        
        # counts, bins = np.histogram(self.array)

        # # plt.style.use('dark_background')
        # # #plt.hist(bins[:-1], bins, weights=counts)
        # # plt.plot()
        # # ##plt.ylabel('some numbers')
        # # plt.show()


    def set_statistics_by_array(self, array): 
        
        self.scipy_stats = stats.describe(array)

        self.min = self.scipy_stats.minmax[0]
        self.max = self.scipy_stats.minmax[1]
        self.range = self.max -self.min
        self.midrange = self.range / 2
        self.sum = np.sum(array)
        self.mean = self.scipy_stats.mean
        self.average = self.mean
        self.median = np.median(array)
        self.mode = stats.mode(array)
        self.variance = self.scipy_stats.variance
        self.standard_deviation = math.sqrt(self.variance)





img_stats = Image_Statistics("./m101_blurry.fts")


img_stats = Image_Statistics("./m101_sharp.fts")





