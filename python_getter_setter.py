class Test: 
    def __init__(self):
        self.test = "test"

    def __setattr__(self,name, value):
        print(self)
        print(name)
        print(value)



t = Test()
t.asdf = "asdfasdf"