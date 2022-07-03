

class O_polynom:
    def __init__(
        self, 
        n_result_number, 
        a_o_coefficient,
        s_name 
    ):
        self.s_name = s_name
        self.n_result_number = n_result_number
        self.a_o_coefficient = a_o_coefficient
    def f_s_equation(self): 
        s_equation = f"{self.n_result_number}="
    
        for o in self.a_o_coefficient:
            if(o.n_factor>=0):
                s_equation+="+"
            # s_equation+=str(o.n_factor)
            s_equation+="{:g}".format(float(o.n_factor)) # 3.0 -> 3 , 3.440 -> 3.44
            s_equation+=str(o.s_variable_char)
        return s_equation
            
    def f_s_equation_solved_for_one_coefficient(
        self
    ):
        o_polynom_simplified = self.f_o_simplified()
        a_s_line = []
        a_s_line.append(self.f_s_equation())
        a_o_filtered = [
                o for o in o_polynom_simplified.a_o_coefficient
                if(o.n_factor != 0)
            ]
        if(len(a_o_filtered) == 1):
            o_coefficient = a_o_filtered[0]
            a_s_line.append(f"{self.f_s_equation()} | ...")
            a_s_line.append(f"{o_polynom_simplified.f_s_equation()} | : {o_coefficient.n_factor}")
            a_s_line.append(f"{o_polynom_simplified.n_result_number / o_coefficient.n_factor} = {1}{o_coefficient.s_variable_char}")
        else: 
            return f"cannot solve for one variable since multiple variables have a factor of not zero!,equation is : {a_s_line[0]}"
        return "\n".join(a_s_line)

    def f_o_simplified(self):
        a_o_coefficient = []
        # remove coefficent with same variable name
        # 12 = 3x + 5y + 2y + x + 22 -> 12 = 4x + 7y + 22
        a_s_variable_char = []
        for o_coefficient in self.a_o_coefficient: 
            if(o_coefficient.s_variable_char.strip() == ""):
                continue
            if(o_coefficient.s_variable_char in a_s_variable_char):
                continue
            if(o_coefficient.n_factor == 0): 
                continue
            a_o = [
                o for o in self.a_o_coefficient
                if o.s_variable_char == o_coefficient.s_variable_char
            ]
            
            n_factor_sum = 0
            s_variable_char = o_coefficient.s_variable_char
            for o in a_o: 
                # print("o.s_variable_char")
                # print(o.s_variable_char)
                # print(o.n_factor)
                n_factor_sum = eval(
                    str(n_factor_sum) +
                    "+" +
                    str(o.n_factor) 
                )

            
            a_o_coefficient.append(
                O_coefficient(
                    s_variable_char,
                    float(n_factor_sum), 
                )
            )
            a_s_variable_char.append(s_variable_char)


        # remove coefficient without any variable 
        # 12 = 4x + 7y + 22 -> 32 = 4x + 7y
        a_o = [
                o for o in self.a_o_coefficient
                if o.s_variable_char.strip() == "" 
        ]
        # print(a_o)

        n_result_number = self.n_result_number
        for o in a_o: 
            # print("o.s_variable_char")
            # print(o.s_variable_char)
            # print("o.n_factor")
            # print(o.n_factor)

            n_result_number = eval(
                str(n_result_number) +
                "+" +
                str(o.n_factor)
                )

        return O_polynom(
            float(n_result_number), 
            a_o_coefficient,
            self.s_name
        )

    def f_o_substite_coefficient(
        self,
        s_variable_char, 
        n_value
    ):
        o_polynom = self.f_o_simplified()
        o_coefficient = [
            o for o in o_polynom.a_o_coefficient
            if o.s_variable_char == s_variable_char
        ][0]
        a_o_coefficient = [
            o for o in o_polynom.a_o_coefficient
            if o.s_variable_char != s_variable_char
        ]
        a_o_coefficient.append(
            O_coefficient(
                "", 
                eval(str(o_coefficient.n_factor) +"*"+ str(n_value))
            )
        )
        # n_result_number = eval(str(o_polynom.n_result_number) + "+" + str(o_coefficient.n_factor) +"*"+ str(n_value))
        s_name = f"{o_polynom.s_name} substituted {s_variable_char} with {n_value}"
        o_polynom_substitued = O_polynom(
            o_polynom.n_result_number, 
            a_o_coefficient,
            s_name
        )
        print(o_polynom_substitued.s_name)
        print(o_polynom_substitued)
        o_polynom_substitued_simplified = o_polynom_substitued.f_o_simplified()
        return o_polynom_substitued_simplified

    def __str__(self):
        # print(self)
        return self.f_s_equation()

    def __mul__(self, s_operation_suffix):
        # when object is on left side => o_polynom * 2 
        return self.f_o_polynom_operated(
            s_operation_suffix, 
            "*"
        )

    def __rmul__(self, s_operation_suffix):
        return self.f_o_polynom_operated(
            s_operation_suffix, 
            "*"
        )
    def __add__(self, variable):
        s_operator = "+"
        return self.f_o_dunder_sum(variable, s_operator)

    def __radd__(self, variable):
        s_operator = "+"
        return self.f_o_dunder_sum(variable, s_operator)

    def __sub__(self, variable):
        s_operator = "-"
        return self.f_o_dunder_sum(variable, s_operator)

    def __rsub__(self, variable):
        s_operator = "-"
        return self.f_o_dunder_sum(variable, s_operator)

    def f_o_dunder_sum(
        self,
        variable,
        s_operator  
    ):
        # print("f_o_dunder_sum")

        if(isinstance(variable, str)):
            return self.f_o_polynom_operated(
                variable, 
            )
        if(isinstance(variable, O_polynom)):
            return self.f_o_polynom_sum_with_o_polynom(variable, s_operator)

    def f_o_polynom_sum_with_o_polynom(
        self, 
        o_polynom,
        s_operator
    ):  
        s = str(self.n_result_number) + s_operator + str(o_polynom.n_result_number)
        
        n_result_number = eval(s)

        a_o_coefficient = []

        for o_coefficient in self.a_o_coefficient: 
            o_coefficient_for_operation = [
                o for o in o_polynom.a_o_coefficient
                if o.s_variable_char.lower() == o_coefficient.s_variable_char.lower()
                ][0]

            a_o_coefficient.append(    
                O_coefficient(
                    o_coefficient.s_variable_char, 
                    eval(str(o_coefficient.n_factor)+s_operator+str(o_coefficient_for_operation.n_factor))
                )
            )

        o_polynom_operation_result = O_polynom(
            n_result_number,
            a_o_coefficient, 
            f"({self.s_name}) {s_operator} ({o_polynom.s_name})" 
        )

        return o_polynom_operation_result
            
    def f_o_polynom_operated(
        self,
        s_operation_suffix, # can be a string for example (2.0/3), 
        s_operator_prefix 
    ):
        if(s_operation_suffix[0] == s_operator_prefix): 
            print(f"s_operation_suffix '{s_operation_suffix}' should not start with an operator, it is added in the function")
            exit()

        s = str(self.n_result_number) + s_operator_prefix + s_operation_suffix

        n_result_number = eval(s)

        a_o_coefficient = []
        for o_coefficient in self.a_o_coefficient: 
            a_o_coefficient.append(
                O_coefficient(
                    o_coefficient.s_variable_char, 
                    eval(
                        str(o_coefficient.n_factor)+s_operator_prefix+s_operation_suffix
                    )
                )
            )
        
        o_polynom = O_polynom(
            n_result_number, 
            a_o_coefficient, 
            self.s_name + s_operator_prefix + s_operation_suffix
        )
        return o_polynom

