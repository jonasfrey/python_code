# the most basic table is the ascii table 
# numbers from 0-127 represent each a individual basic character 
# 0-32 are special characters which are not always visible for example 
# for example 
# 0 [null], 1[start of heading], 2 [start of text], 3 [end of text], 4 [ end of transmission ]
# 9 [horizontal tab],  10 [line feed(\n newline)] , ... 32 [space]
# 33 - 127 are characters 
# for example 
# 33 !, 34 ", 35 #, 36 $, .... 
# 48 0, 49 1, 50 2, ... 
# 65 A, 66 B, 67 C, ... 
# 97 a, 98 b, 99 c, ...

# the last 127 is again special 
# 127 [del]

n_min_ascii = 0
n_max_ascii = 127

for i in range(n_min_ascii, n_max_ascii):
    if(i < 32):
        print('special char!')

    print(f"{i} -> {chr(i)}")

print('end')