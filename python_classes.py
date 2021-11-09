class O_test():
    def __setattr__(self, s_name: str, value) -> None:
        print('__setattr__ was called !! ')
        self.__dict__[s_name] = value 

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self.s_default = 'inited this string'


o_test_instance = O_test(1,2)
# you can add attributes like so 
o_test_instance.s_added_from_with_dotnotaion_to_instance = 'i was added with instance_var_name.s_added_from_with_dotnotaion_to_instance = ...'
# or like so 
setattr(o_test_instance, 's_added_with_setattr', 'i was added with setattr(...) function')
print(o_test_instance.__dict__)


print(o_test_instance.s_added_from_with_dotnotaion_to_instance)
print(o_test_instance.s_added_with_setattr)


# you also can add an attribue with the __dict__[s_name] = value 
# but this way __setattr__ wont get called ! 
o_test_instance.__dict__['s_added_with_instance_var_name.__dict__[...]'] = 'i was added via .__dict__[s_name] = value'

# you then can access the attribute with dotnontaion
# only if the attribute name has no dots in it of corse 
# print(o_test_instance.s_added_with_instance_var_name.__dict__[...]) # this wont work

o_test_instance.__dict__['s_test'] = 'yes i am a string'

print(o_test_instance.s_test)
