import queue


q =  queue.Queue()

numbers = [1,2,3,5]

for num in numbers: 
    q.put(num)


print(q.get())
print(q.get())
print(q.get())



q2 =  queue.Queue()

miscarr = [1, "asd", {"dict":1}]

for o in miscarr: 
    q2.put(o)


print(q2.get())
print(q2.get())
print(q2.get())
