

class O_polynom:
    def __init__(
        self, 
        n_result_number, 
        a_o_coefficient
    ):
        self.n_result_number = n_result_number
        self.a_o_coefficient = a_o_coefficient
    def f_s_equation(self): 
        s_equation = f"{self.n_result_number}="
        for o in self.a_o_coefficient:
            if(o.n_factor>=0):
                s_equation+="+"
            s_equation+=str(o.n_factor)
            s_equation+=str(o.s_variable_char)
        return s_equation
    def __str__(self):
        # print(self)
        return self.f_s_equation()

class O_coefficient: 
    def __init__(
        self,
        s_variable_char, 
        n_factor
        ):
        self.s_variable_char = s_variable_char
        self.n_factor = n_factor

a_o_polynom = []
def f_solve_system_of_equations(
    a_s_equations
):

    # # example 
    # a_s_equations = [
    #   "12=3x+5y+2z", 
    #   "2=2x+1y+-10z", 
    #   "-33=3x+5y-22z", 
    # ]
    for s_equation in a_s_equations: 
        s_equation_no_double_operators = s_equation.replace("+-", "-")
        s_equation_no_double_operators = s_equation_no_double_operators.replace("-+", "-")
        s_equation_no_double_operators = s_equation_no_double_operators.replace("--", "+")
        s_equation_no_double_operators = s_equation_no_double_operators.replace("++", "+")
        s_equation_no_double_operators = s_equation_no_double_operators.replace("*", "")
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

        for n_i in range(0,len(s_equation_coefficient_part)): 
            s = s_equation_coefficient_part[n_i]
            if(
                s == "+" or s == "-"
            ): 
                s_operator = s
            if(
                s.isalpha()
            ):
                if(s_factor.strip() == ""):
                    s_factor = "1"
                a_o_coefficient.append(
                    O_coefficient(
                        s, 
                        eval(s_operator + s_factor)
                    )
                )
                s_factor = ""
            if(
                s != "+" and s != "-" and s.isalpha() == False
            ):
                s_factor+=s

            

        o_polynom = O_polynom(
                n_result_number, 
                a_o_coefficient
            )
        
        a_o_polynom.append(
            o_polynom
        )

    # exit()
    o_polynom_first = a_o_polynom[0]
    o_coefficient_first = o_polynom_first.a_o_coefficient[0]
    o_polynom_second = a_o_polynom[1]

    s_variable_char_to_eliminate = o_coefficient_first.s_variable_char
    o_polynom_operation_result_iv = f_o_polynom_eliminate_variable(
        o_polynom_first=o_polynom_first, 
        s_polynom_first_roman_numeral="I", 
        o_polynom_second=o_polynom_second, 
        s_polynom_second_roman_numeral="II",
        s_variable_char_to_eliminate=s_variable_char_to_eliminate
    )


    o_polynom_first = a_o_polynom[0]
    o_coefficient_first = o_polynom_first.a_o_coefficient[0]
    o_polynom_second = a_o_polynom[2]

    s_variable_char_to_eliminate = o_coefficient_first.s_variable_char
    o_polynom_operation_result_v = f_o_polynom_eliminate_variable(
        o_polynom_first=o_polynom_first, 
        s_polynom_first_roman_numeral="I", 
        o_polynom_second=o_polynom_second, 
        s_polynom_second_roman_numeral="III",
        s_variable_char_to_eliminate=s_variable_char_to_eliminate
    )

    # exit()
    s_variable_char_to_eliminate_second = [o_coefficient for o_coefficient in o_polynom_operation_result_iv.a_o_coefficient if (o_coefficient.s_variable_char.lower() == s_variable_char_to_eliminate) == False][0].s_variable_char
    o_polynom_operation_result_vi = f_o_polynom_eliminate_variable(
        o_polynom_first=o_polynom_operation_result_iv, 
        s_polynom_first_roman_numeral="IV", 
        o_polynom_second=o_polynom_operation_result_v, 
        s_polynom_second_roman_numeral="V",
        s_variable_char_to_eliminate=s_variable_char_to_eliminate_second
    )

    o_coefficient_third = [
        o for o in o_polynom_operation_result_vi.a_o_coefficient
        if (
            o.s_variable_char != s_variable_char_to_eliminate
            and
            o.s_variable_char != s_variable_char_to_eliminate_second
        )][0]
    s_variable_char_to_eliminate_third = o_coefficient_third.s_variable_char

    print(f"{s_variable_char_to_eliminate_third} = {o_polynom_operation_result_vi.n_result_number/o_coefficient_third.n_factor}")

    # eliminate second coefficient


    return False


