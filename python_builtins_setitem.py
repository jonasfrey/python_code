# allright i guess __setitem__ is the same as __setattr__ only that it is dedicated to dicts

class O_test: 

    def __setitem__(self, key , value): 
        print('__setitem__ was called ! ')
        self.__dict__.__setitem__(key, value)
        pass


class O_test_without_setitem:
    def __init__(self) -> None:
        pass


o_test_instance = O_test()

o_test_instance['asdf'] = 2

print("print o_test_instance.__dict__")
print(o_test_instance.__dict__)
print(o_test_instance.asdf)

# when we try to do it on a class without setitem , we will get an error
o_test_instance_without_setitem = O_test_without_setitem()
# TypeError: 'O_test_without_setitem' object does not support item assignment
o_test_instance_without_setitem['asdf'] = 2

print("print o_test_instance_without_setitem.__dict__")
print(o_test_instance_without_setitem.__dict__)
print(o_test_instance_without_setitem.asdf)
