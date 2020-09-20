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


