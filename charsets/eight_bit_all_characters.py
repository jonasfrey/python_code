

n_min = 127
n_max = 255
string = ''
separator = ', '
newline = '\n'
tab = '\t'
for i in range(n_min, n_max):
    string+=(f"{i} -> {chr(i)}")
    string+=tab
    if(i % 2 == 0):
        string+=newline
    
print(string)