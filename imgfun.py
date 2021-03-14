from PIL import Image

import numpy as np
from copy import copy

im = Image.open('boris-smokrovic-lyvCvA8sKGc-unsplash.jpg') # Can be many different formats.
pix = im.load()
print(im.size ) # Get the width and hight of the image for iterating over
# print(pix[x,y])  # Get the RGBA Value of the a pixel of an image
# pix[x,y] = value  # Set the RGBA Value of the image (tuple)

print(pix[10,10])
# for p in pix:
#     print(p)

pixel_values = list(im.getdata())

scale_x_divisor = 16
scale_y_divisor = 16
scale_x = (1/scale_x_divisor)
scale_y = (1/scale_y_divisor)

width = im.size[0]
height = im.size[1]
scaled_width = int(int(width) * scale_x)
scaled_height = int(int(height) * scale_y)

print(scaled_width, scaled_height)


#scale down image take nth pixel

w, h = 11, 11
data = np.zeros((h, w, 3), dtype=np.uint8)
data[0:256, 0:256] = [255, 0, 0] # red patch in upper left

# img = Image.fromarray(data, 'RGB')
# img.save('my.png')
# img.show()

scaled_two_dimensional_array = []
scaled_one_dimensional_array = []
line = []

one_dimensional_pixel_array = im.getdata()

for y in range(0, scaled_height):
    line = []
    y = y * scale_y_divisor
    for x in range(0, scaled_width):
        x = int(x * scale_x_divisor)
        # y = int(y * (1/scale_y))
        index = (y*width) + x
        #print(x)
        line.append(one_dimensional_pixel_array[index])
        scaled_one_dimensional_array.append(one_dimensional_pixel_array[index])

    scaled_two_dimensional_array.append(line)


print(len(scaled_two_dimensional_array[0]), len(scaled_two_dimensional_array))

#print(scaled_two_dimensional_array)
# exit()
# scaled_two_dimensional_array = [
#     [[111,111,111],[0,0,0],[111,111,111],[0,0,0],[111,111,111],[0,0,0]],
#     [[0,0,0],[111,111,111],[0,0,0],[111,111,111],[0,0,0],[111,111,111]],
#     [[111,111,111],[0,0,0],[111,111,111],[0,0,0],[111,111,111],[0,0,0]],
#     [[0,0,0],[111,111,111],[0,0,0],[111,111,111],[0,0,0],[111,111,111]]
# ] 
#2
#print(scaled_two_dimensional_array)

scaled_two_dimensional_array = np.asarray(scaled_two_dimensional_array, dtype=np.uint8)

print(type(data), type(scaled_two_dimensional_array))

img = Image.fromarray(scaled_two_dimensional_array, 'RGB')
img.save('my.png')
img.show()


# def create_two_dimensional_img_array(array, width):
#     print(array)
#     height = int(len(array) / width)
#     tda = [[[0,0,0]] * width] * height
#     print(width, height)
#     for i, p in enumerate(array): 
#         print(p)
#         print(i)
#         y = int(i / width)
#         x = i % width
#         index = (y * width) + x
#         print("p,i,y")
#         print(p, i, y)
#         #print(tda[y])
#         #tda[y] = str(y)
#         tda[y] = [None] * width
#         tda[y][x] = kjasdhflkajhs dflkjhasdlkfjh 

#     print("tda")
#     print(tda)
#     exit()
        

#     return tda

oda = []
for p in scaled_one_dimensional_array:
    rgb_sum = p[0] + p[1] + p[2]
    if rgb_sum > 375:
        oda.append([255,255,255])
    else: 
        oda.append([0,0,0])

# oda = [[1,1,111], [0,0,0], [255,255,255], 
# [2,111,111], [0,0,0], [255,255,255]
# ,[3,111,111], [0,0,0], [255,255,255]
# ]
# tda = create_two_dimensional_img_array(oda, 3)
# print(tda)
# print(len(tda[0]), len(tda))


# print(tda)

# img = Image.fromarray(np.asarray(tda, dtype=np.uint8), 'RGB')
# print(len(scaled_one_dimensional_array))
# numpy_array = np.asarray(scaled_one_dimensional_array, dtype=np.uint8)
# print(len(numpy_array))
# print((numpy_array.size))
# numpy_two_dimensional_array = numpy_array.reshape(scaled_width, scaled_height)

# create 3 dimensional array 

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

ar = list(chunks(oda, scaled_width))

# create numpy array -.- 
ar = np.array(ar)

# create image
img = Image.fromarray(ar, 'RGB')
img.save('my.png')
img.show()

# asdf = [1,2,3,4]
# for key, value in enumerate(asdf):
#     print(key)
#im.save('boris-smokrovic-lyvCvA8sKGc-unsplash_modified.png')  # Save the modified pixels as .png