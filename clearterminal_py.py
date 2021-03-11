import os
import time
import emoji
os.system('cls' if os.name == 'nt' else 'clear')
i = 0
width = 100
emojistr = "😐"

asciistr = "@"
strstr = emojistr
liststr = [" "] * width
while i < 1000:
    time.sleep(0.1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(("".join(liststr)))
    i+= 1
    liststr = [" "] * width
    liststr[(i % width)] = strstr