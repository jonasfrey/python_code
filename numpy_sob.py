import numpy as np
from PIL import Image
from pprint import pprint


ar = [
    
    [0,0,0],
    [11,11,11],
    [22,22,22],

    [77,77,77],
    [88,88,88],
    [99,99,99], 

    [123,123,123],
    [166,166,166],
    [222,222,222],

    [222,222,222],
    [233,233,233],
    [255,255,255],

    [222,222,222],
    [233,233,233],
    [255,255,255],
]

ar2 = [
    [0,0,0],
    [11,11,11],
    [22,22,22],
    [33,33,33],
    [44,44,44],

    [0,0,0],
    [11,11,11],
    [22,22,22],
    [33,33,33],
    [44,44,44],

    [0,0,0],
    [11,11,11],
    [22,22,22],
    [33,33,33],
    [44,44,44],

    [0,0,0],
    [11,11,11],
    [22,22,22],
    [33,33,33],
    [44,44,44],

    [0,0,0],
    [11,11,11],
    [22,22,22],
    [33,33,33],
    [44,44,44],
]
def chunks(ar, n):
    #n = int(len(ar) / n)
    # print(n)
    # return [ for() ar[0::n],ar[1::n],ar[2::n]]
    """Yield successive n-sized chunks from lst."""
    arr = []
    for i in range(0, len(ar), n):
        arr.append(ar[i:i + n])

    return arr


ar = (chunks(ar, 5))
pprint(ar)
#print(ar)
# ar = np.array(ar)
# ar = ar.flatten()
# print(ar)
# ar = ar.reshape(3,4)
ar = np.array(ar)
img = Image.fromarray(ar, 'RGB')
img.save('my.png')
img.show()