import os
import time
import emoji
os.system('cls' if os.name == 'nt' else 'clear')
i = 0
width = 100
<<<<<<< HEAD
emojistr = "😐"

=======
emojistr = "🐸"
>>>>>>> 128542107be4a702a61124398fdc70b1f32aa3f9
asciistr = "@"
strstr = emojistr
liststr = [" "] * width
while i < 1000:
    time.sleep(0.01)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(("".join(liststr)))
    i+= 1
    liststr = [" "] * width
    liststr[(i % width)] = strstr