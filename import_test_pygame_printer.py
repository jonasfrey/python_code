from pygame_printer import Pygame_Printer


class ClassGen: 
    def __init__(self):
        self.pgptr = Pygame_Printer()


        for value in range(0, 1000): 
            print("doing other stuff first")

        for value in range(0, 1000):
            self.pgptr.clear()
            self.pgptr.print("asdf")


asdf = ClassGen()