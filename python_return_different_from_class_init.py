class O_class_with_new_function(object):
    
    def __init__(self):
        print("this init is never called since __new__() is defined in this class")

    def __new__(cls):
        print("this can actually be very disorientating but can be usefull in some rare cases")
        
        return 42

o_class_with_new_function_instance = O_class_with_new_function()
# now the instance is a number 

print(o_class_with_new_function_instance)
