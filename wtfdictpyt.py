dict1 = {
    'listyes' : [
        1,2,3,4
    ]
}
dict2 = {}
dict2['hmm'] = dict1['listyes']


dict1['listyes'].append(99)

print(dict1)
print(dict2)

dict1 = {
    'listyes' : [
        1,2,3,4
    ]
}
dict2 = {}
dict2['hmm'] = dict1['listyes']

dict1['listyes'] = [1,2,3,4,99]

print(dict1)
print(dict2)

dict1 = {
    'listyes' : [
        1,2,3,4
    ]
}
dict2 = {}
dict2['hmm'] = dict1['listyes'].copy()

dict1['listyes'].append(99)

print(dict1)
print(dict2)

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
