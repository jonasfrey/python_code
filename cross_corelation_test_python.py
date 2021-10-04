import numpy as np
from scipy import signal

from PIL import Image
import requests

img1 = Image.open(requests.get("https://stellarium-gornergrat.ch/wp-content/plugins/wp-slim-mvc-framework/public/cdn/2021-04-13T19-58-28_M42_Red_100s_Benjamin-A.jpg", stream=True).raw).convert('LA')
img2 = Image.open(requests.get("https://stellarium-gornergrat.ch/wp-content/plugins/wp-slim-mvc-framework/public/cdn/2021-04-08T19-41-21_M42_Blue_150s_Benjamin-A.jpg", stream=True).raw).convert('LA')

img1 = np.asarray(img1)
img2 = np.asarray(img2)

print(img1)

def cross_image(img1, img2):
   # get rid of the color channels by performing a grayscale transform
   # the type cast into 'float' is to avoid overflows
   img1_gray = np.sum(img1.astype('float'), axis=2)
   img2_gray = np.sum(img2.astype('float'), axis=2)

   # get rid of the averages, otherwise the results are not good
   img1_gray -= np.mean(img1_gray)
   img2_gray -= np.mean(img2_gray)

   # calculate the correlation image; note the flipping of onw of the images
   return signal.fftconvolve(img1_gray, img2_gray[::-1,::-1], mode='same')





img1_gray = np.sum(img1.astype('float'), axis=2)
img2_gray = np.sum(img2.astype('float'), axis=2)
cor = signal.correlate2d (img1_gray, img2_gray)

print(cross_image(img1_gray, img2_gray))

print(cor)
