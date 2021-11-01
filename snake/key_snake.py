#!/usr/bin/python3
import sys, termios, tty, os, time




def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
 
button_delay = 0.2
 
while True:
    char = getch()
 
    if (char == "p"):
        print("Stop!")
        exit(0)
 
    if (char == "a"):
        print("Left pressed")
        time.sleep(button_delay)
 
    elif (char == "d"):
        print("Right pressed")
        time.sleep(button_delay)
 
    elif (char == "w"):
        print("Up pressed")
        time.sleep(button_delay)
 
    elif (char == "s"):
        print("Down pressed")
        time.sleep(button_delay)
 
    elif (char == "1"):
        print("Number 1 pressed")
        time.sleep(button_delay)


# used for deep copy array, because like in js , in python assigning an array to a new variable makes a reference not a copy!!!
def deep_slice_copy(array):
    new_array = []
    for val in array:
        if isinstance(val, list):
            new_array.append(deep_slice_copy(val))
        else:
            new_array.append(val)
    return new_array

class Canvas:
    def __init__(self):
        self.width = 33
        self.height = 33
        self.output = ""
        self.white_pixel = " "
        self.black_pixel = "."
        self.pixel_matrix = []
        self.clear_pixel_matrix = []
        self.counter = 0
        for y in range(0, self.height):
            y_array = []
            for x in range(0, self.width):
                y_array.append(False)
            self.clear_pixel_matrix.append(y_array)
        
        self.pixel_matrix = deep_slice_copy(self.clear_pixel_matrix)

        #print(self.pixel_matrix)

    def clear(self):
        #print("clearing")
        self.pixel_matrix = deep_slice_copy(self.clear_pixel_matrix)
        

        for x in range(0, self.height):
            print("\n")

    def addPixel(self, x,y):
        if x > self.width | y > self.height:
            print("canvas is not big enought to add a pixel at this position")
        else:
            self.pixel_matrix[y][x] = True


    def draw(self):
        self.output = ""
        for value in self.pixel_matrix:
            for value in value:
                if value == True:
                    self.output += self.black_pixel
                else:
                    self.output += self.white_pixel
            self.output +="\n"

        print(self.output)


class Snake:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.pos_x_direction = "t + 1"
        self.pos_y_direction = "t * 0"

    def set_x_direction(self, pos_x_direction):
        self.pos_x_direction = pos_x_direction
    def set_y_direction(self, pos_y_direction):
        self.pos_y_direction = pos_y_direction
        



snake = Snake()

canvas = Canvas()

ts_now = time.time()
ts_then = time.time()
ts_delta_limit = 100

snake.pos_x_direction = "t * 0"
snake.pos_y_direction = "t + 1"








        
def repeat():
    
    # ts_now = time.time()
    # ts_delta = ts_now - ts_then
    # print(ts_now)
    # if ts_delta > ts_delta_limit :
    #     print("ts_delta is bigger tha ts_delta_limit")
    #     #ts_then = ts_now
    time.sleep(ts_delta_limit*10**-3)
    #print("rendering stuff")
    # print(counter)
    canvas.counter += 1
    print(snake.pos_x_direction)

    # canvas.clear()
    # snake.pos_x = eval(snake.pos_x_direction, {"t": canvas.counter})
    # snake.pos_y = eval(snake.pos_y_direction, {"t": canvas.counter})
    # # snake.pos_x += 1
    # canvas.addPixel(snake.pos_x%canvas.width, snake.pos_y%canvas.height)
    # canvas.draw()
    repeat()
repeat()
