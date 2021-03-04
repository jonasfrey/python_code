import time

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



l = Looper()
l.start()
#the script wont get out of the while self.running loop 
# we need multithreading to achieve this
time.sleep(1)
l.end()
print("t")