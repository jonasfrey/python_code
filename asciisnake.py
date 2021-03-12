import os
import time  
import random
import gc 
import keyboard
import threading
import json
import pygame

from pysimplegui_printer import PySimpleGUI_Printer

class Ascii_Map:
    def __init__(self):
        self.names                       = ["emojis", "classic"]
        self.name = "emojis"
        self.game_black_pixel            = ["🌑", " " ]
        self.game_utf_8_border           = ["🌕", "#" ]
        self.snake_utf_8_head            = ["🌕", "O" ]
        self.snake_utf_8_body            = ["🌕", "o" ]
        self.snake_utf_8_tail            = ["🌕", "9" ]
        self.food_powerup_mushroom       = ["🍄", "Ͳ" ]
        self.food_powerup_slow           = ["🐢", "◷" ]
        self.food_powerup_portal         = ["🔄", "α" ]
        self.food_powerup_brick          = ["❓", "#" ]
        self.food_powerup_fast           = ["💨", "☇" ]
        self.food_powerup_clown           = ["❓", "%" ]
        self.food_nerf_garlic           = ["🐉", "Ç" ]
        self.food_powerup_tornado        = ["💫", "?" ]
        self.food_powerup_character_set  = ["💱", "X" ]
        self.food_powerup_gun              =["🔫", "ö" ]
        self.food_default                = ["🍏", "@" ]
        self.food_default                = ["🍏", "@" ]
        

        self.eye                         = ["❓", "¬" ]
        self.mouth                       = ["👄", "o" ]
        self.food_default                = ["🍏", "@" ]
        self.fallback                    = ["🌑", " " ]
    

    """
    @param prop_name string 
    """
    def get_string_by_prop_name(self, prop_name):
        index = self.names.index(self.name)

        if(hasattr(self, prop_name) == False):
            ascii_string = self.fallback[index]
        else:
            ascii_string = getattr(self, prop_name)[index]

        return ascii_string

class Game: 
    def __init__(self):

        if self.is_sudo() != True:
            print("run with sudo ")    
            exit()
        
        self.running = False
        self.render_id = 0

        self.ascii_map = Ascii_Map()
        
        self.c = Canvas(22,22)

        snake = Object(self)
        snake.name = "snake_utf_8_head"
        snake.speed_point_3d.x = 0.1

        def snake_render_function(self):
            if(self.point_3d.x > 10):
                self.point_3d.x = 0

        snake.render_function = snake_render_function 
        
        
        game_self = self


    def is_sudo(self): 
        if os.name == 'nt': 
            return True
        else: 
            return os.geteuid() == 0


    def render(self): 
        
        self.render_id += 1
        
        print("asciisnake render_id: "+str(self.render_id))

        self.c.clear_ascii_pixel_array(self.ascii_map.get_string_by_prop_name("game_black_pixel"))

        #for obj in gc.get_objects():
        for obj in Object._instances:

            #destory object if rendered_count_limit is reached
            if(obj.rendered_count > obj.rendered_count_limit & obj.rendered_count_limit != 0):
                del obj
                continue

            #cache the position 
            obj.last_rendered_point_3d.x = obj.point_3d.x
            obj.last_rendered_point_3d.z = obj.point_3d.z
            obj.last_rendered_point_3d.y = obj.point_3d.y

            #calculate new position
            obj.point_3d.x = (obj.point_3d.x) + (obj.speed_point_3d.x) 
            obj.point_3d.y = (obj.point_3d.y) + (obj.speed_point_3d.y) 
            obj.point_3d.z = (obj.point_3d.z) + (obj.speed_point_3d.z) 
            
            if(obj.render_function != None):
                obj.render_function(obj)

            #temporarily render function which can be used for temporarily speedboost and other stuff
            if(len(obj.temp_render_functions) > 0):
                for trf in obj.temp_render_functions:
                    trf.rendered_count += 1

                    if trf.rendered_count == 1:
                        if(trf.render_function_firstcall != None):
                            trf.render_function_firstcall(trf, obj)
                    
                    trf.render_function(trf, obj)

                    if(trf.rendered_count > trf.rendered_count_limit):
                        if(trf.render_function_lastcall != None):
                            trf.render_function_lastcall(trf, obj)

                        obj.temp_render_functions.remove(trf)
            

            obj.collision_with = []

            if obj.collidable == True :
                for obj2 in gc.get_objects():

                    if isinstance(obj2, Object):
                        if obj2 == obj or obj2.rendered_count < 2: #ignore just spawned objects:
                            continue
                        if (
                            (obj2.point_3d.x == obj.point_3d.x) and 
                            (obj2.point_3d.y == obj.point_3d.y) and
                            (obj2.point_3d.z == obj.point_3d.z)
                            ):
                                obj.collision_with.append(obj2)

                if(len(obj.collision_with) > 0):
                    if(obj.collision_function != None):
                        obj.collision_function(obj.parent_class_instance, obj, obj.collision_with)
          
                    
        # will search for ascii symbol in map or if not found return fallback 
        ascii_string = self.ascii_map.get_string_by_prop_name(obj.name)

        #ascii_string  can be overwritten by having the property ascii character
        if(hasattr(obj, "ascii_character")):
            ascii_string = getattr(obj, "ascii_character")

        # increment the rendered_count on object since it gets rendered
        obj.rendered_count += 1

        self.c.add_ascii(obj.point_3d.x, obj.point_3d.y, obj.point_3d.z, ascii_string)


    def end(self):
        self.running = False            
        exit()

    def start(self):
        self.running = True
        
        while self.running:
            self.render()
            self.c.render()