def f_o_polynom_eliminate_variable(
    o_polynom_first, 
    s_polynom_first_roman_numeral, 
    o_polynom_second, 
    s_polynom_second_roman_numeral,
    s_variable_char_to_eliminate
):  
    print("")
    print("--eliminate variable--")
    print("")

    o_coefficient_first = [o_coefficient for o_coefficient in o_polynom_first.a_o_coefficient if o_coefficient.s_variable_char.lower() == s_variable_char_to_eliminate.lower()][0]
    o_coefficient_second = [o_coefficient for o_coefficient in o_polynom_second.a_o_coefficient if o_coefficient.s_variable_char.lower() == s_variable_char_to_eliminate][0]
    
    s_factor_operation_suffix = f"*({o_coefficient_first.n_factor}/{o_coefficient_second.n_factor})"
    print(s_factor_operation_suffix)
    a_o_coefficient_for_o_polynom_for_operation = []
    for o_coefficient in o_polynom_second.a_o_coefficient: 
        a_o_coefficient_for_o_polynom_for_operation.append(
            O_coefficient(
                o_coefficient.s_variable_char, 
                eval(str(o_coefficient.n_factor)+s_factor_operation_suffix)
            )
        )  
    o_polynom_for_operation = O_polynom(
        eval(str(o_polynom_second.n_result_number)+s_factor_operation_suffix), 
        a_o_coefficient_for_o_polynom_for_operation
    )

    # lets say first    coefficient => 4x
    # lets say second   coefficient => -1x
    # calculation must then be      => 4x + -1x*(4/1)

    o_coefficient_polynom_for_operation = [o_coefficient for o_coefficient in o_polynom_for_operation.a_o_coefficient if o_coefficient.s_variable_char.lower() == s_variable_char_to_eliminate][0]
    if(
        (
            o_coefficient_first.n_factor > 0 # +
            and 
            o_coefficient_polynom_for_operation.n_factor > 0 # +
        )
        or
        (
            o_coefficient_first.n_factor < 0 # -
            and 
            o_coefficient_polynom_for_operation.n_factor < 0 # -
        )
    ): 
        s_operator = '-'
    else:
        s_operator = '+'

    a_o_coefficient_for_o_polynom_operation_result = []

    for o_coefficient in o_polynom_first.a_o_coefficient: 
        o_coefficient_for_operation = [
            o for o in o_polynom_for_operation.a_o_coefficient
            if o.s_variable_char.lower() == o_coefficient.s_variable_char.lower()
            ][0]

        a_o_coefficient_for_o_polynom_operation_result.append(    
            O_coefficient(
                o_coefficient.s_variable_char, 
                eval(str(o_coefficient.n_factor)+s_operator+str(o_coefficient_for_operation.n_factor))
            )
        )

    o_polynom_operation_result = O_polynom(
        eval(str(o_polynom_first.n_result_number)+s_operator+str(o_polynom_for_operation.n_result_number)),
        a_o_coefficient_for_o_polynom_operation_result
    )
    

    print(s_polynom_first_roman_numeral)
    print(o_polynom_first)
    print("")

    print(s_polynom_second_roman_numeral)
    print(o_polynom_second)
    print("")

    print(f"{s_polynom_second_roman_numeral}{s_factor_operation_suffix}, ({s_polynom_second_roman_numeral}m)")
    print(o_polynom_for_operation)
    print("")

    print(f"{s_polynom_first_roman_numeral}{s_operator}({s_polynom_second_roman_numeral}m)")
    print(o_polynom_operation_result)
    print("")
    
    return o_polynom_operation_result

# example 
a_s_equations = [
    "1=2x-y+3z", 
    "0=3x+y-2z", 
    "3=1x+y+z", 
]
    
f_solve_system_of_equations(a_s_equations)