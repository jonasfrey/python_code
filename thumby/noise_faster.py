# Written by: Laveréna Wienclaw, Feb 2022
import thumby
import random

while( True):

    n_bytes = thumby.display.width * 5
    a = []
    for n in range(0, n_bytes):
        a.append(int(random.uniform(0, 1) * 255))
        
    a_bytes = bytearray(a)
    
    o_sprite = thumby.Sprite(72, 40, a_bytes, 0, 0)
    
    thumby.display.drawSprite(o_sprite)
    
    thumby.display.update()