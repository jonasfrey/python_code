from munch import *

o_dict = {
    's_hello' : 'hello',
    'b_is_inited' : True,
    'n_fib' : 11235,
    'n_fib_float' : 112.35,
    'a_fib_nums' : [1,1,2,3,5],
    'o_dict_nested': {
        's_hello' : 'hello',
        'b_is_inited' : True,
        'n_fib' : 11235,
        'n_fib_float' : 112.35,
        'a_fib_nums' : [1,1,2,3,5]
    }
}

undefined = object()

o_class_instance_with_dot_notation_access = (
    DefaultMunch.fromDict(o_dict, undefined)
)
print(
    o_class_instance_with_dot_notation_access.n_fib
)

print(
    o_class_instance_with_dot_notation_access.o_dict_nested
)

o_class_instance_with_dot_notation_access.o_dict_nested.asdf = '3'