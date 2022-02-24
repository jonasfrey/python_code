# print('give me some nums between -100 and 100')

# n_input_is_in_range = True
# n_sum = 0
# while(n_input_is_in_range):

#     n_input = int(input())
#     n_input_is_in_range = (n_input > -100 and n_input < 100)

#     if(n_input_is_in_range):
#         n_sum = n_sum + n_input

# print(
#     "sum of numbers is" + str(n_sum)
# )


start = 0
inputs = int(input())

while inputs >= -100 and inputs <= 100:
    inputs = int(input("")) # you are overwriting the inputs value here


if inputs == -101:
    calculation = start+inputs # so the inputs variable holds the last value which was retrieved by input() function
    print("The Sum:", calculation)