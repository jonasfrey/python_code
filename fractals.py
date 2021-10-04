
import sys
import time
from datetime import datetime

time_start = time.time()
datetime_start = datetime.now().microsecond

def make_me_fractal(multiline_string, base_multiline_string):

    new_multiline_string = ''
    lines = multiline_string.split("\n")
    for line in lines:
        chars = list(line)
        
        for line2 in base_multiline_string.split("\n"):
            for char in chars:
                    if char == " ":
                        str = char * len(line2)
                        new_multiline_string += str
                    else:
                        new_multiline_string += line2
    
            new_multiline_string += "\n"
    
    return new_multiline_string
    
base_shape = "###\n"
base_shape+= "# #\n"
base_shape+= "###"

iterations = 4

if(len(sys.argv)>1):
    iterations = int(sys.argv[1])

new_shape = base_shape; 
for i in range(1, iterations):
    new_shape = make_me_fractal(new_shape, base_shape)
    # print(new_shape)


time_end = time.time()
datetime_end = datetime.now().microsecond

time_delta = abs(time_start - time_end)
datetime_delta = abs(datetime_start - datetime_end)

print(new_shape)

print("script execution time_delta, datetime_delta:"+str(time_delta)+","+str(datetime_delta))

exit
