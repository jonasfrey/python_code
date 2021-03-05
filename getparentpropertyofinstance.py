#will work
class Foo:
    def __init__(self, parent_class_instance)
        self.parent_class_instance = parent_class_instance
        print(self.parent_class_instance) # will print Bar

class Bar:
    def __init__(self)
        self.foos = []
        self.foos.append(Foo(self))

#wont work
class Foo2:
    def __init__(self)
        print(self.parent_class_instance) # will print Bar

class Bar2:
    def __init__(self)
        self.foos2 = []
        self.foos2.append(Foo2())
