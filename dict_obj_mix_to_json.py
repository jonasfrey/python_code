import json 
import jsonpickle

class   My_obj():
    def __init__(self) -> None:
        pass

dict_obj_mix = {
  'dict_prop': True, 
  'obj_instance': My_obj()
}
# print(json.dumps(dict_obj_mix))
# not working 
print(str(dict_obj_mix))
# working !
print(jsonpickle.encode(dict_obj_mix))
# also working but needs a library


# import jsonpickle

# class   My_obj():
#     def __init__(self) -> None:
#         pass
# dict_obj_mix = {
#   'dict_prop': True, 
#   'obj_instance': My_obj()
# }
# print(jsonpickle.encode(dict_obj_mix))
import json
class   My_obj():
    def __init__(self, object=None) -> None:
        self.nested_object = object
        self.simple_str_prop = 'aBcDeF'
        pass
    def __repr__(self):
        return self.toJSON()
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

dict_obj_mix = {
  'dict_prop': True, 
  'obj_instance': My_obj(My_obj()), 
  'nested_dict': {
    'dict_prop': True, 
    'obj_instance': My_obj(My_obj()), 
    }
}
print(str(dict_obj_mix))
