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
        self.width = 22
        self.height = 22
        self.output = ""
        self.white_pixel = "　"
        self.white_pixel = "🌑"
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

    def addPixel(self, x,y, string):
        if x > self.width | y > self.height:
            print("canvas is not big enought to add a pixel at this position")
        else:
            self.pixel_matrix[y][x] = string


    def draw(self):
        self.output = ""
        for value in self.pixel_matrix:
            for value in value:
                if isinstance(value, str):
                    self.output += value
                else:
                    self.output += self.white_pixel
            self.output +="\n"

        print(self.output)

class Limb: 
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def get_position_string(self):
        return str(self.x) + "|" + str(self.y)

class Snake:
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.pos_x_direction = "snake.pos_x"
        self.pos_y_direction = "snake.pos_y"
        #self.utf_8_head = "◈"
        self.utf_8_head = "🌝"
        #self.utf_8_body = "○"
        self.utf_8_body = "🌕"
        #self.utf_8_tail = "◌"
        self.utf_8_tail = "🌕"
        self.limbs = [Limb(0,0)]
        self.limbs_for_collision_detection = ["0|0"]
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
        new_limbs = []
        new_limbs_for_collision_detection = []
        for key, value in enumerate(self.limbs):
            
            if key > 0:
                new_limb = Limb(self.limbs[key-1].x, self.limbs[key-1].y)

                new_limbs.append(new_limb)
                new_limbs_for_collision_detection.append(new_limb.get_position_string())
        
        new_pos_limb = Limb(new_pos_x, new_pos_y)
        new_limbs.insert(0, new_pos_limb)
        new_limbs_for_collision_detection.insert(0, new_pos_limb.get_position_string())


        self.pos_x = new_pos_x
        self.pos_y = new_pos_y
        self.limbs = new_limbs
        self.limbs_for_collision_detection = new_limbs_for_collision_detection
        self.detect_collision()


    def detect_collision(self):
        #print(snake.limbs_for_collision_detection)
        #print(set(snake.limbs_for_collision_detection))

        multiple_limbs_on_same_position_exist = len(self.limbs_for_collision_detection) != len(set(self.limbs_for_collision_detection))
        if multiple_limbs_on_same_position_exist:
            print("Snake self collision, game over!")
            exit(0)

class Food:
    def __init__(self, canvas, snake):
        self.x = random.randint(0, canvas.width)
        self.y = random.randint(0, canvas.height)
        self.utf_8 = "🍎"
        
        while self.check_collision_with_snake(snake) | self.x == canvas.width | self.x == 0 | self.y == canvas.height | self.y == 0:
            self.x = random.randint(0, canvas.width)
            self.y = random.randint(0, canvas.height)
        print("position food")
        print(str(self.x) + "|" + str(self.y))

    def check_collision_with_snake(self, snake):
        pos_string = str(self.x) + "|" + str(self.y)
        if pos_string in snake.limbs_for_collision_detection:
            return True
        else:
            return False




canvas = Canvas()

snake = Snake()
food = Food(canvas,snake)

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
        #print("Stop!")
        exit(0)
 
    if (char == "a"):
        snake.pos_x_direction_left()
        #print("Left pressed")

 
    elif (char == "d"):
        snake.pos_x_direction_right()
        #print("Right pressed")

 
    elif (char == "w"):
        snake.pos_x_direction_up()
        #print("Up pressed")

    
    elif (char == "s"):
        snake.pos_x_direction_down()
        #print("Down pressed")

    # elif(char == "l"):
    #     #limb = Limb(snake.limbs[-1].x, snake.limbs[-1].y)

    #     # print(snake.limbs[-1].x)
    #     # exit()
    #print("rendering stuff")
    # print(counter)
    canvas.counter += 1

    canvas.clear()


        

    snake.set_position()
    # # snake.pos_x += 1

    for key, value in enumerate(snake.limbs):
        if(key == 0):
            snake_utf_8_symbol = snake.utf_8_head
        
        if(key > 0 & (len(snake.limbs) > 2)):
            snake_utf_8_symbol = snake.utf_8_body
        
        if((key == (len(snake.limbs)-1)) & (len(snake.limbs) > 1)):
            snake_utf_8_symbol = snake.utf_8_tail

        canvas.addPixel(value.x%canvas.width, value.y%canvas.height, snake_utf_8_symbol)
    
    

    if food is not None:
        food_eaten = food.check_collision_with_snake(snake)

        if(food_eaten):
            # print("food eaten")
            global food
            food = Food(canvas, snake)
            limb = Limb(0,0)
            snake.limbs.append(limb)
        
        canvas.addPixel(food.x%canvas.width, food.y%canvas.height, food.utf_8)


    canvas.draw()
    
    repeat()
repeat()



