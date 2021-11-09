class Foo(object):

    def __init__(self):
        self._dirty = False

    def __setattr__(self, key, value):
        if key != '_dirty':
            if isinstance(value, list):
                self.__dict__[key] = list_observer(value, self.observer(self))
            else:
                self.__dict__[key] = value
            self._make_dirty()

    def _make_dirty(self):
        self._dirty = True
        print('is dirty')
        print('changed ...')
        self._dirty = False 

    def _not_dirty(self):
        self._dirty = False
        print('is no more dirty')

    class observer(object):
        """
        If a call to a method is made, this class prints the name of the method
        and all arguments.
        """

        def __init__(self, instance):
            self.instance = instance

        def p(self, *args):
            print(self.attr, args)
            self.instance._make_dirty()

        def __getattr__(self, attr):
            self.attr = attr
            return self.p


class list_observer(list):
    """
    Send all changes to an observer.
    """

    def __init__(self, value, observer):
        list.__init__(self, value)
        self.set_observer(observer)

    def set_observer(self, observer):
        """
        All changes to this list will trigger calls to observer methods.
        """
        self.observer = observer

    def __setitem__(self, key, value):
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

    def __delitem__(self, key):
        oldvalue = list.__getitem__(self, key)
        list.__delitem__(self, key)
        self.observer.list_del(self, key, oldvalue)

    def __setslice__(self, i, j, sequence):
        oldvalue = list.__getslice__(self, i, j)
        self.observer.list_setslice(self, i, j, sequence, oldvalue)
        list.__setslice__(self, i, j, sequence)

    def __delslice__(self, i, j):
        oldvalue = list.__getitem__(self, slice(i, j))
        list.__delslice__(self, i, j)
        self.observer.list_delslice(self, i, oldvalue)

    def append(self, value):
        list.append(self, value)
        self.observer.list_append(self)

    def pop(self):
        oldvalue = list.pop(self)
        self.observer.list_pop(self, oldvalue)

    def extend(self, newvalue):
        list.extend(self, newvalue)
        self.observer.list_extend(self, newvalue)

    def insert(self, i, element):
        list.insert(self, i, element)
        self.observer.list_insert(self, i, element)

    def remove(self, element):
        index = list.index(self, element)
        list.remove(self, element)
        self.observer.list_remove(self, index, element)

    def reverse(self):
        list.reverse(self)
        self.observer.list_reverse(self)

    def sort(self, cmpfunc=None):
        oldlist = self[:]
        list.sort(self, cmpfunc)
        self.observer.list_sort(self, oldlist)

class   My_obj():
    def __init__(self, object=None) -> None:
        self.nested_object = object
        self.simple_str_prop = 'aBcDeF'
        pass


if __name__ == '__main__':

    f = Foo()

    #change detected, f is dirty
    f.bar = ['foo']

    f.bar.append('asdf ')
    f.bar.append('asdf ')
    f.bar.append('asdf ')
    f.bar.append('asdf ')
    f.bar.append('asdf ')

    f.data = {
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
    f.data['nested_dict']['a_dict_attr'].pop(0)
    f.data['nested_dict']['a_dict_attr'].pop(0)
    f.data['nested_dict']['a_dict_attr'].pop(0)
    # f._not_dirty()

    # #change detected, f is dirty again
    # f.bar.append('bar')
