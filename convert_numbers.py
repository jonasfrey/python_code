import readline

class Polynom: 
    
    def __init__(self, s_number, n_base):

        n_base = int(n_base)
        s_number = str(s_number)

        self.n_base = n_base
        self.s_number = s_number
        
        self.n_decimal = int(s_number,n_base)

    def __repr__(self) -> str:
        n_binstrlen = len(str(self._dec_to_base(self.n_decimal, 2)))
        string = ""
        string += self._get_formatted_string_by_base(2)
        string += self._get_formatted_string_by_base(4)
        string += self._get_formatted_string_by_base(8)
        string += self._get_formatted_string_by_base(10)
        string += self._get_formatted_string_by_base(16)
        return string
        pass

    def _get_formatted_string_by_base(self, n_base):
        
        o_dictmap = {
            "2":"binary",
            "4":"base4",
            "4":"marsian",
            "8":"octal",
            "10":"decimal",
            "16":"hexadecimal",
        }
        longest_s_val_in_s_dict = o_dictmap[next(iter(o_dictmap))]

        for s in o_dictmap: 
            if(len(o_dictmap[s]) > len(longest_s_val_in_s_dict) ):
                longest_s_val_in_s_dict = o_dictmap[s]
        
        n_rjust = len(longest_s_val_in_s_dict)

        if(str(n_base) in o_dictmap):
            s_for_base = o_dictmap[str(n_base)]


        if(not str(n_base) in o_dictmap):
            s_for_base = 'base_'+str(n_base)

        n_binstrlen = len(str(self._dec_to_base(self.n_decimal, 2)))

        return s_for_base.rjust(n_rjust)+" : "+self._dec_to_base(self.n_decimal, n_base).rjust(n_binstrlen)+"\n"


    def to_d(self):
        return self._to_formatted_string_by_base(10)

    def to_b(self):
        return self._to_formatted_string_by_base(2)

    def to_m(self):
        return self._to_formatted_string_by_base(4)

    def to_o(self):
        return self._to_formatted_string_by_base(8)

    def to_h(self):
        return self._to_formatted_string_by_base(16)
    
    def to_base(self, n_base):
        return self._to_formatted_string_by_base(n_base)

    def _to_formatted_string_by_base(self, n_base):
        string = ''
        string += self._get_formatted_string_by_base(self.n_base)
        string += self._get_formatted_string_by_base(n_base)
        return string

    def _dec_to_base(self, num,base):  #Maximum base - 36
        if(base > 36):
            raise Exception('base must be in { x | x < 37 }')

        base_num = ""
        while num>0:
            dig = int(num%base)
            if dig<10:
                base_num += str(dig)
            else:
                base_num += chr(ord('A')+dig-10)  #Using uppercase letters
            num //= base

        base_num = base_num[::-1]  #To reverse the string
        return base_num

    def __add__(self, polynom):
        return self._operate_with_polynom(polynom, "+")

    def __sub__(self, polynom):
        return self._operate_with_polynom(polynom, "-")
    
    def __mul__(self, polynom):
        return self._operate_with_polynom(polynom, '*')

    def __truediv__(self, polynom):
        return self._operate_with_polynom(polynom, '/')


    def _operate_with_polynom(self, polynom, operator):
        print(type(polynom))
        if(not type(polynom) == p):
            raise Exception('second argument has to be type of class p')
        
        
        n_sum_decimal = eval('self.n_decimal '+operator+' polynom.n_decimal')

        return p(n_sum_decimal, 10)


class p:
    def __new__(self, *arguments):
        a_arguments = list(arguments)

        if(len(a_arguments) > 2):
            return multiple_p(arguments)
        
        return single_p(a_arguments[0], a_arguments[1]) 

class single_p(Polynom):
    pass

class multiple_p:
    def __init__(self, *arguments): 
        a_arguments = list(arguments)
        self.n_base = a_arguments[-1]
        a_arguments.pop(-1)
        self.a_s_numbers = a_arguments
        self.ps = []
        for s_number in self.a_s_numbers:
            self.ps.append(single_p(s_number, self.n_base))
        

    def __repr__(self) -> str:
        string = ""
        for p in self.ps:
            string += str(p)+"\n"

        # print(string)
        return str(string)

    def to_d(self):
        return self._foreach_to_base(10)

    def to_b(self):
        return self._foreach_to_base(2)

    def to_m(self):
        return self._foreach_to_base(4)

    def to_o(self):
        return self._foreach_to_base(8)

    def to_h(self):
        return self._foreach_to_base(16)
    
    def to_base(self, n_base):
        return self._foreach_to_base(n_base)

    def _foreach_to_base(self, n_base): 
        string = ""
        for p in self.ps: 
            string += p._to_formatted_string_by_base(n_base) + "\n"

        return string

def help():
    # p = Polynom('10', 10)
    string = ""
    string += "usage: " + "\n"
    string += "p(number, base).{ function_name }" + "\n"
    string += "available functions are:" + "\n"
    for s_name in dir(Polynom):
        if(not s_name.startswith("_")):
            string += s_name + "\n"
    return string
    # print(dir(p))
    # l = []
    # for key, value in locals().items():
    #     if callable(value) and value.__module__ == __name__:
    #         l.append(key)
    # print(l)

def h():
    return help()


if __name__ == "__main__":
    h = h()
    help = help()

    s_markdown_doc = """
# usage 
## convert number to all possible bases 
```python
# input the number with its base
print( p(243, 10) )
```
## convert number to only one desired base
```python
# to_b -> 'to binary'
# to_m -> 'to marsian/base 4'
# to_o -> 'to octal'
# to_h -> 'to hexadecimal'
print( p(243, 10).to_b() )
```
## convert number to only one custom base
```python
print( p(243, 10).to_base(13) )
```

## calculating/operating with numbers

you can operate with two instances

```python
print( p(243, 10) + p(10010, 2) )

print( p(243, 10) - p(10010, 2) )

print( p(243, 10) * p(10010, 2) )

print( p(243, 10) / p(10010, 2) )

```

since a new p(...) instance is returned you can apply more functions after wrapping the return in round brackets (p(...) + p(...)).to_h()
```python

print( ( p(243, 10) + p(10010, 2) ).to_base(13)

```

# multiple conversion array/list/batch 
you can convert multiple numbers , by using the p like this
```
print( p(2, 4, 8, 16, 32, 128, 243, 10).to_b() )
```
"""
    try: 
        s_current_file_name = __file__
        s_cur_file_name_no_ext = (s_current_file_name.split('.').pop(0))
        f = open(s_cur_file_name_no_ext+"_documentation.md", "a")
        f.write(s_markdown_doc)
        f.close()
    
    except:
        pass

    # testing 
    
    # get all bases
    print( p(243, 10) )

    # get a specific base 
    print( p(243, 10).to_b() )
    print( p(243, 10).to_m() )
    print( p(243, 10).to_o() )
    print( p(243, 10).to_h() )

    # get a specific custom base
    print( p(243, 10).to_base(13) )

    # ps 
    print(p(123,323,4342,23,1234,10))
    print(p(123,323,4342,23,1234,10).to_b())


    while(True):
        string = ("h for help\n")
        string += ("q for quit\n")
        val = input(string+"enter:")

        if(val == 'q'):
            break
        
        exec('def tmp_fun():\n   evaluated_return = '+str(val)+'\n   return evaluated_return')
        evaluated_return = tmp_fun()
        print("")
        print(evaluated_return)
        print("")
