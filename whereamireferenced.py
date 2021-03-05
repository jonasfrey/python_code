class Foo:
    def __init__(self, parent_class_instance)
        self.parent_class_instance = parent_class_instance

class Bar:
    def __init__(self)
        test = Foo(self)
        print(self.every_instance_where_Bar_is_referenced) # should print [Foo]


#possible like that 

import gc
class Foo:
    def __init__(self, parent_class_instance):
        self.parent_class_instance = parent_class_instance

class Bar:
    def __init__(self):
        test = Foo(self)
        print(gc.get_referrers(self)) # should print Foo
Bar()

# or possible like that


class Foo:
    registered_instances = []

    def __init__(self, name):
        self.registered_instances.append(self)
        self.name = name

    def __repr__(self):
        return repr(vars(self))


class Bar:
    def __init__(self):
        test = Foo(name='test')
        snork = Foo(name='snork')
        print(test.registered_instances)


b = Bar()