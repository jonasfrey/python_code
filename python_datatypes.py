# python and its variables/references

str_hello = 'hello'
boo_is_inited = True
num_fib = 11235
num_fib_float = 112.35
arr_fib_nums = [1,1,2,3,5]

obj_dict = {
    'str_hello' : 'hello',
    'boo_is_inited' : True,
    'num_fib' : 11235,
    'num_fib_float' : 112.35,
    'arr_fib_nums' : [1,1,2,3,5],
    'obj_dict_nested': {
        'str_hello' : 'hello',
        'boo_is_inited' : True,
        'num_fib' : 11235,
        'num_fib_float' : 112.35,
        'arr_fib_nums' : [1,1,2,3,5]
    }
}

class Obj_this_is_a_class:
    def __init__(self, obj_this_is_a_class_instance=None):
        self.str_hello = 'hello'
        self.boo_is_inited = True
        self.num_fib = 11235
        self.num_fib_float = 112.35
        self.arr_fib_nums = [1,1,2,3,5]
        self.obj_this_is_a_class_instance_nested = obj_this_is_a_class_instance

obj_this_is_a_class_instance = Obj_this_is_a_class(
    Obj_this_is_a_class()
)

# since everything is a class in python
# below wont work
# it will always return true, 
# print(inspect.isclass(type(str_hello)))

# print(isinstance(type(str_hello), type))
# isinstance(type(my_variable_name), type) is by the way the same as inspect.isclass

print(type(str_hello))
print(type(boo_is_inited))
print(type(num_fib))
print(type(num_fib_float))
print(type(arr_fib_nums))
print(type(obj_dict))
print(type(obj_this_is_a_class_instance))

# to really check if a variable references a 'user' defined class
# we have to check if the __class__.__module__ is 'builtins'

print(str_hello.__class__.__module__ == 'builtins')
print(boo_is_inited.__class__.__module__ == 'builtins')
print(num_fib.__class__.__module__ == 'builtins')
print(num_fib_float.__class__.__module__ == 'builtins')
print(arr_fib_nums.__class__.__module__ == 'builtins')
print(obj_dict.__class__.__module__ == 'builtins')
print(obj_this_is_a_class_instance.__class__.__module__ == 'builtins')

# python < 3.7
# print(obj_this_is_a_class_instance.__class__.__module__ == '__builtins__')


str_hello = 'hello'
boo_is_inited = True
num_fib = 11235
num_fib_float = 112.35
arr_fib_nums = [1,1,2,3,5]
obj_dict = {'a':True}
print(isinstance(str_hello, type))
print(isinstance(boo_is_inited, type))
print(isinstance(num_fib, type))
print(isinstance(num_fib_float, type))
print(isinstance(arr_fib_nums, type))
print(isinstance(obj_dict, type))

print(isinstance(obj_this_is_a_class_instance, type))
