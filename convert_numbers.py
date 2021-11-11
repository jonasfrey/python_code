class Hex_map(): 
    def __init__(self): 
        self.a = 10
        self.b = 11 
        self.c = 12
        self.d = 13 
        self.e = 14 
        self.f = 15

    def __getitem__(self, s_name, value):
        return self.__dict__[str(s_name).lower()]

class Polynom: 
    
    hex_map = Hex_map()

    def __init__(self, s_number, n_base):

        n_base = int(n_base)
        s_number = str(s_number)


        # a_coefficients = s_number.split('')
        # self.degree = len(a_coefficients)
        
        self.n_decimal = int(s_number,n_base)

        # n_dec_sum = 0
        # for n_index, s_char in a_coefficients:
            
        #     n_coefficient = int(s_char)
        #     n_exponent = len(a_coefficients) - n_index
        #     if(not s_char.isnumeric()):
        #         n_coefficient = Polynom.hex_map[s_char]

        #     n_dec_sum += n_coefficient * pow(n_base, n_exponent)
             
        
        # self.n_dec_sum = n_dec_sum

        # self.degree =
        #  
    def __repr__(self) -> str:
        n_binstrlen = len(str(self._dec_to_base(self.n_decimal, 2)))
        string = ""
        string += "     binary:"+self._dec_to_base(self.n_decimal, 2).rjust(n_binstrlen)+"\n"
        string += "     base 4:"+self._dec_to_base(self.n_decimal, 4).rjust(n_binstrlen)+"\n"
        string += "      octal:"+self._dec_to_base(self.n_decimal, 8).rjust(n_binstrlen)+"\n"
        string += "    decimal:"+self._dec_to_base(self.n_decimal, 10).rjust(n_binstrlen)+"\n"
        string += "hexadecimal:"+self._dec_to_base(self.n_decimal, 16).rjust(n_binstrlen)+"\n"
        
        return string
        pass
    def to_d(self):
        return self._dec_to_base(self.n_decimal, 10)
    def to_b(self):
        return self._dec_to_base(self.n_decimal, 2)
    def to_m(self):
        return self._dec_to_base(self.n_decimal, 4)
    def to_o(self):
        return self._dec_to_base(self.n_decimal, 8)
    def to_h(self):
        return self._dec_to_base(self.n_decimal, 16)

    def to_base(self, n_base):
        return self._dec_to_base(self.n_decimal, n_base)

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


class p(Polynom):
    pass

# def base_to_(base, string):

# def b2d(base, string):
#     a_chars = string.split('')

#     # polynom_degree = 
#     return "convert(2, '01011010')"


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
