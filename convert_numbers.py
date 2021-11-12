try:
    importing_possible = True
    import readline
    import numpy
except:
    importing_possible = False
    pass

try:
    import sys
    import_sys = True
except: 
    import_sys = False

def rjust(s_string, n_characters, s_character='_'):
    return '{s:{c}>{n}}'.format(s=s_string,n=n_characters,c=s_character)
    # return ('{:>{}}'.format(s_string, n_characters))
 
class Polynom:
     
    def __init__(self, s_number, n_base):
 
        n_base = int(n_base)
        s_number = str(s_number)
 
        self.n_base = n_base
        self.s_number = s_number
         
        self.n_decimal = int(s_number,n_base)
    
    def _get_polynomial_overview_string(self,n_decimal):

        string = ""
        string += self._get_formatted_string_by_base(2, n_decimal)
        string += self._get_formatted_string_by_base(4, n_decimal)
        string += self._get_formatted_string_by_base(8, n_decimal)
        string += self._get_formatted_string_by_base(10, n_decimal)
        string += self._get_formatted_string_by_base(16, n_decimal)
        
        return string

    def __repr__(self) -> str:
        
        string = ""

        string += self._get_polynomial_overview_string(self.n_decimal)

        string += str(self.get_decoded_string())

        return string

    def get_decoded_string(self):
        o_charsets = {
            'latin1' : '',
            'utf8' : '',
            'utf16' : '',
            'base64' : ''
            }
        o_charsets_decoded_bigendian = {}
        o_charsets_decoded_littleendian = {}
        s_charset_detected = 'no charset detected'
        s_decoded_string = ''

        for s_key, value in o_charsets.items(): 
            try:
                s_charset_detected = s_key
                n_bytes = int(len(self._dec_to_base(self.n_decimal, 16))/2)
                a_bytes_bigendian = self.n_decimal.to_bytes(n_bytes, 'big')
                a_bytes_littleendian = self.n_decimal.to_bytes(n_bytes, 'little')
                # s_decoded_string = bytes.fromhex(self._dec_to_base(self.n_decimal, 16)).decode(s_key) # only python version 3.5++
                o_charsets_decoded_bigendian[s_key] = a_bytes_bigendian.decode(s_key)
                o_charsets_decoded_littleendian[s_key] = a_bytes_littleendian.decode(s_key)

            except:
                continue 

        string = ""
        string += 'charsets decoded bigendian:' + str(o_charsets_decoded_bigendian) +"\n" 
        string += 'charsets decoded littleendian:' + str(o_charsets_decoded_littleendian) +"\n"

        return string
        # s_charset_detected + ' decoded :' + s_decoded_string

    def _get_complements_binary_string(self, two_complements=False):
        n_decimal = self.n_decimal
        if(two_complements):
            n_decimal = abs(self.n_decimal) - 1

        n_binary_abs = self._dec_to_base(abs(n_decimal), 2)
        
        n_next_highest_nibble = int(len(n_binary_abs) / 4) 
        n_next_highest_nibble += (len(n_binary_abs)/4 != 0) * 1

        n_number_of_bits_for_complement = n_next_highest_nibble * 4
        
        s_complement = rjust(n_binary_abs, n_number_of_bits_for_complement, '0')
        
        if(self.n_decimal < 0): 
            s_complement = self._switch_bits_in_string(
                s_complement
            )

        return s_complement

    def _switch_bits_in_string(self, s_string):

        s_switched_string = ""

        for bit in s_string:  
            if bit == "1":
                s_switched_string += "0"
            else:
                s_switched_string += "1"

        return s_switched_string
    def _get_formatted_string_by_base(self, n_base, n_decimal):
         
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
 
        n_binstrlen = len(str(self._dec_to_base(n_decimal, 2)))
 
        return rjust(s_for_base, n_rjust)+" : "+ rjust(self._dec_to_base(n_decimal, n_base), n_binstrlen)+"\n"
 
    def to_complements(self):
        string = ''
        string += "one's complement :"+ "\r\n"
        string += self._get_polynomial_overview_string(int(self._get_complements_binary_string(), 2))

        string += "two's complement: "+ "\r\n"
        string += self._get_polynomial_overview_string(int(self._get_complements_binary_string(True), 2))
        
        print(string)

    def to_d(self):
        print(self._to_formatted_string_by_base(10, self.n_decimal))
 
    def to_b(self):
        print(self._to_formatted_string_by_base(2, self.n_decimal))
 
    def to_m(self):
        print(self._to_formatted_string_by_base(4, self.n_decimal))
 
    def to_o(self):
        print(self._to_formatted_string_by_base(8, self.n_decimal))
 
    def to_h(self):
        print(self._to_formatted_string_by_base(16, self.n_decimal))
     
    def to_base(self, n_base):
        print(self._to_formatted_string_by_base(n_base, self.n_decimal))
 
    def _to_formatted_string_by_base(self, n_base, n_decimal):
        string = ''
        string += self._get_formatted_string_by_base(self.n_base, n_decimal)
        string += self._get_formatted_string_by_base(n_base, n_decimal)
        return string
 
    def _dec_to_base(self, num,base): #Maximum base - 36
        if(base > 36):
            raise Exception('base must be in { x | x < 37 }')
 
        base_num = ""
        while num>0:
            dig = int(num%base)
            if dig<10:
                base_num += str(dig)
            else:
                base_num += chr(ord('A')+dig-10) #Using uppercase letters
            num //= base
 
        # base_num = base_num[::-1] #To reverse the string
        base_num = "".join(reversed(base_num)) #To reverse the string

        if(base_num == ''):
            base_num = '0'

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
        if(not type(polynom) == single_p):
            raise Exception('second argument has to be type of class p')
        if(operator == "+"):
            n_sum_decimal = self.n_decimal + polynom.n_decimal
        if(operator == "-"):
            n_sum_decimal = self.n_decimal - polynom.n_decimal
        if(operator == "*"):
            n_sum_decimal = self.n_decimal * polynom.n_decimal
        if(operator == "/"):
            n_sum_decimal = self.n_decimal / polynom.n_decimal

        # n_sum_decimal = eval('self.n_decimal '+operator+' polynom.n_decimal')
 
        return p(n_sum_decimal, 10)
 
