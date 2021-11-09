class O_class:
    # def __init__(self, dict_or_classinstance) -> None:
    #     if isinstance(dict_or_classinstance, list):
    #         print('ERROR: root arg cannot be type list') 

    #     self.recursive_update_attributes(dict_or_classinstance)

    def __setattr__(self, s_name: str, value) -> None:
        if( 
            value.__class__.__module__ != 'builtins' or 
            isinstance(value, dict) or 
            isinstance(value, list)
        ):
            print('now')
            value = O_class(value)    
            print(type(value))                
        setattr(self, s_name, value) # this would end in max recursion depth reached
        #self.__dict__[s_name] = value # setting the attribute via __dict__ wont call __setattr__
        pass

    
    def __new__(self, dict_or_classinstance_or_list):
        """
        with the __new__ funtion we have control over the return value
        """
        if isinstance(dict_or_classinstance_or_list, list):
            for (key, val)in enumerate(dict_or_classinstance_or_list):
                dict_or_classinstance_or_list[key] = O_class(val)

            return dict_or_classinstance_or_list

        if not isinstance(dict_or_classinstance_or_list, list):
            self.recursive_update_attributes(self, dict_or_classinstance_or_list)
            return self

    def recursive_update_attributes(self, dict_or_classinstance):
        if isinstance(dict_or_classinstance, dict):
            # loop over dict attrs 
            for s_attr, attr in dict_or_classinstance.items():
                # print(attr)
                # print(s_attr)
                if(not s_attr.startswith('_')):
                    self.__setattr__(self, s_attr, attr)

        if(dict_or_classinstance.__class__.__module__ != 'builtins'):
            # loop over class instance attrs 
            for s_attr in dir(dict_or_classinstance):
                if(not s_attr.startswith('_')):

                    attr = getattr(dict_or_classinstance, s_attr)
                    print(attr)
                    self.__setattr__(self, s_attr, attr)


###### Testing 

o_dict_nested_three_times = {
    'str_hello' : 'hello',
    'boo_is_inited' : True,
    'num_fib' : 11235,
    'num_fib_float' : 112.35,
    'arr_fib_nums' : [1,1,2,3,
            [1,2,3, 
                { 
                    "s_test": "m51"
                }
            ], 
            {
                "s_test": "m106"
            }
        ],
    'obj_dict_nested': {
        'str_hello' : 'hello',
        'boo_is_inited' : True,
        'num_fib' : 11235,
        'num_fib_float' : 112.35,
        'arr_fib_nums' : [1,1,2,3,
                [1,2,3, 
                    { 
                        "s_test": "m51"
                    }
                ], 
                {
                    "s_test": "m106"
                }
            ], 
        'obj_dict_nested': {
            'str_hello' : 'hello',
            'boo_is_inited' : True,
            'num_fib' : 11235,
            'num_fib_float' : 112.35,
            'arr_fib_nums' : [1,1,2,3,
                    [1,2,3, 
                        { 
                            "s_test": "m51"
                        }
                    ], 
                    {
                        "s_test": "m106"
                    }
                ]
        }
    }
}

o_converted = O_class(o_dict_nested_three_times)
print(type(o_converted))
# c create
o_converted.s_added_after_convertion = 'yes i was added after conversion'
o_converted.obj_dict_nested.s_added_after_convertion = 'nested, yes i was added after conversion'
o_converted.obj_dict_nested.obj_dict_nested.s_added_after_convertion = 'nested nested, yes i was added after conversion'

# r read 
print(o_converted.s_added_after_convertion)
print(o_converted.obj_dict_nested.s_added_after_convertion)
print(o_converted.obj_dict_nested.obj_dict_nested.s_added_after_convertion)

# u update 
#skipping this 


# d delete 
del o_converted.s_added_after_convertion
del o_converted.obj_dict_nested.s_added_after_convertion
del o_converted.obj_dict_nested.obj_dict_nested.s_added_after_convertion


print(o_converted.obj_dict_nested.obj_dict_nested.arr_fib_nums)
print(o_converted.obj_dict_nested.obj_dict_nested.arr_fib_nums[4])
print(o_converted.obj_dict_nested.obj_dict_nested.arr_fib_nums[4][3].s_test)