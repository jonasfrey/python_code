from drawille import Canvas
from copy import copy
import time
import curses
import os


import numpy as np
from PIL import Image

class Pixel: 
    def __init__(self, x, y, z ):
        self.x = x
        self.y = y
        self.z = z

class PixelIcon:
    instances = []
    def __init__(self):
        self.width = None
        self.height = None
        self.pixels = []
        self.multiline_string = ""
        #print("please specify PixelIcon.width and .height if you dont use PixelIcon.generate_pixels_by_multiline_string" )
        PixelIcon.instances.append(self)

    def add_pixel(self,x, y, z,  add_mirrored_x_pixel = False, add_mirrored_y_pixel = False, add_mirrored_z_pixel = False):
        #pixels = []
        pixel1 = Pixel(x,y,z)
        self.pixels.append(pixel1)
        if add_mirrored_x_pixel:
            self.pixels.append(self.get_mirrored_x_pixel(pixel1))

    def mirror_x(self):
        pixels_copy = self.pixels[:] #array[:]  <- copy without reference
        for val in pixels_copy:
            self.pixels.append(self.get_mirrored_x_pixel(val))

    def get_mirrored_x_pixel(self, pixel):
        cpixel = copy(pixel) # copy(obj) <-copy obj without reference
        cpixel.x = (self.width-1) - pixel.x
        return cpixel

    def generate_pixels_by_multiline_string(self, mls):
        self.multiline_string = mls

        lines = self.multiline_string.splitlines()
        x = 0
        y = 0 
        z = 0
        for line in lines: 
            characters = list(line)
            if(self.width == None or self.width == 0):
                self.width = len(characters)
            x = 0
            for char in characters: 
                if x > self.width - 1:
                    continue
                if(char != " "):
                    self.add_pixel(x, y, z)  
                x += 1
            y += 1
        self.height = y-1

            
    def get_fractal_pixels(self, iterations=2):
        pixels = self.pixels
        for i in range(0,iterations-1):
            pixels = self.get_fractal_pixels_by_array(pixels)
        
        return pixels


    def get_fractal_pixels_by_array(self, array): 
        pixel_icons = []
        for val in array:
            npixel_icon = PixelIcon()
            x_offset = self.width * val.x
            y_offset = (self.height) * val.y
            for val2 in self.pixels:
                x = x_offset + (val2.x)
                y = y_offset + (val2.y)
                npixel_icon.add_pixel(x,y,0)
                #val2.z = self.depth * val2.z + val2.z

            pixel_icons.append(npixel_icon)

        pixels = []
        for npi in pixel_icons:
            for ps in npi.pixels:
                pixels.append(ps)

        return pixels


    # todo mirror_y and mirror_z 

# add by defining every pixel, only for loosers the way to go is multilinestring !!
# pi = PixelIcon()
# # print(pi)
# pi.add_pixel(0,0,0)
# pi.add_pixel(2,0,0)
# pi.add_pixel(4,0,0)
# pi.mirror_x()
fractal_objects = []
if True: 
    brick = PixelIcon()
    fractal_objects.append(brick)
    brick.generate_pixels_by_multiline_string(
"""
ooooooooo
o o   o o
ooooooooo
o   o   o
ooooooooo
o o   o o
ooooooooo
o   o   o
ooooooooo
""")
# print(brick.__dict__)
# exit()
# print(pi)


# for val in brick.pixels:
#     print(val.__dict__)
#     c.set(val.x, val.y)

