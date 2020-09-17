import sys, time

print("start")

ch = sys.stdin.read(1)
print(ch)

input("press enter to exit")

def loop():
    ch = sys.stdin.read(1)
    print(ch)
    time.sleep(1)
    loop()

loop()

# s1 = input()
# s2 = sys.stdin.read(1)
# print(s1)
# print(s2)