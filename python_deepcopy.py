import copy
import json

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


# another way if you dont need functions
dict1 = {
    'nested_dict' : {
        'prop': True
    },
    'im_a_lambda': lambda x : x*2
}
dict2 = json.loads(json.dumps(dict1))
dict1['nested_dict']['prop'] = False
print(dict2)
print(type(dict2))