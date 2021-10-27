arr = [0,1,2,3,4,5,6,7,8]

index_start = 2 
index_end = 4
for key in range(index_start, index_end):
    print(key)
    arr.pop(key)


arr = [0,1,2,3,4,5,6,7,8]
# lets say you want to remove at index 2, 4 and 7
arr.pop(2) # works, but now index 4 is at 3 since one item is missing
arr.pop(4) # wont work
# arr.pop(7) # wont work index 7 is even out of range now

print(arr)

def pop_at_indices(arr, indices):
    sorted_indices = indices.copy()
    sorted_indices.sort()
    pops_done = 0
    for key in sorted_indices:
        pop_at_index = key - pops_done
        arr.pop(pop_at_index)
        pops_done +=1

arr = [0,1,2,3,4,5,6,7,8]

pop_at_indices(arr, [4,2,7])

print(arr)