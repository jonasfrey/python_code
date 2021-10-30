import functools
def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        if(type(obj) is list and attr.isnumeric()):
            return obj[int(attr)]
        if(type(obj) is dict):
            return obj.get(attr, *args)
        
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


my_dict = {
    'a':[
        0,1,2,3,4,[
            'yess!'
        ]
    ]
}
print(rgetattr(my_dict, 'a'))
print(rgetattr(my_dict, 'a.1'))
print(rgetattr(my_dict, 'a.5'))
print(rgetattr(my_dict, 'a.5.0'))