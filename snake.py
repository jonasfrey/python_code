#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys, tty, termios, time, random
from select import select


def getch(timeout):                                                                                                                                          
    fd = sys.stdin.fileno()                                                                                                                                   
    old_settings = termios.tcgetattr(fd)                                                                                                                      
    ch = None                                                                                                                                                 
    try:                                                                                                                                                      
        tty.setraw(fd)                                                                                                                                        
        rlist, _, _ = select([sys.stdin], [], [], timeout)                                                                                                    
        if len(rlist) > 0:                                                                                                                                    
            ch = sys.stdin.read(1)                                                                                                                            
    finally:                                                                                                                                                  
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)                                                                                                
    return ch                                      
    

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
        self.black_pixel = "•"
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

class Limb: 
    def __init__(self, x,y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.pos_x_direction = "snake.pos_x"
        self.pos_y_direction = "snake.pos_y"
        self.limbs = [Limb(1,0), Limb(0,0)]
        self.counter = 0
        
    def pos_x_direction_up(self):
        self.pos_x_direction = "snake.pos_x"
        self.pos_y_direction = "snake.pos_y-1"

    def pos_x_direction_down(self):
        self.pos_x_direction = "snake.pos_x"
        self.pos_y_direction = "snake.pos_y+1"
    
    def pos_x_direction_right(self):
        self.pos_x_direction = "snake.pos_x+1"
        self.pos_y_direction = "snake.pos_y"
    
    def pos_x_direction_left(self):
        self.pos_x_direction = "snake.pos_x-1"
        self.pos_y_direction = "snake.pos_y"

    def set_position(self):
        new_pos_x = eval(snake.pos_x_direction, {"snake": snake})
        new_pos_y = eval(snake.pos_y_direction, {"snake": snake})
        #if new_pos_x != self.limbs[0].x | new_pos_y != self.limbs[0].y:
        limbs_len = len(self.limbs)-1
        for key, value in enumerate(self.limbs):
            reverse_key = limbs_len - key - 1
            if key != limbs_len-1:
                value.x = self.limbs[reverse_key-1].x
                value.y = self.limbs[reverse_key-1].y
        
        self.limbs[0].x = new_pos_x
        self.limbs[0].y = new_pos_y
        self.pos_x = new_pos_x
        self.pos_y = new_pos_y


# class Food:
#     def __init__(self, canvas, snake):
#         self.pos_x = random.randint(0, canvas.width)
#         self.pos_y = random.randint(0, canvas.height)
        
#         while self.pos_x < 6:
#             print(i)
#             i += 1
#         self.pos_x_direction = "snake.pos_x"
#         self.pos_y_direction = "snake.pos_y"
#         self.counter = 0




snake = Snake()

canvas = Canvas()

ts_now = time.time()
ts_then = time.time()
ts_delta_limit = 100




        
def repeat():
    
    # ts_now = time.time()
    # ts_delta = ts_now - ts_then
    # print(ts_now)
    # if ts_delta > ts_delta_limit :
    #     print("ts_delta is bigger tha ts_delta_limit")
    #     #ts_then = ts_now
    #time.sleep()
    char = getch(ts_delta_limit*10**-3)
        
    if (char == "p"):
        print("Stop!")
        exit(0)
 
    if (char == "a"):
        snake.pos_x_direction_left()
        print("Left pressed")

 
    elif (char == "d"):
        snake.pos_x_direction_right()
        print("Right pressed")

 
    elif (char == "w"):
        snake.pos_x_direction_up()
        print("Up pressed")

    
    elif (char == "s"):
        snake.pos_x_direction_down()
        print("Down pressed")

    elif(char == "l"):
        #limb = Limb(snake.limbs[-1].x, snake.limbs[-1].y)
        limb = Limb(snake.limbs[-1].x, snake.limbs[-1].y)
        snake.limbs.append(limb)
        # print(snake.limbs[-1].x)
        # exit()
    #print("rendering stuff")
    # print(counter)
    canvas.counter += 1

    canvas.clear()

    snake.set_position()

    # # snake.pos_x += 1
    for value in snake.limbs:
        print(str(value.x) +":"+ str(value.y))
        
        canvas.addPixel(value.x%canvas.width, value.y%canvas.height)

    canvas.draw()
    
    repeat()
repeat()



