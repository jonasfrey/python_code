import time
import threading

class Looper():
    def __init__(self):
        self.running = False    
        

    def start(self): 
        self.running = True
        

        while self.running:
            print(self.running)

    def end(self):
        self.running = False
        

        print(self.running)

# l = looper()
# l.start()
# #the script wont get out of the while self.running loop 
# # we need multithreading to achieve this
# time.sleep(1)
# l.end()
# print("t")

l = Looper()

def background():
    l.start()

def foreground():
    time.sleep(1)
    l.end()
    print("now it has finished")
    # What you want to run in the foreground

b = threading.Thread(name='background', target=background)
f = threading.Thread(name='foreground', target=foreground)

b.start()
f.start()