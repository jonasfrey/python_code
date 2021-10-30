
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

# loop over class instance attrs 
for str_attr in dir(obj_this_is_a_class_instance):
    attr = getattr(obj_this_is_a_class_instance, str_attr)
    print(attr)
    print(str_attr)

# loop over dict attrs 
for str_attr, attr in obj_dict.items():
    print(attr)
    print(str_attr)