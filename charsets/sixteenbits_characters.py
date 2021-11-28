import time

n_min = 0
n_max = 65536
string = ''
separator = ', '
newline = '\n'
tab = '\t'
for i in range(n_min, n_max):

    try:
        s_char = chr(i)
    except: 
        print(f'{i} exception found')
        continue

    string+=(f"{i} -> {chr(i)}")
    string+=tab
    if(i % 2 == 0):
        string+=newline
    
print(string)