import thumby 
import random

# print("thumby.display")
# print(thumby.display.__dict__)
# {
#     'textBitmap': bytearray(b '\x00\x00\x00\x00\x00'),
#     'frameRate': 0,
#     'width': 72,
#     'max_x': 71,
#     'max_y': 39,
#     'textBitmapSource': 'lib/font5x7.bin',
#     'textCharCount': 96,
#     'textWidth': 5,
#     'lastUpdateEnd': 0,
#     'textHeight': 7,
#     'height': 40,
#     'textSpaceWidth': 1,
#     'textBitmapFile': < io.TextIOWrapper > ,
#     'display': < SSD1306_SPI object at 2000 b260 >
# }

n_time = 0
while(True):
    n_time += 1
    n_toggle = n_time % 2 
    thumby.display.fill(0)
    for n_i in range(0, thumby.display.width * thumby.display.height):
        n_x = n_i % thumby.display.width
        n_y = int(n_i / thumby.display.width)
        n_y_toggle= (n_y % 2) == n_toggle
        n_pixel = 0
        # if(((n_i % 2) % (n_time % 2)) == 0): 
        if (n_i % 2) == n_y_toggle:
            n_pixel = 1
        
        thumby.display.setPixel(n_x, n_y, n_pixel)
            
            
    thumby.display.update()