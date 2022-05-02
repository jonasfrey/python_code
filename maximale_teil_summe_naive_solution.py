array = [1,-2,4,102,-22,33]

array_len = len(array)
start_index = 0
sums = []
for i in range(0, (array_len-1)):
    start_index = i
    end_index = (array_len-1)

    sum = {"indices":[], "value": 0}
    
    while start_index <= end_index:
        sum["indices"].append(start_index)
        sum["value"] += array[start_index]
        start_index+=1

    sums.append(sum)

biggest_sum = {"value":0}

for i in range(0, len(sums)): 
    if(sums[i]["value"] > biggest_sum["value"]): 
        biggest_sum = sums[i]
    # for(j in range())


print(biggest_sum)