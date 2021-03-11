class Foo:
    def __init__(self): 
        print(self) # has self by default

    def pre_defined_function(self):
        print(self) # has self by default


f = Foo()

f.pre_defined_function()

def later_added_function(self): 
    print(self) # wont work unless self gets passed as param

f.later_added_function = later_added_function

f.later_added_function()
f.later_added_function(f)




