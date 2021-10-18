# code ="""
# def f():
#     print("yay!")
# """
# f = compile(code, 'testfilename', 'exec')
# f()

# exec("def fun(x): return x + 1")
# print(fun(1))

import time 
import types

class test:
    def __init__(self):
        self.test = 11
        fname = 'fun'

    def add_ten(self, var):
        return var + 10 

    def set_n_get_function_by_string(self, string):
        funname = 'fun_'+str((int(time.time())))
        funstr = ''
        funstrlines = []
        funstrlines.append('def '+str(funname)+'(self):')

        for property in dir(self):
            print(property)
            funstrlines.append('    '+property+'='+'self.'+property)           
            # print(property, ":", value)

        #funstrlines.append('    return '+string)
        funstrlines.append('    '+string)
        funstr = "\n".join(funstrlines)
        #print(funstr) 
        exec(funstr)
        functionbody = locals()[funname]
        # we have to bind the method to the class in order to automatically
        # get the first parameter 'self'
        # simply setattr wont work
        # setattr(self, fname, lambda: functionbody(self))
        # this will bind the method to the self
        setattr(self, funname, types.MethodType( functionbody, self ))

        return getattr(self, funname)
            
t = test()

t.asdf = 100
# fun = t.set_n_get_function_by_string(
#     """self.test + 12"""
# )
f = t.set_n_get_function_by_string(
    """test + 12"""
)
print(f())

# not work
f = t.set_n_get_function_by_string(
    """asdf = 99"""
)
print(f())

f = t.set_n_get_function_by_string(
    """self.asdf = 99"""
)
print(f())


f = t.set_n_get_function_by_string(
    """add_ten(asdf)"""
)
print(f())


f = t.set_n_get_function_by_string(
    """print('printing from string function is workinmg')"""
)
print(f())
print(t.asdf)
    # def create_function_by_string(self):
    #     print(f(1))
    #     funname = 'fun_'+str((int(time.time())))
    #     funstr = 'def '+ funname + '(self): ' + 'return ' + 
