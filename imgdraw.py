from PIL import Image
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 


class Canvas():
    def rectangle(self, x, y , width, height): 
        
        w, h = 512, 512
        data = np.zeros((h, w, 3), dtype=np.uint8)

        print(data)
        data[x : (x+width), y:(y+height)] = [255, 0, 0] # red patch in upper left
        img = Image.fromarray(data, 'RGB')

        draw = ImageDraw.Draw(img)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("OpenSansEmoji.ttf", 20)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((0, 0),u"\U0001f44d",(255,255,255),font=font)

        #img.save('my.png')

        img.show()


c = Canvas()
c.rectangle(10, 50 , 100, 100)
i = 0
while i < 10:
    i+= 1
    c.rectangle(i*10, 50 , 100, 100)
