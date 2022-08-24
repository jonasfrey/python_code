from re import A
from astropy.io import fits
import sys 
import cv2

s_path_name_file_name = sys.argv[1]

print(s_path_name_file_name)
o_hdulist = fits.open(s_path_name_file_name)
a_data =  o_hdulist[0].data
print(a_data)
a_data_width = a_data.shape[0]
a_data_height = a_data.shape[1]
print(a_data_width/2)
print(a_data.shape)

cv2.imshow('B-RGB', a_data)
cv2.waitKey(0)

a_data_downscale = cv2.resize(a_data, dsize=(int(a_data_height/2),int(a_data_width/2)))
# cv2.imwrite("test.png", a_data_downscale)
# cv2.imwrite("test.png", a_data)
cv2.imwrite("test.jpg", a_data)