def f_o_polynom_by_equation_string(
    s_string, 
    s_name = ""
): 
    s_equation_no_double_operators = s_string.replace("+-", "-")
    s_equation_no_double_operators = s_equation_no_double_operators.replace("-+", "-")
    s_equation_no_double_operators = s_equation_no_double_operators.replace("--", "+")
    s_equation_no_double_operators = s_equation_no_double_operators.replace("++", "+")
    s_equation_no_double_operators = s_equation_no_double_operators.replace("*", "")
    s_equation_no_double_operators = s_equation_no_double_operators.strip()
    # split by equal =>  "-33=3x+5y-22z" -> ["-33","3x+5y-22z"]
    a_s_part = s_equation_no_double_operators.split("=")
    n_result_number_index = (0 if(len(a_s_part[0]) < len(a_s_part[1])) else 1)
    n_result_number = float(a_s_part[n_result_number_index])
    a_s_part.pop(n_result_number_index)
    s_equation_coefficient_part = "".join(a_s_part)

    # 12=3x+5y+2z => ["12", "=", "3x", "+", "5y","+", "2z"]
    a_o_coefficient = [] # for example ['x','y','z']
    s_factor = ""
    s_operator = ""
    if((s_equation_coefficient_part[0] != '-' and s_equation_coefficient_part[0] != '+')):
        s_equation_coefficient_part = '+' + s_equation_coefficient_part

    a_s_summand = []
    s_summand = ""
    for n_i in range(0,len(s_equation_coefficient_part)): 
        s = s_equation_coefficient_part[n_i]
        if(
            (s == "+" or s == "-")
        ): 
            if n_i > 0: 
                a_s_summand.append(s_summand)
                s_summand = ""
                
        s_summand = s_summand + s
        
        if(n_i == len(s_equation_coefficient_part)-1):
            a_s_summand.append(s_summand)
    
    a_o_coefficient = []
    for s_summand in a_s_summand: 
        s_variable_char = ""
        s_factor = ""
        for s in s_summand: 
            if(s.isalpha()):
                s_variable_char = s
                break
            s_factor = s_factor + s
        if(s_factor.strip() == '-' or s_factor.strip() == '+'):
            s_factor = s_factor + "1"
        a_o_coefficient.append(
            O_coefficient(
                s_variable_char, 
                n_factor=eval(s_factor)
            )
        )

    o_polynom = O_polynom(
            n_result_number, 
            a_o_coefficient, 
            s_name
        )
    return o_polynom

