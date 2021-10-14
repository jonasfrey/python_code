class Test_class:
    def __init__(self, arg1, arg2, **test):
        self.arg1 = arg1
        self.arg2 = arg2 
        for key, value in test.items():
          setattr(self, key, value)

t = Test_class('a1', 'a2', te=1, lol=2, xd=3)
print(t.__dict__)

# def i_do_sth(arg1, arg2, **test):
#     print("arg1")
#     print(arg1)
#     print("arg2")
#     print(arg1)
#     print("*")
#     print(*)

# def me_too(arg1, arg2, ):
#     print("arg1")
#     print(arg1)
#     print("arg2")
#     print(arg1)
#     print("*")
#     print(a*)
#     print("**")
#     print(aa**)