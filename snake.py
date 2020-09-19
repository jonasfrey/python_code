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
        self.food = []
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
        self.t = 0
        self.next_random_item_ts = 0

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


        self.next_random_item_ts = random.randint(0, 200)
        self.snake = Snake()
        self.food.append(Food(self, self.canvas, self.snake, "default"))
        self.food.append(Food(self, self.canvas, self.snake, "powerup_slow"))
        self.repeat()


    def check_and_add_random_item(self):

        if(self.t >= self.next_random_item_ts):
            food = Food(self, self.canvas, self.snake, "random")
            self.next_random_item_ts = self.next_random_item_ts + random.randint(0, 200)
            if(len(self.food) < len(food.types) ):
                self.food.append(food)

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

        elif(char == "l"):
            self.snake.limbs.append(Position(0, 0))

        #print("rendering stuff")
        # print(counter)
        self.canvas.counter += 1
        self.t = self.canvas.counter
        self.canvas.clear()

        print(self.snake.limbs_for_collision_detection)

        self.snake.set_position_detect_collision(self.t)
        self.snake.call_power_ups(self)

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


        for value in self.food:
            self.canvas.addPixel(value.position.x%self.canvas.width, value.position.y%self.canvas.height, value.utf_8)
            
            food_eaten = value.check_collision_with_snake(self.snake)

            if(food_eaten):
                getattr(value, 'pickup_' + value.type_name)(self)

            value.live_count += 1

            if (value.type_name != "default") & (value.live_count > value.time_to_live):
                value.destroy(self) 

        #     self.canvas.addPixel(self.food.position.x%self.canvas.width, self.food.position.y%self.canvas.height, self.food.utf_8)

        #     food_eaten = self.food.check_collision_with_snake(self.snake)

        #     if(food_eaten):
        #         getattr(self.food, 'pickup_' + self.food.type_name)(self)

        self.check_and_add_random_item()


        self.canvas.draw()

        # print("self.food.position.string")
        # print(self.food.position.string)
        
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
        
        self.pixel_matrix = self.get_cleared_matrix()

        #print(self.pixel_matrix)

    def get_cleared_matrix(self):
        clear_pixel_matrix = []
        for y in range(0, self.height):
            y_array = []
            for x in range(0, self.width):
                y_array.append(False)
            clear_pixel_matrix.append(y_array)
        return clear_pixel_matrix
    def clear(self):
        #print("clearing")
        self.pixel_matrix = self.get_cleared_matrix()

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
        self.string_int = self.get_position_string_int()

    def is_colliding(self, position): 
        return self.x == position.x & self.y == position.y
    def get_position_string(self):
        return str(self.x) + "|" + str(self.y)
    def get_position_string_int(self):
        return str(int(self.x)) + "|" + str(int(self.y))

class Snake:
    def __init__(self):
        self.pos_x_direction = "snake.position.x"
        self.pos_y_direction = "snake.position.y"
        self.power_ups = []
        self.speed = 5
        self.speed_max = 10
        #self.utf_8_head = "◈"
        self.utf_8_head = "🌝"
        #self.utf_8_body = "○"
        self.utf_8_body = "🌕"
        #self.utf_8_tail = "◌"
        self.utf_8_tail = "🌕"
        self.position = Position(1,1)
        self.limbs = [self.position]
        self.limbs_for_collision_detection = list(map(lambda v: v.string, self.limbs))
        self.counter = 0
        
    def pos_x_direction_up(self):
        self.pos_x_direction = "snake.position.x"
        self.pos_y_direction = "snake.position.y - 1"

    def pos_x_direction_down(self):
        self.pos_x_direction = "snake.position.x"
        self.pos_y_direction = "snake.position.y + 1"
    
    def pos_x_direction_right(self):
        self.pos_x_direction = "snake.position.x + 1"
        self.pos_y_direction = "snake.position.y"
    
    def pos_x_direction_left(self):
        self.pos_x_direction = "snake.position.x - 1"
        self.pos_y_direction = "snake.position.y"

    def set_position_detect_collision(self, t):
        print("snake.speed")
        print(self.speed)
        self.speed_modulo = self.speed_max - self.speed
        if int(t % self.speed_modulo) != 0:
            return 
        # calculate new position of first limb
        new_pos_x = eval(self.pos_x_direction, {"snake": self, "t":t})
        new_pos_y = eval(self.pos_y_direction, {"snake": self, "t":t})
        

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
            #print(index_of_first_limb)
            return True
        except:
            #print("no collision :)")
            return False
        
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

        self.limbs.append(Position(0, 0))
        #print(self.limbs_for_collision_detection)
    def call_power_ups(self, game):
        for value in self.power_ups:
            value.func(value, game)

class Power_up: 
    def __init__(self, func, time_to_live):
        self.func = func
        self.time_to_live = time_to_live
        self.live_count = 0
    

class Food:
    def __init__(self, game, canvas, snake, type_name):
        self.live_count = 0
        self.type_name = type_name
        self.time_to_live = None
        self.types = ["powerup_mushroom", "powerup_slow", "default"]

        if self.type_name == "random":
            random_choice = self.types[:]
            random_choice.remove("default")
            self.type_name = random.choice(random_choice)
            #prevent having multiple food of same type_name
            # double_power_up = False
            # for value in random_choice:
            #     if len(filter(lambda val: val.type_name == self.type_name, game.food)) > 0:
            #         double_power_up = True
            
            # if double_power_up:
            #     self.type_name = "default"


        if self.type_name == "default":
            self.utf_8 = "🍎"

        if self.type_name == "powerup_mushroom":
            self.utf_8 = "🍄"
            self.time_to_live = 200

        if self.type_name == "powerup_slow":
            self.utf_8 = random.choice(["🐢", "🦥", "🐌"])
            self.time_to_live = 200

            
        self.position = Position(random.randint(1, canvas.width-2), random.randint(1, canvas.height-2))



        if (self.position.x ==  0  | self.position.y == 0):
            time.sleep(1)

        while self.check_collision_with_snake(snake) | self.check_collision_with_other_food(game):
            self.position = Position(random.randint(1, canvas.width-2), random.randint(1, canvas.height-2))

    def pickup_default(self, game):
        self.destroy(game)
        game.snake.add_limb()
        game.food.append(self.__class__(game, game.canvas, game.snake, "default"))
    
    def pickup_powerup_mushroom(self, game):
        self.destroy(game)
        game.snake.add_limb()
        game.snake.add_limb()
        game.snake.add_limb()
        game.snake.add_limb()
        game.snake.add_limb()
        game.snake.add_limb()
        game.snake.add_limb()
        game.snake.add_limb()
    
    def pickup_powerup_slow(self, game):
        
        def func(self, game):
            print("self should be powerup")
            if self.live_count == 0:
                self.snake_speed_cached = game.snake.speed

            game.snake.speed = 1
            self.live_count += 1
            if self.live_count > self.time_to_live:
                game.snake.speed = self.snake_speed_cached
                game.snake.power_ups.remove(self)

        power_up = Power_up(func, 100)
        game.snake.power_ups.append(power_up)

        self.destroy(game)


    def destroy(self, game):
        game.food.remove(self)

    def check_collision_with_other_food(self, game):
        for value in game.food:
            if value.position.is_colliding(self.position):
                return True
        return False

    def check_collision_with_snake(self, snake):
        
        if self.position.string in snake.limbs_for_collision_detection:
            return True
        else:
            return False


game = Game()

