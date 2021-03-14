from drawille import Canvas
from copy import copy

class Pixel: 
    def __init__(self, x, y, z ):
        self.x = x
        self.y = y
        self.z = z

class PixelIcon:
    def __init__(self):
        self.width = None
        self.height = None
        self.pixels = []
        self.multiline_string = ""
        print("please specify PixelIcon.width and .height if you dont use PixelIcon.generate_pixels_by_multiline_string" )

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
            self.width = len(characters)
            x = 0
            for char in characters: 
                if x > self.width - 1:
                    continue
                if(char != " "):
                    self.add_pixel(x, y, z)  
                x += 1
            y += 1
        self.height = y

            
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
            y_offset = (self.height-1) * val.y
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

if True: 
    brick = PixelIcon()
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
    xico.generate_pixels_by_multiline_string(
"""
o   o
 o o
  o
 o o
o   o
""")


    threetimesthree = PixelIcon()
    threetimesthree.generate_pixels_by_multiline_string(
"""
---
- - 
---
""")



    tree = PixelIcon()
    tree.generate_pixels_by_multiline_string(
"""
x    
xx   
xxx  
xxxx 
xxxxx
""")

    tetrislol = PixelIcon()
    tetrislol.generate_pixels_by_multiline_string(
"""
   
 x 
xxx
""")

    x = PixelIcon()
    x.generate_pixels_by_multiline_string(
"""
x x
 x 
x x
""")

    x = PixelIcon()
    x.generate_pixels_by_multiline_string(
"""
- - 
 - -
- - 
 - -
""")

    x = PixelIcon()
    x.generate_pixels_by_multiline_string(
"""
- -
---
 - 
""")

c = Canvas()
pi = x

for px in pi.get_fractal_pixels(3):
    c.set(px.x, px.y)

print(c.frame())