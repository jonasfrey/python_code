class Eis: 
    def __init__(self):
        self.array_from_other_class = ["jetz no 'läär'"]


class Zwöi: 
    def __init__(self):
        self.mis_array = ["ju", "di", "hui"]


z = Zwöi()

z.mis_array = ["jetz", "ischs", "nöi"]


e = Eis()
e.array_from_other_class = z.mis_array


print(e.array_from_other_class) # ['jetz', 'ischs', 'nöi']

z.mis_array[0]= "wider"

print(e.array_from_other_class) # ['wider', 'ischs', 'nöi']