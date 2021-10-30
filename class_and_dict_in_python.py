import inspect

class My_class:
    def __init__(self):
        self.porp =1

my_class_instance = My_class()
my_dict = {}

print(inspect.isclass(my_class_instance))
print(inspect.isclass(my_dict))

print(inspect.isclass(type(my_class_instance)))
print(inspect.isclass(type(my_dict)))
