import cv2
import multiprocessing as mp
import numpy as np
import psutil

img = cv2.imread('test.tiff', cv2.IMREAD_ANYDEPTH) # here I'm using a indexed 16-bit tiff as an example.
num_processes = 4
kernel_size = 11
tile_size = img.shape[0]/num_processes  # Assuming img.shape[0] is divisible by 4 in this case

output = mp.Queue()

def mp_filter(x, output):
    print(psutil.virtual_memory())  # monitor memory usage
    output.put(x, cv2.GaussianBlur(img[img.shape[0]/num_processes*x:img.shape[0]/num_processes*(x+1), :], 
               (kernel_size, kernel_size), kernel_size/5))
    # note that you actually have to process a slightly larger block and leave out the border.

if __name__ == 'main':
    processes = [mp.Process(target=mp_filter, args=(x, output)) for x in range(num_processes)]

    for p in processes:
        p.start()

    result = []
    for ii in range(num_processes):
        result.append(output.get(True))

    for p in processes:
        p.join()