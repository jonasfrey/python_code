# Written by: Laveréna Wienclaw, Feb 2022
import thumby
import random

n_bytes = thumby.display.width * 5
a = [0 for n in range(0, n_bytes)]
    
def f_set_pixel_fast(
    n_x, 
    n_y, 
    b_value
    ):
    # if(
    #     n_x > thumby.display.width
    #     or 
    #     n_x < 0
    #     or 
    #     n_y > thumby.display.height
    #     or 
    #     n_y < 0 
    # ): 
    #     return False
    try:
        n = int(n_y / 8) * 72
        n_bit = n_y % 8
        n_index = n + n_x
        n_byte_with_bit_set = n_byte_with_bit_set
        if(n_bit_value):
            n_byte = a[n_index] | n_byte_with_bit_set
        else: 
            n_byte = a[n_index] & ~(n_byte_with_bit_set)
            
        a[n_index] = n_byte
    except:
        pass

f_set_pixel_fast(1,1)

for n_x in range(0,72):
    n_y = int(n_x*(40/72))
    f_set_pixel_fast(n_x, n_y)
    
for n_x in range(0,72):
    n_y = int(n_x * n_x * 0.01)
    f_set_pixel_fast(n_x, n_y)
        
a_bytes = bytearray(a)
o_sprite = thumby.Sprite(72, 40, a_bytes, 0, 0)
print(a)
thumby.display.drawSprite(o_sprite)

thumby.display.update()