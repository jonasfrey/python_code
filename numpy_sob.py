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
ar2 = [
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],

    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],

    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],

    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],

    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
    ["px_r", "px_g", "px_b"],
]
def chunks(ar, n):
    """Yield successive n-sized chunks from lst."""
    arr = []
    for i in range(0, len(ar), n):
        arr.append(ar[i:i + n])

    return arr
def jesse_chunks(ar, n):
    return [ar[0:n],ar[n:2*n],ar[2*n:3*n]]



ar2_chunked = (chunks(ar2, 5))
ar2_jesse_chunked = (jesse_chunks(ar2, 5))

print("chunks")
pprint(ar2_chunked)
print("jesse_chunks")
pprint(ar2_jesse_chunked)

#print(ar)
# ar = np.array(ar)
# ar = ar.flatten()
# print(ar)
# ar = ar.reshape(3,4)
ar = np.array(ar)
img = Image.fromarray(ar, 'RGB')
img.save('my.png')
img.show()