class O_coefficient: 
    def __init__(
        self,
        s_variable_char, 
        n_factor
        ):
        self.s_variable_char = s_variable_char
        self.n_factor = n_factor

a_o_polynom = []
a_s_roman_numeral = [
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "VIIII", "X"
]

def f_solve_system_of_equations(
    a_s_equations
):
    # # example 
    # a_s_equations = [
    #   "12=3x+5y+2z", 
    #   "2=2x+1y+-10z", 
    #   "-33=3x+5y-22z", 
    # ]
    n_index = 0
    for s_equation in a_s_equations: 
    
        s_name = a_s_roman_numeral[n_index]
        o_polynom = f_o_polynom_by_equation_string(s_equation, s_name)
        o_polynom = o_polynom.f_o_simplified() # example => 5 = 3x+2y+2x+5z-3 -> 2 = 5x+2y+5z
    

        a_o_polynom.append(
            o_polynom
        )
        n_index+=1

    n_number_of_equations = len(a_s_equations)
    for o_polynom in a_o_polynom:
        if(n_number_of_equations < len(o_polynom.a_o_coefficient)):
            print("not enough equations to solve the variables")
            exit()


    # depending on the degree/(number of different varibales) of the polynom
    o_polynom_first = a_o_polynom[0]
    a_a_o_polynom_result = []
    a_o_polynom_result = f_a_o_eliminate_variable(a_o_polynom)
    a_a_o_polynom_result.append(a_o_polynom_result)
    while(len(a_o_polynom_result) > 1):
        a_o_polynom_result = f_a_o_eliminate_variable(a_o_polynom_result)
        a_a_o_polynom_result.append(a_o_polynom_result)
    
    print(a_o_polynom_result[0].f_s_equation_solved_for_one_coefficient())
    exit()


    return False


def f_a_o_eliminate_variable(
    a_o_polynom
):
    o_polynom_first = a_o_polynom[0]
    a_o_polynom_result = []
    for n_dimension in range(1, len(o_polynom_first.a_o_coefficient)):
        o_polynom_second = a_o_polynom[n_dimension]
        o_polynom_result = f_o_polynom_eliminate_variable(
            o_polynom_first=o_polynom_first, 
            o_polynom_second=o_polynom_second, 
            s_variable_char_to_eliminate=o_polynom_first.a_o_coefficient[0].s_variable_char
        )
        o_polynom_result = o_polynom_result.f_o_simplified()
        a_o_polynom_result.append(
            o_polynom_result
        )

        # print(o_polynom_result.s_name) 
        # print(o_polynom_result)
    
    return a_o_polynom_result
