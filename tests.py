strin = "asdf"
strin+="23234"

arr = ["val1", "val2_car", "val3"]

for key,value in enumerate(arr):
    print(value)
    print(key)


arr_one = ["val1", "du", "da"]
# a reference, which is synchronized with the arr_one
referenced_array = arr_one

# a real separated copy duplicate of the arr_one
copied_array = arr_one[:]

referenced_array[2] = "trololol"

copied_array[2] = "yes im different"

def deep_slice_copy(array):
    new_array = []
    for val in array:
        if isinstance(val, list):
            new_array.append(deep_slice_copy(val))
        else:
            new_array.append(val)
    return new_array


deep_arr_original = [["deep 0 0", "deep 0 1"], ["deep 1 0", "deep 1 1"]]
deep_arr_copy_questionmark = deep_arr_original[:]

deep_arr_real_copy = [deep_arr_original[0][:], deep_arr_original[1][:]]


deep_arr_copy_with_func = deep_slice_copy(deep_arr_original)

deep_arr_copy_questionmark[0][0] = "changed 0 0"
deep_arr_real_copy[0][0] = "this should be independent 0 0"
deep_arr_copy_with_func[0][0] = "nice this is also independent now 0 0"




print(deep_arr_original)
print(deep_arr_copy_questionmark)
print(deep_arr_real_copy)
print(deep_arr_copy_with_func)

# print(arr_one)
# print(referenced_array)
# print(copied_array)


# print(strin)


a = [1]
b = [a[0]]

b = [3]


print(a)
print(b)




class Object: 
    def __init__(self,integer,string,flt):
        self.integer = integer
        self.string = string
        self.flt = float 
    def __eq__(self, other) : 
        return self.__dict__ == other.__dict__

number_array = [-1,-2,-3,1,2,3,45,6,6,5,4,3,11,22,33]
object_array = [Object(1,"test", 1.1), Object(1,"test", 1.1), Object(2,"test", 1.1), Object(3,"test3", 1.1), Object(4,"test4", 4.1)]


has_duplicates = len(number_array) != len(set(number_array))
object_array_mapped_string = list(map(lambda v: v.string, object_array))
# set() removes duplicates from array, a duplicate is only one if it is the exact same instance of an object
# not if only the values of each property matches
object_array_mapped_string_has_duplicates = len(object_array_mapped_string) != len(set(object_array_mapped_string))

objects_are_same = object_array[0].__eq__(object_array[1])

less_than_zero = list(filter(lambda val: val < 0, number_array))

print(has_duplicates)
print(objects_are_same)
print(less_than_zero)
print(object_array_mapped_string_has_duplicates)

# Output: [-5, -4, -3, -2, -1]


def func_name_called_by_string():
    print("i was called")


locals()["func_name_called_by_string"]()




# # RuntimeError: maximum recursion depth exceeded while calling a Python object, python doesnt like recursive functions... so just use a while loop 

# # bad
# def repeat():
#     # do stuff... 
#     # do stuff... 
#     # maybe time.sleep(ms*10**-3)
#     # recursive call
#     repeat()

# # good
# def repeat():
#     while True
#         # do stuff... 
#         # do stuff... 
#         # maybe time.sleep(ms*10**-3)
#         # while loop will be executed again by itself



# obj = {"test": "asdf"}

# print(obj.test)



asdf = "asdf"
b = asdf 

asdf = "lol"

print(asdf)
print(b)

class Test:
    def __init__(self):
        self.prop = "test"

asdf = Test()
b = asdf

asdf.prop = "lol=?"

print(asdf.prop)
print(b.prop)

asdf = Test()
b = Test()

b.prop = asdf.prop

asdf.prop = "lol=?"

print(asdf.prop)
print(b.prop)


# Python program to illustrate destructor 
class Can_i_self_destroy_me: 
  
    # Initializing 
    def __init__(self): 
        print('Employee created.') 
  
    def self_destroy(self):
        self.__del__()
    # Deleting (Calling destructor) 
    def __del__(self): 
        del self
        print('Destructor called, Employee deleted.') 
  
can_i_self_destroy_me = Can_i_self_destroy_me() 
del can_i_self_destroy_me 

can_i_self_destroy_me = Can_i_self_destroy_me() 
can_i_self_destroy_me.self_destroy()
can_i_self_destroy_me.self_destroy()
can_i_self_destroy_me.self_destroy()
can_i_self_destroy_me.self_destroy()

print(can_i_self_destroy_me)
print("can_i_self_destroy_me still here ?=e")
print(can_i_self_destroy_me)

can_i_self_destroy_me.self_destroy()  

can_i_self_destroy_me.prop = "test321"
print(can_i_self_destroy_me.prop)

can_i_self_destroy_me_arr = []

can_i_self_destroy_me_arr.append(can_i_self_destroy_me)
import gc
gc.collect()
print(can_i_self_destroy_me_arr)
del can_i_self_destroy_me

print(can_i_self_destroy_me_arr[0])


print("####")

# Python program to illustrate destructor 
class Parent_class: 
  
    # Initializing 
    def __init__(self,name):
        self.name = name 
        self.child_class = Child_class("childname")

# Python program to illustrate destructor 
class Child_class: 
  
    # Initializing 
    def __init__(self,name):
        self.name = name

    def find_parents(self):
        return gc.get_referrers(self)

pc = Parent_class("Father Baba")

print("parent class")
print(pc)


new_ref = pc.child_class

print(pc.child_class.find_parents())


print("###")

class Instance_count:
    _counter = 0
    _counter_name = []

    
    def __init__(self, name):
        self.name = name
        self.__class__._counter += 1
        self.__class__._counter_name.append(name)
        _instance_counter_with_name_string = "_instance_counter_with_name_"+name
        
        if(hasattr(self.__class__, _instance_counter_with_name_string) == False):
            _instance_counter_with_name_value = 0
        else: 
            _instance_counter_with_name_value = getattr(self.__class__, _instance_counter_with_name_string)
        setattr(self.__class__,_instance_counter_with_name_string , _instance_counter_with_name_value+1)
        
        self.id = self.__class__._counter

    def get_instance_count(self): 
        print("i was instanciated so many times")
        print(self.__class__._counter)

        #print("i with the name " + self.name + "  was instanciated so many times")
        #print(filter(lambda val: val.name == self.name, self.__class__._counter_name))

        print("instances with name" + self.name)
        print(getattr(self.__class__, "_instance_counter_with_name_" + self.name))







i1 = Instance_count("u")
i2 = Instance_count("u")
i3 = Instance_count("a")
i4 = Instance_count("a")
i5 = Instance_count("a")
i6 = Instance_count("i")
i7 = Instance_count("e")

# del i3

# print(i1.get_instance_count())
# print(i3)

print("###")

class Demo():
    def __init__(self, name):
        self.name = name

var1 = Demo("var1")
var2 = Demo("var2")

vars_in_arr = [var1, var2]

print(vars_in_arr)

var1.name = "var1_changed"

print(vars_in_arr[0].name)

print(gc.get_referrers(var1))

print(vars_in_arr[0].name)

