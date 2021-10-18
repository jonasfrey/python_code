class Data():

    def __setattr__(self, name, value) -> None:
        # super().__setattr__(str(name), value)
        super(Data, self).__setattr__(name, value)

        print('attribute was set')


class Otherobj():
    def __init__(self):
        self.test = 1

d = Data()

d.test = 2 
d.otherobj = Otherobj()
d.otherobj.test = 2 
d.otherobj.test = 3 
d.otherobj.test = 4 


class ObservedDict(dict):
    def __init__(self, dict, pathname):
        self.pathname = pathname

    def __setitem__(self, item, value):
        print("You are changing the value of {} to {}!!".format(self.pathname, value))
        if type(value) is dict:
            od = ObservedDict(value, self.pathname+'.'+str(item))
            value = od 
        super(ObservedDict, self).__setitem__(item, value)

od = ObservedDict({}, 'od')


od['a'] = 2

od['a'] = {'a':2}

# my_dict.a.a = 3 
od['a']['a'] = 3 