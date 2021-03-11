from PIL import Image
 
img = Image.new('RGB', (60, 30), color = 'red')
#img.save('pil_red.png')
img.show()

img = Image.new("RGB", (12, 12))
img.show() # see a black image
pixels = [(255,0,0)]*(12*12)
img.putdata(pixels)
img.show() # see a red image

pixels = [(0,255,0)]*(12*12)
img.putdata(pixels)
img.show() # see a red image