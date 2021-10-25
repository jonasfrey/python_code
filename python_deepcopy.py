import copy

dict1 = {
    'nested_dict' : {
        'prop': True
    }
}
dict2 = dict1.copy()
dict1['nested_dict']['prop'] = False

print(dict2)
# $ {'nested_dict': {'prop': False}}
# wtf i though i copied dict1 !?!?



dict1 = {
    'nested_dict' : {
        'prop': True
    }
}
dict2 = copy.deepcopy(dict1)

dict1['nested_dict']['prop'] = False
print(dict2)
# $ {'nested_dict': {'prop': True}}
# ohhhh , much better
