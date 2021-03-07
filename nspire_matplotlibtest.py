from math import * 
from random import * 
import ti_plotlib as plt 

totals = [0] * 11
trials = int(input("# of trials ? "))

for i in range(trials):
    die_1 = randint(1, 6)
    die_2 = randint(1, 6)
    sum = die_1 + die_2 
    totals[sum-2] = totals[sum-2]+1

plt.window(-5, 15, -10, 1000)
plt.axes("on")

plt.scatter(sums, totals, "o")