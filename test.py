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
arr_to_del = []
for str_attr, attr in obj_dict.items():
  if(str_attr != 'num_fib'):
    arr_to_del.append(str_attr)

for str_attr in arr_to_del:
    del obj_dict[str_attr]