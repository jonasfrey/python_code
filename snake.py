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

class Game:
    def __init__(self):
        self.running = False
        self.over = False
        self.message = ""
        self.food = None
        self.white_pixel = "🌕"
        self.black_pixel = "🌑"
        self.utf_8_border = "💀"
        self.detect_canvas_size = False
        self.border_collision = True
        self.snake = None
        self.canvas = None
        self.ts_now = time.time()
        self.ts_then = time.time()
        self.ts_delta_limit = 30


        self.setup()


    def setup(self):
        if self.detect_canvas_size:
            max_height = 200
            for value in range(0, max_height):
                val = max_height - value
                output = self.white_pixel
                if(val % 5 == 0):
                    output = self.black_pixel
                
                print(output)

            height = input("How many full groups of 4 yellow + 1 black moons do you see ?:")
            height = height * 4

            max_width = 200
            output_str = ""
            for value in range(0, max_width): 
                if(value % 5 == 0):
                    output_str += self.black_pixel
                else:
                    output_str += self.white_pixel

            print(output_str)

            width = input("after how many groups of 4 yellow + 1 black moons does the line break ?:")
            width = width * 4
        else:
            width = 20
            height = 20
        
        self.canvas = Canvas(width, height)
        self.border_pixels = []

        for value in range(0, width-1):
            self.border_pixels.append(Position(value, 0))
            self.border_pixels.append(Position(value, height-1))
        for value in range(0, height-1):
            self.border_pixels.append(Position(0, value))
            self.border_pixels.append(Position(width-1, value))

        self.border_pixels_for_collision_detection = list(map(lambda v: v.string, self.border_pixels))


        self.snake = Snake()
        self.food = Food(self.canvas,self.snake)
        self.repeat()



    def repeat(self):
        
        # ts_now = time.time()
        # ts_delta = ts_now - ts_then
        # print(ts_now)
        # if ts_delta > ts_delta_limit :
        #     print("ts_delta is bigger tha ts_delta_limit")
        #     #ts_then = ts_now
        #time.sleep()
        char = getch(self.ts_delta_limit*10**-3)
            
        if (char == "p"):
            #print("Stop!")
            exit(0)
    
        if (char == "a"):
            self.snake.pos_x_direction_left()
            #print("Left pressed")

    
        elif (char == "d"):
            self.snake.pos_x_direction_right()
            #print("Right pressed")

    
        elif (char == "w"):
            self.snake.pos_x_direction_up()
            #print("Up pressed")

        
        elif (char == "s"):
            self.snake.pos_x_direction_down()
            #print("Down pressed")

        # elif(char == "l"):
        #     #limb = Position(self.snake.limbs[-1].x, self.snake.limbs[-1].y)

        #     # print(self.snake.limbs[-1].x)
        #     # exit()
        #print("rendering stuff")
        # print(counter)
        self.canvas.counter += 1

        self.canvas.clear()


        self.snake.set_position_detect_collision()
        # detect border collision 
        # print("self.snake.position.string")
        # print(self.snake.position.string)

        # print("self.border_pixels_for_collision_detection")
        # print(self.border_pixels_for_collision_detection)
        if self.snake.position.string in self.border_pixels_for_collision_detection:
            print("collidet with wall")
            exit(0)

        # # self.snake.pos_x += 1

        for key, value in enumerate(self.snake.limbs):
            if(key == 0):
                self.snake_utf_8_symbol = self.snake.utf_8_head
            
            if(key > 0 & (len(self.snake.limbs) > 2)):
                self.snake_utf_8_symbol = self.snake.utf_8_body
            
            if((key == (len(self.snake.limbs)-1)) & (len(self.snake.limbs) > 1)):
                self.snake_utf_8_symbol = self.snake.utf_8_tail

            self.canvas.addPixel(value.x%self.canvas.width, value.y%self.canvas.height, self.snake_utf_8_symbol)
        
        # draw border 
        if self.border_collision:
            for value in self.border_pixels:
                #print(value.string)
                self.canvas.addPixel(value.x, value.y, self.utf_8_border)

        print(self.food)
        if self.food is not None:
            self.canvas.addPixel(self.food.position.x%self.canvas.width, self.food.position.y%self.canvas.height, self.food.utf_8)

            food_eaten = self.food.check_collision_with_snake(self.snake)

            if(food_eaten):
                # print("food eaten")
                # time.sleep(1)
                self.food = None
                self.snake.add_limb()
                self.food = Food(self.canvas, self.snake)
                #print("food eaten limb added")

        


        self.canvas.draw()
        
        self.repeat()






