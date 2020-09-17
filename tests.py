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


class Limb: 
    def __init__(self, x,y):
        self.x = x
        self.y = y
limb = Limb(0,0)

b = tuple(limb)


limb.x = 22

print(limb.x)
print(b.x)