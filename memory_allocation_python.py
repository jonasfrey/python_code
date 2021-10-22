
print("in python every variable is an object")
var_x = 10 
print("var_x = 10")
print("print(var_x)")
print(">>>"+str(var_x))

print("if one creates a new variable now called var_y = var_x")

print("this will be the same object as var_x")
print("var_y = var_x")
var_y = var_x
print("print(var_x)")
print(">>>"+str(var_x))

print("we can check this by calling id(variable) function")

print('var_x_and_var_y_reference_to_same_object = id(var_x) == id(var_y)')
var_x_and_var_y_reference_to_same_object = id(var_x) == id(var_y)
print('print(var_x_and_var_y_reference_to_same_object)')
print(">>>"+str(var_x_and_var_y_reference_to_same_object))




