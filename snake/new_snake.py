#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import time, tty, sys

class Character_set():
    def __init__(self):
        self.name = "classical"
        self.game_white_pixel = " " 
        self.game_black_pixel = " " 
        self.canvas_white_pixel = " " 
        self.canvas_black_pixel = "-" 
        self.game_utf_8_border = "#" 
        self.snake_utf_8_head = "O"
        self.snake_utf_8_body = "o"
        self.snake_utf_8_tail = "9"
        self.food_powerup_mushroom = "Ͳ"
        self.food_powerup_slow = "◷"
        self.food_powerup_portal = "α"
        self.food_powerup_brick = "#"
        self.food_powerup_fast = "☇"
        self.food_powerup_character_set = "?"
        self.food_powerup_tornado = "X"
        self.food_default = "@"
    def __getitem__(self, item):
        character = getattr(self, item)
        if(isinstance(character, list)):
            return random.choice(character)
        else:
            return character


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.output = ""
        self.pixel_matrix = []
        self.clear_pixel_matrix = []
        self.counter = 0
        self.character_set_property_name_white_pixel = "canvas_white_pixel"
        self.character_set_property_name_black_pixel = "canvas_black_pixel"
        self.white_pixel = character_set[self.character_set_property_name_white_pixel]
        self.black_pixel = character_set[self.character_set_property_name_black_pixel]
        
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

        # for x in range(0, self.height):
        #     print("\n")

    def addPixel(self, x,y, string):
        x = int(x)
        y = int(y)
        if x > self.width | y > self.height:
            print("canvas is not big enought to add a pixel at this position")
        else:
            self.pixel_matrix[y][x] = string


    def draw(self):
        global character_set
        self.output = ""
        for value in self.pixel_matrix:
            for value in value:
                if isinstance(value, str):
                    self.output += value
                else:
                    self.output += character_set[self.character_set_property_name_white_pixel]
            self.output +="\n"

        print(self.output)

class Game: 
    def __init__(self):
        self.running = False
        self.delta_ms = 0
        self.now_ms = 0
        self.then_ms = 0
        self.fps = 60
        self.interval_ms = self.get_interval_ms()
        self.real_interval_ms = 0
        self.t = 0

        self.setup()
    
    def setup(self):
        self.canvas = Canvas(11,11)

    def get_interval_ms(self):
        return 1000 / self.fps    

    def start(self):
        if self.running:
            return True

        self.running = True

        while self.running:
            self.now_ms = int(round(time.time() * 1000))
            self.delta_ms = self.now_ms - self.then_ms
            if self.delta_ms >= self.interval_ms:
                self.t += 1
                self.real_interval_ms = self.delta_ms 
                self.render_frame()
                self.then_ms = self.now_ms

    def stop(self):
        self.running = False
        print(self.running)
        exit()


    def render_frame(self):
        print("rendering " + str(self.t) + " frame, current fps is:")
        print(1000 / self.real_interval_ms)

        self.canvas.clear()
        self.canvas.addPixel(0, self.canvas.height-1,"a")
        self.canvas.draw()


character_set = Character_set()
game = Game()
game.start()