def f_o_polynom_eliminate_variable(
    o_polynom_first, 
    o_polynom_second, 
    s_variable_char_to_eliminate
):  

    print("")
    print(f"--eliminate variable '{s_variable_char_to_eliminate}' --")
    print("")

    o_coefficient_first = [o_coefficient for o_coefficient in o_polynom_first.a_o_coefficient if o_coefficient.s_variable_char.lower() == s_variable_char_to_eliminate.lower()][0]
    o_coefficient_second = [o_coefficient for o_coefficient in o_polynom_second.a_o_coefficient if o_coefficient.s_variable_char.lower() == s_variable_char_to_eliminate][0]
    
    # s_factor_operation_suffix = f"*({o_coefficient_first.n_factor}/{o_coefficient_second.n_factor})"
    # print(s_factor_operation_suffix)
    # gemeinsames vielfaches !
    s_factor_operation_suffix_first = "{:g}".format(float(o_coefficient_second.n_factor)) # -2.0 -> -2, 4.400 -> 4.4
    s_factor_operation_suffix_second = "{:g}".format(float(o_coefficient_first.n_factor))
    

    o_polynom_for_operation_first = o_polynom_second * s_factor_operation_suffix_second
    o_polynom_for_operation_second = o_polynom_first * s_factor_operation_suffix_first


    
    # lets say first    coefficient => 4x
    # lets say second   coefficient => -1x
    # calculation must then be      => 4x + -1x*(4/1)

    o_coefficient_first = [
        o_coefficient for o_coefficient in o_polynom_for_operation_first.a_o_coefficient
        if o_coefficient.s_variable_char.lower() == s_variable_char_to_eliminate
        ][0]
    o_coefficient_second = [
        o_coefficient for o_coefficient in o_polynom_for_operation_second.a_o_coefficient
        if o_coefficient.s_variable_char.lower() == s_variable_char_to_eliminate
        ][0]
    if(
        (
            o_coefficient_first.n_factor > 0 # +
            and 
            o_coefficient_second.n_factor > 0 # +
        )
        or
        (
            o_coefficient_first.n_factor < 0 # -
            and 
            o_coefficient_second.n_factor < 0 # -
        )
    ): 
        s_operator = '-'
    else:
        s_operator = '+'
    
    o_polynom_operation_result = eval("o_polynom_for_operation_first" + s_operator + "o_polynom_for_operation_second")
    
    a_o_polynom.append(o_polynom_for_operation_first)
    a_o_polynom.append(o_polynom_for_operation_second)
    a_o_polynom.append(o_polynom_operation_result)
    
    print(o_polynom_for_operation_first)
    print(o_polynom_for_operation_first.s_name)
    print(o_polynom_for_operation_second)
    print(o_polynom_for_operation_second.s_name)
    print(o_polynom_operation_result)
    print(o_polynom_operation_result.s_name)
    
    return o_polynom_operation_result


def f_test_equation_solving():        
    # example 
    a_s_equations_4x4 = [
        "1=2x-y+3z+2b", 
        "0=3x+y-2z+b", 
        "3=1x+y+z-b", 
        "7=1x+y+z+12b", 
    ]

    a_s_equations_3x3 = [
        "1=2x-y+3z", 
        "0=3x+y-2z", 
        "3=1x+y+z", 
    ]
        
    a_s_equations_2x2 = [
        # x = 2 
        # y = 3
        "1=2x-y", 
        "9=3x+y", 
    ]
        
    # f_solve_system_of_equations(a_s_equations_2x2)
    f_solve_system_of_equations(a_s_equations_3x3)
    # f_solve_system_of_equations(a_s_equations_4x4)

def f_test_solving_of_one_coefficient():
    s_polynom = "12 = 6x + 12x + 0y + 0y + 12 + 6x"
    o_polynom = f_o_polynom_by_equation_string(s_polynom)
    print(o_polynom)
    print(o_polynom.f_s_equation_solved_for_one_coefficient())

def f_test_polynom():
    s_polynom = "12 = 2 + 3x + 6y - 3 + 2 + 2x +2y + 12"
    # s_polynom = "12 = 2x-3y+3"

    s_separator = "+"
    o_polynom = f_o_polynom_by_equation_string(s_polynom)
    o_polynom_simplified = o_polynom.f_o_simplified()
    print(o_polynom)
    print(o_polynom_simplified)

def f_test_substitution():
    s_polynom = "12 = 3x + 5y + 2z"
    s_polynom_expected = "20 = 3x + 5y" # z = 4 
    o_polynom = f_o_polynom_by_equation_string(s_polynom, "I")
    o_polynom_substituted = o_polynom.f_o_substite_coefficient(
        "z", 
        4
    )

    print(o_polynom.s_name)
    print(o_polynom)
    print("---")
    print(o_polynom_substituted.s_name)
    print(o_polynom_substituted)
    print("---")


# f_test_solving_of_one_coefficient()

# f_test_equation_solving()

f_test_substitution()