class Point_3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        if z < 0 or z > 2:
            raise Exception("z index must be -1 < z < 3") 
        self.z = z


class Temp_Render_Function:
    def __init__(self, render_function): 

        self.rendered_count = 0
        self.rendered_count_limit = 0
        # a callback which gets called and passed (trf temp_render_function instance, obj)
        self.render_function = render_function
        self.render_function_firstcall = None
        self.render_function_lastcall = None
        self.before_remove = None


class Object: 
    _instances = []
    def __init__(self, parent_class_instance):
        # 'parent' object
        self.parent_class_instance = parent_class_instance
        #  point
        self.point_3d = Point_3D(0,0,1)
        self.last_rendered_point_3d = Point_3D(0,0,1)
        #  speed vector which is used to calculate the new position on an object
        self.speed_point_3d = Point_3D(0,0,0)
        # snake, item, enemy... 
        self.name = "default"
        # defines how many with the same name can exists at the same time
        self.co_existance_limit = 1
        # on every render this gets incremented
        self.rendered_count = 0 # 
        # when the render_count has reached the render_count_limit, the object gets destroyed
        self.rendered_count_limit = 0 # 0 infinity
        # boolean wether object is collidable
        self.collidable = False
        # a callback which is getting executed on every render 
        #optional , by default None
        self.render_function = None
        # temporary render functions
        self.temp_render_functions = []
        # a callback which is getting exectued when the object collides with other objects
        #optional , by default None 
        self.collision_function = None
        # other object this collided with will be appended here
        self.collision_with = []

        # append instance to class object property 
        self._instances.append(self)


class GenericObject(Object):
    def __init__(self):
        self.generic = True

class Canvas: 
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ascii_pixel_array = [" "] * (self.width*self.height)
        self.ascii_pixel_z_axis_arrays = [[],[],[]]
        self.pysimplegui_printer = PySimpleGUI_Printer()

        """
        @param x int 
        @param y int 
        @param z int 
        """
    def add_ascii(self, x, y, z,  ascii):
        #print("add_ascii: " + str(x) + "|" + str(y) + "|" +str(z) + ", "+ ascii)
        if(x > self.width or y > self.height): 
            print("skipping add_ascii: cannot draw out of canvas width and canvas height the following x|y was passed: " + str(x)+"|"+str(y) )
            return False

        array_index = self.get_array_index_by_x_y((x), (y))
        self.ascii_pixel_z_axis_arrays[z].append([x,y,ascii])

    def draw_ascii(self, x, y, ascii):
        array_index = self.get_array_index_by_x_y(x, y)
        try:
            self.ascii_pixel_array[array_index] = ascii
        except IndexError as e:
            print("skipping index " + str(array_index) + ": impossible to draw out of canvas")

    def get_array_index_by_x_y(self, x, y):
        index = int(y) * self.width + int(x)
        return index 

    def get_x_y_by_array_index(self, array_index): 
        y = int(array_index/self.width)
        x = int(array_index % self.width)
        return Point_3D(x,y)

    def clear_ascii_pixel_array(self, black_pixel = " "):
        self.ascii_pixel_array =  [black_pixel] * (self.width*self.height)
        self.ascii_pixel_z_axis_arrays = [[],[],[]]

    def create_ascii_pixel_array(self):
        for arr in self.ascii_pixel_z_axis_arrays:
            for x_y_ascii in arr:
                self.draw_ascii(x_y_ascii[0],x_y_ascii[1],x_y_ascii[2])

    def render(self):
        self.create_ascii_pixel_array()
        render_string = ""
        for key, val in enumerate(self.ascii_pixel_array):
            if (key+1) % self.width == 0:
                render_string += val
                render_string += "\n"
            else:
                render_string += val
        
        time.sleep(0.001) # 1000(ms)/60(fps) => 0.016 ms sleep
        self.pysimplegui_printer.print(render_string)
        #self.pygame_printer.clear()
        #self.clear_terminal()
        #print(render_string)

    # define our clear function 
    def clear_terminal(self): 
        #print("\n".join([""]*100))
        #print(chr(27) + "[2J")
        os.system('cls' if os.name == 'nt' else 'clear')
        #print("".join(["\n"]*10))


game = Game()
game.start()
