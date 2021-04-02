import os
import time  
import random
import gc 
import keyboard
import threading
import json

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
        self.food_powerup_clown          = ["❓", "%" ]
        self.food_nerf_garlic            = ["🐉", "Ç" ]
        self.food_powerup_tornado        = ["💫", "?" ]
        self.food_powerup_character_set  = ["💱", "X" ]
        self.food_powerup_gun            = ["🔫", "ö" ]
        self.food_default                = ["🍏", "@" ]
        self.food_default                = ["🍏", "@" ]

        self.eye                         = ["❓", "¬" ]
        self.mouth                       = ["👄", "o" ]
        self.food_default                = ["🌕", "@" ]
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
        game_self = self
        if self.is_sudo() != True:
            print("run with sudo ")    
            exit()
        
        self.running = False
        self.render_id = 0

        self.ascii_map = Ascii_Map()
        
        self.c = Canvas(22,22)

        snake = Object(self)
        snake.name = "snake_utf_8_head"
        snake.limbs = []
        snake.speed = 0.1
        snake.speed_point_3d.x = snake.speed
        snake.collidable = True

        def render_function(self):
            if(self.point_3d_has_new_integer_position): 
                for key, val in enumerate(self.limbs):

                    key = len(self.limbs) - (key+1)

                    val = self.limbs[key]
                    val_before_in_array = self.limbs[key-1]
                    
                    val.position_point_3d.x = val_before_in_array.position_point_3d.x
                    val.position_point_3d.y = val_before_in_array.position_point_3d.y
                
                if(len(self.limbs) > 0):
                    self.limbs[0].position_point_3d.x = self.position_point_3d.x
                    self.limbs[0].position_point_3d.y = self.position_point_3d.y

            if keyboard.is_pressed('w'):  # if key 'w' is down 
                self.speed_point_3d =  Point_3D(0, -self.speed, 0)
            if keyboard.is_pressed('s'):  # if key 's' is down 
                self.speed_point_3d = Point_3D(0, self.speed, 0)
            if keyboard.is_pressed('a'):  # if key 'a' is down 
                self.speed_point_3d =  Point_3D(-self.speed, 0, 0)
            if keyboard.is_pressed('d'):  # if key 'd' is down 
                self.speed_point_3d = Point_3D(self.speed, 0, 0)

            if keyboard.is_pressed('l'): #
                print("l is pressed") 
                for val in range(0, 1):
                    self.add_limb(self)

            if keyboard.is_pressed('n'): # 
                    self.speed = (self.speed + 0.05)
            
            if keyboard.is_pressed('m'): # 
                    self.speed = (self.speed - 0.05)
        
        def add_limb(self):
            limb = Object(self)
            limb.name = "snake_utf_8_body"
            limb.speed = 0
            
            if(len(self.limbs) > 0):
                limb.position_point_3d = self.limbs[-1].position_point_3d
            else: 
                limb.position_point_3d = self.position_point_3d

            self.limbs.append(limb)

        def collision_function(self, collision_with):

            if(collision_with[0].name == "food_default"):
                self.add_limb(self)
                collision_with[0].position_point_3d = random_position_point_3d()

        snake.limbs = []
        snake.add_limb = add_limb
        snake.collision_function = collision_function
                
        snake.render_function = render_function


        def random_position_point_3d():
            return Point_3D(random.randint(0,game_self.c.width-1), random.randint(0,game_self.c.width-1), random.randint(0,2))            

        food = Object(self)
        food.name = "food_default"
        food.position_point_3d = random_point_3d()


    def is_sudo(self): 
        if os.name == 'nt': 
            return True
        else: 
            return os.geteuid() == 0


    def render(self): 
        
        #print(self.c.pysimplegui_printer.event)
        if self.c.pysimplegui_printer.event == None:
            self.end()
        self.c.pysimplegui_printer.window_title =  " render_id:" + str(self.render_id)

        self.render_id += 1
        
        #print("asciisnake render_id: "+str(self.render_id))

        self.c.clear_ascii_pixel_array(self.ascii_map.get_string_by_prop_name("game_black_pixel"))

        #for obj in gc.get_objects():
        for obj in Object._instances:
            
            #self.pygames_events = pygame.event.get()

            #destory object if rendered_count_limit is reached
            if(obj.rendered_count > obj.rendered_count_limit & obj.rendered_count_limit != 0):
                print("deleting obj")
                del obj
                continue

            #cache the position 
            obj.last_render_dict = obj.__dict__.copy()

            #calculate the new speed_point
            obj.speed_point_3d.x = (obj.speed_point_3d.x) + (obj.acceleration_point_3d.x) 
            obj.speed_point_3d.y = (obj.speed_point_3d.y) + (obj.acceleration_point_3d.y) 
            obj.speed_point_3d.z = (obj.speed_point_3d.z) + (obj.acceleration_point_3d.z)

            #calculate new position
            obj.position_point_3d.x = (obj.position_point_3d.x) + (obj.speed_point_3d.x) 
            obj.position_point_3d.y = (obj.position_point_3d.y) + (obj.speed_point_3d.y) 
            obj.position_point_3d.z = (obj.position_point_3d.z) + (obj.speed_point_3d.z) 

            #acceleration delta
            obj.delta_acceleration_point_3d.x = obj.last_render_dict.acceleration_point_3d.x - obj.acceleration_point_3d.x
            obj.delta_acceleration_point_3d.y = obj.last_render_dict.acceleration_point_3d.y - obj.acceleration_point_3d.y
            obj.delta_acceleration_point_3d.z = obj.last_render_dict.acceleration_point_3d.z - obj.acceleration_point_3d.z
         
            #speed delta 
            obj.delta_speed_point_3d.x = obj.last_render_dict.speed_point_3d.x - obj.speed_point_3d.x
            obj.delta_speed_point_3d.y = obj.last_render_dict.speed_point_3d.y - obj.speed_point_3d.y
            obj.delta_speed_point_3d.z = obj.last_render_dict.speed_point_3d.z - obj.speed_point_3d.z
         
            #position delta
            obj.delta_position_point_3d.x = obj.last_render_dict.position_point_3d.x - obj.position_point_3d.x
            obj.delta_position_point_3d.y = obj.last_render_dict.position_point_3d.y - obj.position_point_3d.y
            obj.delta_position_point_3d.z = obj.last_render_dict.position_point_3d.z - obj.position_point_3d.z
            
            #check if delta greater than 1 since 1 is the grid size 
            obj.point_3d_has_new_integer_position  = obj.delta_position_point_3d.x > 1 or obj.delta_position_point_3d.x > 1 or obj.delta_position_point_3d.x

            if( delta):
                obj.point_3d_has_new_integer_position = True

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
                            (int(obj2.point_3d.x) == int(obj.point_3d.x)) and 
                            (int(obj2.point_3d.y) == int(obj.point_3d.y)) and
                            (int(obj2.point_3d.z) == int(obj.point_3d.z))
                            ):
                                obj.collision_with.append(obj2)

                if(len(obj.collision_with) > 0):
                    if(obj.collision_function != None):
                        obj.collision_function(obj, obj.collision_with)
        

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
        self.position_point_3d = Point_3D(0,0,1)
        #  speed vector which is used to calculate the new position on an object
        self.speed_point_3d = Point_3D(0,0,0)
        # acceleration
        self.acceleration_point_3d = Point_3D(0,0,0)
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
        # is set to true if the new point_3d.x and .y position differenciate from self.last_rendered_point_3d 
        self.point_3d_has_new_integer_position = False
        #a copy of the object from the last render which can be used to calculate deltas
        self.last_render_dict = self.__dict__.copy()


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
        
        time.sleep(0.016) # 1000(ms)/60(fps) => 0.016 ms sleep
        #print(self.pysimplegui_printer.event)
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
