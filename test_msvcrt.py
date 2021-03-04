import msvcrt
while True:
    if msvcrt.kbhit():
        key_stroke = msvcrt.getch()
        print(key_stroke)   # will print which key is pressed
        