#fractal fun 




    xico = PixelIcon()
    fractal_objects.append(xico)
    xico.generate_pixels_by_multiline_string(
"""
o   o
 o o 
  o  
 o o 
o   o
""")


    threetimesthree = PixelIcon()
    fractal_objects.append(threetimesthree)
    threetimesthree.generate_pixels_by_multiline_string(
"""
---
- -
---
""")



    tree = PixelIcon()
    fractal_objects.append(tree)
    tree.generate_pixels_by_multiline_string(
"""
x    
xx   
xxx  
xxxx 
xxxxx
""")

    tetrislol = PixelIcon()
    fractal_objects.append(tetrislol)
    tetrislol.generate_pixels_by_multiline_string(
"""
   
 x 
xxx
""")

    x1 = PixelIcon()
    fractal_objects.append(x1)
    x1.generate_pixels_by_multiline_string(
"""
x x
 x 
x x
""")

    x2 = PixelIcon()
    fractal_objects.append(x2)
    x2.generate_pixels_by_multiline_string(
"""
- - 
 - -
- - 
 - -
""")

    x3 = PixelIcon()
    fractal_objects.append(x3)
    x3.generate_pixels_by_multiline_string(
"""
- -
---
 - 
""")


x4 = PixelIcon()
fractal_objects.append(x4)
x4.generate_pixels_by_multiline_string(
"""
-- 
 --
- -
""")


x5 = PixelIcon()
fractal_objects.append(x5)
x5.generate_pixels_by_multiline_string(
"""
xxxx
x  x
 xx 
xxxx
""")

x6 = PixelIcon()
fractal_objects.append(x6)
x6.generate_pixels_by_multiline_string(
"""
  x 
 xx 
xxx 
xxxx
""")

twotimestwo = PixelIcon()
fractal_objects.append(twotimestwo)
twotimestwo.generate_pixels_by_multiline_string(
"""
xx
x 
""")


moon = PixelIcon()
fractal_objects.append(moon)
moon.generate_pixels_by_multiline_string(
"""
 ,-,
/.( 
\ { 
 `-`
""")


moon2 = PixelIcon()
fractal_objects.append(moon2)
moon2.generate_pixels_by_multiline_string(
"""
   _..._   
 .:::::::. 
...........
...........
...........
...........
`:::::::::'
  `':::'"  
""")


pi = x1
c = Canvas()

# for px in pi.get_fractal_pixels(2):
#     c.set(px.x, px.y)
# print(c.frame())

# w = 100
# for i in range(0, 1000):
#     time.sleep(1)
#     c.clear()
#     print("".join(["\n"]*10))
#     for px in pi.get_fractal_pixels(3):
#         c.set((i%w)+px.x, px.y)
#         print(c.frame())


# stdscr = curses.initscr()
# stdscr.refresh()

# we have to create a border

w = 100
h = 100

def c_set_border(w,h):
    for x in range(0,w):
        for y in range(0,h):
            if x  == 0 or x == w-1 or y == 0 or y == h-1:
                c.set(x, y) 


for key, val in enumerate(fractal_objects):
    #print(10-val.width)
    #print(val)
    i = 1
    while len(val.get_fractal_pixels(i)) < 1024:
        i+=1 
        
    for px in val.get_fractal_pixels(i):
        c.set(px.x, px.y)


    # w, h = 1024, 1024
    # data = np.zeros((h, w, 3), dtype=np.uint8)
    # for px in val.get_fractal_pixels(i):
    #     data[px.x, px.y] = [255,255,255]
    # img = Image.fromarray(data, 'RGB')
    # img.save('fractal'+str(key)+'.png')

    print(c.frame())
    c.clear()
    

w, h = 1920, 1500
data = np.zeros((h, w, 3), dtype=np.uint8)
for px in fractal_objects[2].get_fractal_pixels(6):
    data[px.x, px.y] = [255,255,255]
img = Image.fromarray(data, 'RGB')
img.save('my_fractal.png')

# for i in range(0,7):
#     # print("".join(["\n"]*20)) #''clear'' terminal
#     print(i)
#     # print(chr(27) + "[2J")
#     c_set_border(100,100)
#     for p in twotimestwo.get_fractal_pixels(i):
#         c.set(p.x+i, p.y)
#     # f = c.frame()+'\n'
#     # stdscr.addstr(0, 0, f)
#     # stdscr.refresh()
#     time.sleep(0.1)
#     print(c.frame())
#     c.clear()
#     # os.system('cls' if os.name == 'nt' else 'clear')
