class printargs(object):
    """
    If a call to a method is made, this class prints the name of the method
    and all arguments.
    """
    def p(self, *args):
        print('!! changed !!')
        print(self.attr, args)
    def __getattr__(self, attr):
        self.attr = attr
        return self.p

"""
Implement an observer pattern for lists and dictionaries.

A subclasses for dicts and lists are defined which send information
about changes to an observer.

The observer is sent enough information about the change so that the
observer can undo the change, if desired.
"""
class list_observer(list):
    """
    Send all changes to an observer.
    """
    
    def __init__ (self,value,observer):
        list.__init__(self,value)
        self.set_observer(observer)
    
    def set_observer (self,observer):
        """
        All changes to this list will trigger calls to observer methods.
        """
        self.observer = observer 
    
    def __setitem__ (self,key,value):
        """
        Intercept the l[key]=value operations.
        Also covers slice assignment.
        """
        try:
            oldvalue = self.__getitem__(key)
        except KeyError:
            list.__setitem__(self, key, value)
            self.observer.list_create(self, key)
        else:
            list.__setitem__(self, key, value)
            self.observer.list_set(self, key, oldvalue)
    
    def __delitem__ (self,key):
        oldvalue = list.__getitem__(self, key)
        list.__delitem__(self, key)
        self.observer.list_del(self, key, oldvalue)
    
    def __setslice__ (self, i, j, sequence):
        oldvalue = list.__getslice__(self, i, j)
        self.observer.list_setslice(self, i, j, sequence, oldvalue)
        list.__setslice__(self, i, j, sequence)
    
    def __delslice__ (self, i, j):
        oldvalue = list.__getitem__(self, slice(i, j))
        list.__delslice__(self, i, j)
        self.observer.list_delslice(self, i, oldvalue)
    
    def append (self,value):
        list.append(self,value)
        self.observer.list_append(self)
    
    def pop (self, index):
        oldvalue = list.pop(self, index)
        self.observer.list_pop(self,oldvalue)
    
    def extend (self, newvalue):
        list.extend(self, newvalue)
        self.observer.list_extend(self, newvalue)
    
    def insert (self, i, element):
        list.insert(self, i, element)
        self.observer.list_insert(self, i, element)
    
    def remove (self, element):
        index = list.index(self, element)
        list.remove(self, element)
        self.observer.list_remove(self, index, element)
    
    def reverse (self):
        list.reverse(self)
        self.observer.list_reverse(self)
    
    def sort (self,cmpfunc=None):
        oldlist = self[:]
        list.sort(self,cmpfunc)
        self.observer.list_sort(self, oldlist)

printargs_observer  = printargs()

class Observed_o(dict):
    def __init__(self, root_o):
        self.recursive_update_attributes(root_o)

    def __setitem__(self, item, value):
        
        if(value.__class__.__module__ != 'builtins'):
            value = Observed_o(value)
        if isinstance(value, dict):
            value = Observed_o(value)
        if isinstance(value, list):
            value = list_observer(value, printargs_observer)


        # print("type(value)")
        # print(type(value))
        print("__setitem__ was caled, string : %s , value: %s"%(item, value))
        
        super(Observed_o, self).__setitem__(item, value)

    def recursive_update_attributes(self, dir_or_object_or_list):
        if isinstance(dir_or_object_or_list, list):
            for (key, val)in enumerate(dir_or_object_or_list):
                if( isinstance(val, list)):
                    dir_or_object_or_list[key] = list_observer(val, printargs_observer)
                if(dir_or_object_or_list.__class__.__module__ != 'builtins'):
                    dir_or_object_or_list[key] = Observed_o(dir_or_object_or_list)
                if isinstance(dir_or_object_or_list, dict):
                    dir_or_object_or_list[key] = Observed_o(dir_or_object_or_list)

            dir_or_object_or_list = list_observer(dir_or_object_or_list, printargs_observer)


        if isinstance(dir_or_object_or_list, dict):
            # loop over dict attrs 
            for s_attr, attr in dir_or_object_or_list.items():
                # print(attr)
                # print(s_attr)
                if(not s_attr.startswith('_')):

                    self.__setitem__(s_attr, attr)
        if(dir_or_object_or_list.__class__.__module__ != 'builtins'):
            # loop over class instance attrs 
            for s_attr in dir(dir_or_object_or_list):
                print(s_attr)
                if(not s_attr.startswith('_')):

                    attr = getattr(dir_or_object_or_list, s_attr)
                    print(attr)
                    self.__setitem__(s_attr, attr)




class   My_obj():
    def __init__(self, object=None) -> None:
        self.nested_object = object
        self.simple_str_prop = 'aBcDeF'
        pass

dict_obj_mix = {
    'dict_prop': True, 
    'b_dict_attr': True, 
    'n_dict_attr': 1, 
    'n_dict_attr': 1.1, 
    's_dict_attr': 1.1, 
    'a_dict_attr': [1,2,3,4,5], 
    'obj_instance': My_obj(My_obj()), 
    'nested_dict': {
        'dict_prop': True, 
        'b_dict_attr': True, 
        'n_dict_attr': 1, 
        'n_dict_attr': 1.1, 
        's_dict_attr': 1.1,  
        'a_dict_attr': [1,2,3,4,5],  
        'obj_instance': My_obj(My_obj()), 
    }
}

simple_dict = {
    'simple_string': 'judihui'
}

obseved_o = Observed_o(simple_dict)


print(obseved_o['simple_string'])
obseved_o['simple_string'] = "nonononon"


simple_dict_nested = {
    'nested_dict': {
        'simple_string': 'test2',
        'a_test': [1,2,3]
    }
}

obseved_o = Observed_o(simple_dict_nested)

obseved_o['nested_dict']['simple_string'] = 'ok i changed'
print(obseved_o['nested_dict']['a_test'])
obseved_o['nested_dict']['a_test'].append('test')
obseved_o['nested_dict']['a_test'].pop(0)
obseved_o['nested_dict']['a_test'].append(simple_dict_nested)
print(obseved_o['nested_dict']['a_test'][3]['nested_dict']['a_test'])

obseved_o['nested_dict']['a_test'][3]['nested_dict']['a_test'].append('asdf')
obseved_o['nested_dict']['a_test'][3]['nested_dict']['a_test'].append('asdf')
obseved_o['nested_dict']['a_test'][3]['nested_dict']['a_test'].append('asdf')
obseved_o['nested_dict']['a_test'][3]['nested_dict']['a_test'].append('asdf')

# obseved_o['nested_dict']['a_dict_attr'].pop(0)
# print(obseved_o['nested_dict']['a_test'])
# obseved_o['nested_dict'] = 'xD xD xD'


# #jsonfile approach
# import jsonfile

# class Observed_o(jsonfile.JSONFileRoot):
#   def on_change(self):
#     print(f'notify: {self.data}')



# observed_o = Observed_o('jsonfiletest.json')
# obseved_o.data = dict_obj_mix


# obseved_o.data["nested_dict"]["a_dict_attr"].pop(0)
# obseved_o.data["nested_dict"]["a_dict_attr"].pop(0)