class p:
    def __new__(self, *arguments):
        a_arguments = list(arguments)
 
        if(len(a_arguments) > 2):
            return multiple_p(*arguments)
         
        return single_p(a_arguments[0], a_arguments[1])
 
class single_p(Polynom):
    pass
 
 
class multiple_p:
    def __init__(self, *arguments):
        a_arguments = list(arguments)
        self.n_base = a_arguments[-1]
        a_arguments.pop(-1)
        self.a_s_numbers = a_arguments
        self.a_p_instances = []

        for s_number in self.a_s_numbers:
            self.a_p_instances.append(single_p(str(s_number), self.n_base))
        
    def __repr__(self) -> str:
        string = ""
        for p in self.a_p_instances:
            string += str(p)+"\n"
 
        # print(string)
        return str(string)
 
    def __getattr__(self, s_attr):
        # print("getattr s_attr is")
        # print(s_attr)
        def callback(p):
            fun = getattr(p, s_attr)
            if(callable(fun)):
              print(fun())

        self._foreach_p_callback(callback)
 
    def _foreach_p_callback(self, callback):
        for p in self.a_p_instances:
            callback(p)
 
def help():
    string = ""
    string += "usage: " + "\r\n"
    string += "p(number, base).{ function_name }" + "\n"
    string += "\n"
    string += "available functions are:" + "\r\n"
    string += "\n"
    for s_name in dir(Polynom):
        if(not s_name.startswith("_")):
            string +=  "p(number, base)."+ s_name + "\r\n"
    print(string)


 
def multiline_print(arg):
 
    if(type(arg) is str):
      if("\n" in str):
        a_strings = arg.split("\n")
        for s_string in a_strings:
            print(s_string)
     
    print(arg)
 
def h():
    return help()

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
```python
print( p(2, 4, 8, 16, 32, 128, 243, 10).to_b() ) 
```

# hex to charset 
you can convert a hexstring, the charset will be detected
```python
print(p('c3b666666e656e6465',16))
```

"""
if(import_sys):
    print("wälcöm !")
    print("sys.version")
    print(sys.version)
    print("for help enter 'h()'")

if(importing_possible):
    try:
        s_current_file_name = __file__ 
        s_cur_file_name_no_ext = (s_current_file_name.split('.').pop(0))
        f = open(s_cur_file_name_no_ext+"_documentation.md", "w")
        f.write(s_markdown_doc)
        f.close()
    except:
        pass
    # testing
    print('--- start testing ---')
        
    # # get all bases
    # print( p(243, 10) )

    # # get a specific base
    # print( p(243, 10).to_b() )
    # print( p(243, 10).to_m() )
    # print( p(243, 10).to_o() )
    # print( p(243, 10).to_h() )

    # # get a specific custom base
    # print( p(243, 10).to_base(13) )

    # # ps
    # print(p(123,323,4342,23,1234,10))
    # print(p(123,323,4342,23,1234,10).to_b())

    # print(p(7,10))

    print(p(-7,10))

    # print(p(-50,10))

    # testing utf8 or latin1
    print(p('f6646c616e646573',16))

    #random number just for fun
    print(p(4208869,10))

    # from reference test
    print(p('616d62696775ef74e9',16))

    print(p('f66468656974656e',16))

    print(p('64e96ae0',16))

    print(p('c3b666666e656e6465',16))

    print('--- end testing ---')

    # while(True):
    #     string = ("h for help\n")
    #     string += ("q for quit\n")
    #     val = input(string+"enter:")

    #     if(val == 'q'):
    #         break
            
    #     exec('def tmp_fun():\n evaluated_return = '+str(val)+'\n return evaluated_return')
    #     evaluated_return = tmp_fun()
    #     print("")
    #     multiline_print(evaluated_return)
    #     print("")
    