class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
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
        x = int(x)
        y = int(y)
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

class Position: 
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.string = self.get_position_string()

    def get_position_string(self):
        return str(self.x) + "|" + str(self.y)

class Snake:
    def __init__(self):
        self.pos_x_direction = "snake.position.x"
        self.pos_y_direction = "snake.position.y"

        self.speed = 0.5
        #self.utf_8_head = "◈"
        self.utf_8_head = "🌝"
        #self.utf_8_body = "○"
        self.utf_8_body = "🌕"
        #self.utf_8_tail = "◌"
        self.utf_8_tail = "🌕"
        self.position = Position(1,1)
        self.float_position = Position(1,1)
        self.limbs = [self.position]
        self.limbs_for_collision_detection = list(map(lambda v: v.string, self.limbs))
        self.counter = 0
        
    def pos_x_direction_up(self):
        self.pos_x_direction = "snake.float_position.x"
        self.pos_y_direction = "snake.float_position.y-1* snake.speed"

    def pos_x_direction_down(self):
        self.pos_x_direction = "snake.float_position.x"
        self.pos_y_direction = "snake.float_position.y+1* snake.speed"
    
    def pos_x_direction_right(self):
        self.pos_x_direction = "snake.float_position.x+1* snake.speed"
        self.pos_y_direction = "snake.float_position.y"
    
    def pos_x_direction_left(self):
        self.pos_x_direction = "snake.float_position.x-1* snake.speed"
        self.pos_y_direction = "snake.float_position.y"

    def set_position_detect_collision(self):
        new_pos_x = eval(self.pos_x_direction, {"snake": self})
        new_pos_y = eval(self.pos_y_direction, {"snake": self})
        
        self.float_position.x = new_pos_x
        self.float_position.y = new_pos_y

        new_pos_x = int(new_pos_x)
        new_pos_y = int(new_pos_y)
        
        #if new_pos_x != self.limbs[0].x | new_pos_y != self.limbs[0].y:
        new_limbs = []
        for key, value in enumerate(self.limbs):
            
            if key > 0:
                new_limb = Position(self.limbs[key-1].x, self.limbs[key-1].y)

                new_limbs.append(new_limb)
            
        
        new_pos_limb = Position(new_pos_x, new_pos_y)
        new_limbs.insert(0, new_pos_limb)
        self.position = new_pos_limb
        self.limbs = new_limbs
        self.limbs_for_collision_detection = list(map(lambda v: v.string, self.limbs))
        if self.self_collision():
            print("Snake self collision, game over!")
            exit(0)

    def self_collision(self):
        try:
            index_of_first_limb = self.limbs_for_collision_detection.index( self.limbs[0].string, 2)
            print(index_of_first_limb)
        except:
            print("no collision :)")
        
        
        #multiple_limbs_on_same_position_exist = len(self.limbs_for_collision_detection) != len(set(self.limbs_for_collision_detection))
        #return multiple_limbs_on_same_position_exist


    def add_limb(self):
        # count = 0
        # limb = Position(self.limbs[-1].x + count, self.limbs[-1].y + count)
        # marged_limbs_for_collision_detection = self.limbs_for_collision_detection + [limb.string]

        # while limb.string in marged_limbs_for_collision_detection:
        #     count = count + 1
        #     limb = Position(self.limbs[-1].x + count, self.limbs[-1].y + count)
        #     marged_limbs_for_collision_detection = self.limbs_for_collision_detection + [limb.string]

        self.limbs.append(Position(1111, 1111))

class Food:
    def __init__(self, canvas, snake):
        self.position = Position(random.randint(1, canvas.width-1), random.randint(1, canvas.height-1))
        self.utf_8 = "🍎"
        
        while self.check_collision_with_snake(snake):
            self.position = Position(random.randint(1, canvas.width-1), random.randint(1, canvas.height-1))


    def check_collision_with_snake(self, snake):
        
        if self.position.string in snake.limbs_for_collision_detection:
            return True
        else:
            return False


game = Game()

