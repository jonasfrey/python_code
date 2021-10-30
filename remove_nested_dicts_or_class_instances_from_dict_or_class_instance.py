def remove_nested_dicts_or_class_instances_from_dict_or_class_instance(obj):
    arr_attrs_to_delete = []
    # obj.__class__.__module__ == 'builtins' checks if obj is user defined class via 'class my_class_name:...'
    if(obj.__class__.__module__ != 'builtins'):
        # loop over class instance attrs
        for str_attr in dir(obj):
            # ignore the builtin python attributes
            if(str_attr.startswith('__')):
                continue
            attr = getattr(obj, str_attr)
            if(attr.__class__.__module__ != 'builtins' or type(attr) is dict):
                arr_attrs_to_delete.append(str_attr)

    if(type(obj) is dict):
        # loop over dict attrs 
        for str_attr, attr in obj.items():
            if(attr.__class__.__module__ != 'builtins' or type(attr) is dict):
                arr_attrs_to_delete.append(str_attr)

    for str_attr_to_delete in arr_attrs_to_delete:
        if(obj.__class__.__module__ != 'builtins'):
            delattr(obj, str_attr_to_delete)
        if(type(obj) is dict):
            del obj[str_attr_to_delete]

# tests
import pprint 

class Test_class:
    pass 

obj_dict = {
    'a' : '2',
    'b' : True,
    'obj_nested_dict': { 'str' : 'hello'},
    'obj_nested_dict': { 'dict' : {}},
    'c': "asdf", 
    'class_instance': Test_class()
}

print('before')
pprint.pprint(obj_dict)
remove_nested_dicts_or_class_instances_from_dict_or_class_instance(obj_dict)
print('after')
pprint.pprint(obj_dict)


# test for object with nested objects, dicts
class A:
    def __init__(self, nested_class_instance=None):
        self.a = 1
        self.b = 2
        self.nested_class_instance = nested_class_instance
        self.c = True


a_instance = A(A())

print('before')
pprint.pprint(a_instance.__dict__)
remove_nested_dicts_or_class_instances_from_dict_or_class_instance(a_instance)
print('after')
pprint.pprint(a_instance.__dict__)
