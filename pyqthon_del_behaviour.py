class Obs_del():

    def __del__(self):
        print("yes, now __del__ was called !")
        del self

od_ref_one = Obs_del()
od_ref_two = od_ref_one
od_ref_three = od_ref_one

# del the first reference of Obs_del
del od_ref_one
print('i ran "del od_ref_one", was __del__ called ?') # nope you have to delete every other reference

# del the second reference of Obs_del
del od_ref_two
print('i ran "del od_ref_two", was __del__ called ?') # nope you have to delete every other reference

# del the third reference of Obs_del
del od_ref_three
print('i ran "del od_ref_three", was __del__ called ?') # nope you have to delete every other reference

print('===== this part of script finished =====') 




class Obs_del():

    def __del__(self):
        print("yes, now __del__ was called !")

obs_del_obj = Obs_del()
obs_del_obj2 = Obs_del()
obs_del_obj3 = Obs_del()

print('i dont call del ')
print('but __del__, in the end it, will be called anyway')
print('because of garbage collector ?')
print('last statement in code...')