# stack and queue 

# LIFO Last In First Out
class O_Stack:

    def __init__(self, a_items):
        self.a_items = a_items

    def f_push(self, var): 
        self.a_items.append(var)
    
    def f_pop(self): 
        item = self.a_items[-1]
        self.a_items = self.a_items[:-1]
    
    def f_top(self):
        return self.a_items[-1]



# FIFO First In First Out
class O_Queue:

    def __init__(self, a_items):
        self.a_items = a_items
        
    def f_en_queue(self, var): 
        self.a_items.append(var)

    def f_de_queue(self, ):
        item = self.a_items[0]
        self.a_items = self.a_items[1:]

    def f_get_first():
        return self.a_items[0]


# if __name__ == "__main__":
#     o_stack = O_stack()