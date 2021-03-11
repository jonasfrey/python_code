class My_Class: 
    def __init__(self):
        self.x = 10

m = My_Class()

m.y = m.x

o = m 

o.x = 20 

print(m.x) # what does it print and why
print(o.x) # what does it print and why