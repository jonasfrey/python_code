import numpy as np
import time
# sooooo we have 


class Eval_n_print: 
    def __init__(self):
        self.strings = []

    
    def eval_n_print(self, string):
    
        var_name = string.split("=")[0]
        exec(string)
        print(string)
        print("print("+"".join(var_name.split("\n"))+")")
        print("> "+str(eval(var_name)))
        print("")

ep = Eval_n_print()

ep.eval_n_print("ep.arr = [0,1,2,3,4,5,6,7,8,9,0]")

ep.eval_n_print("ep.arr_first_item = ep.arr[0]")

ep.eval_n_print("ep.arr_last_imtem_classic = ep.arr[len(ep.arr)-1]")

ep.eval_n_print("ep.arr_last_imtem_pythonic = ep.arr[-1]")

ep.eval_n_print("ep.arr_range_second_to_fourth = ep.arr[2:4]")

ep.eval_n_print("ep.arr_range_begin_to_fourth = ep.arr[:4]")

ep.eval_n_print("ep.arr_range_fourth_to_end = ep.arr[4:]")



# double colons 
# arr[start:stop:step]


ep.eval_n_print("ep.arr_every_2nd = ep.arr[::2]")

ep.eval_n_print("ep.arr_every_3rd = ep.arr[::3]")

ep.eval_n_print("ep.arr_every_2nd_from_2_to_6 = ep.arr[2:6:2]")

ep.eval_n_print("ep.arr_every_3nd_from_6_to_end = ep.arr[6::3]")

# you can set multiple values 
# print("you can set multiple values at once")
# print("set every 2nd to 0")
# print("ep.arr[::2] = 0")
# ep.arr[::2] = [0]
# print(ep.arr)

print("# slice assignment")
ep.eval_n_print("ep.arr_cp = ep.arr.copy()")

ep.eval_n_print("ep.arr_cp_every_2nd = ep.arr_cp[::2]")

print("# now if we want to replace every second with 0 ")

print("ep.arr_cp[::2] = 0")

print("> TypeError: must assign iterable to extended slice")

print("ep.arr_cp[::2] = [0]")
print("> ValueError: attempt to assign sequence of size 1 to extended slice of size 6")


ep.eval_n_print("ep.arr_cp[::2] = [0,0,0,0,0,0]")

print("print(ep.arr_cp)")
print(">"+str(ep.arr_cp))


# print("!!! the following is not python default behaviour, somehow numpy makes this possible !")
# # commas / multidimensional arrays

ep.eval_n_print(""" 
ep.arr_2d = np.array([
    [0,1,2,3,4],
    [1,1,2,3,4],
    [2,1,2,3,4],
    [3,1,2,3,4]
])
"""
)

ep.arr_2d[:, 0] = 0

print(ep.arr_2d)


ep.arr_2d[:, 2] *= ep.arr_2d[:, 2]

print(ep.arr_2d)



ep.eval_n_print(""" 
ep.arr_3d = np.array([
    [[122,122,122],[221,221,221],[55,55,55]],
    [[122,122,122],[221,221,221],[55,55,55]],
    [[122,122,122],[221,221,221],[55,55,55]],
])
"""
)

# ep.arr_3d[::,::,0] = 0

print(ep.arr_3d)


# speed test 
w = 1920
h = 1080
color_channels = 3


img = np.ones((w,h,color_channels))

start = time.time()
img[::, ::, 0] = 0

end = time.time()
#print(img)
print("time delta with img[::,::,0] = 0")
print(end - start)

img = np.ones((w,h,color_channels))

start = time.time()

for y in img:
    for x in y: 
        x[0] = 0

end = time.time()

#print(img)

print("time delta with for loops")
print(end - start)
