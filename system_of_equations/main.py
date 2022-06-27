from ossaudiodev import SNDCTL_TMR_CONTINUE
from re import I
from stat import S_ENFMT


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

        # 12=3x+5y+2z => ["12", "=", "3x", "+", "5y","+", "2z"]
        a_s_part = []
        a_s_variable_char = [] # for example ['x','y','z']
        s_tmp = ""
        for n_i in s_equation_no_double_operators: 
            s = s_equation_no_double_operators[n_i]
            if(
                s == "=" 
                or
                s == "+"
                or 
                s == "-"
                or 
                n_i == len(s_equation_no_double_operators)
            ): 
                if(n_i == len(s_equation_no_double_operators)): 
                    s_tmp+=s

                a_s_part.append(s_tmp)
                for n_i in range(0, len(s_tmp)):
                    if(s_tmp[n_i].isnumeric() == False):
                        a_s_variable_char.append(s_tmp[n_i])

                a_s_part.append(s)
                s_tmp = ""
                continue
            
            s_tmp+=s


        print(a_s_part)
        print(a_s_variable_char)

    return False


# example 
a_s_equations = [
    "12=3x+5y+2z", 
    "2=2x+1y+-10z", 
    "-33=3x+5y-22z", 
]
    
f_solve_system_of_equations(a_s_equations)