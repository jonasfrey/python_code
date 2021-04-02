from PIL import Image
from drawille import Canvas
import numpy as np

import requests
sq_i_w = 200
url = "https://picsum.photos/"+str(sq_i_w)
#url = "https://media.geeksforgeeks.org/wp-content/uploads/20190712221555/png-248x300.png"
im = Image.open(requests.get(url, stream=True).raw)
w = im.size[0]
h = im.size[1]  # Get the width and hight of the image for iterating over

#im = Image.open('birds.jpg') # Can be many different formats.
#im = im.resize((int(im.width/2), int(im.height/2)))
w = im.size[0]
h = im.size[1] 


im.save("fdsa.png")
im.show()

c = Canvas()
pix = im.load()

# array_1d = [11,11,11,22,22,22,33,33,33,44,44,44]
# array_2d = [[11,11,11],[22,22,22],[33,33,33],[44,44,44]]
# array_3d = [[[11,11,11],[22,22,22]],[[33,33,33],[44,44,44]]]

# data = np.zeros((2, 2, 3), dtype=np.uint8)

# asdf = np.asarray(array_3d)
# img = Image.fromarray(asdf, 'RGB')
# img.save('my.png')
# img.show()
# exit()
# print(data)

pixels = list(im.getdata())
pixels_reversed = pixels
pixels_reversed = pixels[::-1]
# N = 100
# pixels_reversed_3d = pixels
# #pixels_reversed_3d = [pixels_reversed[n:n+N] for n in range(0, len(pixels_reversed), N)]
# # pixels_reversed_2d = [[(255,255,255), (0,0,0)],[(255,255,255), (0,0,0)]]

# asdf = np.asarray(pixels_reversed).flatten().reshape(3, 100,100)

# asdf = np.array(im.getdata()).ravel().reshape(100,100,3)

# PIL_image = Image.fromarray(asdf, "RGB")
# PIL_image.save("test.png")
# PIL_image.show()


from tkinter import *
master = Tk()

canvas_width = sq_i_w
canvas_height = sq_i_w
w = Canvas(master, width=canvas_width,height=canvas_height)
w.pack()
img = PhotoImage(width=canvas_width, height=canvas_height)
w.create_image(canvas_width/2,canvas_height/2, image=img, state="normal")

for key, val in enumerate(pixels_reversed):
    y = int(key/sq_i_w)
    x = key%sq_i_w

    #hex_col = ("#"+str(hex(val[0]).split("0x",1)[1])+str(hex(val[1]).split("0x",1)[1])+str(hex(val[2]).split("0x",1)[1]))
    hex_col = '#%02x%02x%02x' % val
    img.put(hex_col, (x,y))




mainloop()


exit()
for x in range(0,w):
    for y  in range(0,h):
        
        rgb_sum = pix[x,y][0]+ pix[x,y][1]+ pix[x,y][2]

        if rgb_sum < (255*3) /2 :
            pix[x,y] = (0, 0, 0)  # Set the RGBA Value of the image (tuple)
        else: 
            c.set(x,y)
            pix[x,y] = (255,255,255)

        
print(c.frame())
print()


im.save('birds_m.png')  # Save the modified pixels as .png
im.show()
