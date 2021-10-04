# primes

import sys

amountofprimes = 20

if(len(sys.argv)>1):
    amountofprimes = int(sys.argv[1])

primes = [2]
i_current = 3

while len(primes) < amountofprimes: 
    result_was_int = False
    for primenum in primes: 
        if(primenum >= i_current):
            break
        if((float(i_current)/primenum).is_integer()):
            result_was_int = True

    if result_was_int == False: 
        primes.append(i_current)
        i_current+= 1

    i_current+=1

print(primes)