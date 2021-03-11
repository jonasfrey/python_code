import os
import time  
import random
import gc 
import keyboard
import threading
import json

class Ascii_Map:
    def __init__(self):
        self.names                       = ["emojis", "classic"]
        self.name = "emojis"
        self.game_black_pixel            = ["🌑", " " ]
        self.game_utf_8_border           = ["🧱", "#" ]
        self.snake_utf_8_head            = ["🌝", "O" ]
        self.snake_utf_8_head_2           = ["🌝", "X" ]
        self.snake_utf_8_head_3           = ["🌝", "8" ]
        self.snake_utf_8_body            = ["🌕", "o" ]
        self.snake_utf_8_tail            = ["🌕", "9" ]
        self.food_powerup_mushroom       = ["🍄", "Ͳ" ]
        self.food_powerup_slow           = ["🐢", "◷" ]
        self.food_powerup_portal         = ["🌀", "α" ]
        self.food_powerup_brick          = ["🧱", "#" ]
        self.food_powerup_fast           = ["💨", "☇" ]
        self.food_powerup_clown           = ["🤡", "%" ]
        self.food_nerf_garlic           = ["❓", "Ç" ]
        self.food_powerup_tornado        = ["💫", "?" ]
        self.food_powerup_character_set  = ["💱", "X" ]
        self.food_powerup_gun              =["🔫", "ö" ]
        self.food_default                = ["🍏", "@" ]
        self.food_default                = ["🍏", "@" ]
        

        self.eye                         = ["🏐", "¬" ]
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

        self.c = Canvas(33, 33)
        #self.c.render_test()
        
        game_self = self

        def o1_render_fun(self):
            #self.collidable = True
            if(self.direction == "right"): 
                x_summand = + 1
                y_summand = 0
            if(self.direction == "left"): 
                x_summand = - 1
                y_summand = 0
            if(self.direction == "up"): 
                x_summand = 0
                y_summand = - 1
            if(self.direction == "down"): 
                x_summand = 0
                y_summand = + 1

            # if(int(self.head.rendered_count) % 3 == 0): self.head.ascii_character = game_self.ascii_map.get_string_by_prop_name("snake_utf_8_head_1")
            # if(int(self.head.rendered_count) % 3 == 1): self.head.ascii_character = game_self.ascii_map.get_string_by_prop_name("snake_utf_8_head_2")
            # if(int(self.head.rendered_count) % 3 == 2): self.head.ascii_character = game_self.ascii_map.get_string_by_prop_name("snake_utf_8_head_3")

            child_objects_len = len(self.child_objects)

            for key, val in enumerate(self.child_objects):
                key = child_objects_len - (key+1)

                val = self.child_objects[key]
                val_before_in_array = self.child_objects[key-1]


                if val.name == "snake_utf_8_head":
                    continue
                
                #print("key: "+str(key)+" has point"+str(val.point_3d.x)+"|"+str(val.point_3d.y)+", get point" + str(val_before_in_array.point_3d.x)+"|"+str(val_before_in_array.point_3d.y))

                val.point_3d.x = val_before_in_array.point_3d.x
                val.point_3d.y = val_before_in_array.point_3d.y

            self.head.point_3d.x = (self.head.point_3d.x + x_summand) % game_self.c.width
            self.head.point_3d.y = (self.head.point_3d.y + y_summand) % game_self.c.width
            self.add_limb_called_tmp_ignore_collisions = False


        def snake_collision_function(self, obj, collision_with):
            if(obj == self.head):

                if(collision_with[0].name == "snake_utf_8_body"):
                    obj.game_over = True
                    if(self.add_limb_called_tmp_ignore_collisions == False):
                        game_self.end()
                        #game_self.end()
                
                if(collision_with[0].name == "game_utf_8_border"):
                    obj.game_over = True
                    game_self.end()
                
                if(collision_with[0].name == "food_default"):
                    random_position(collision_with[0])
                    self.add_limb(self)
                
                if(collision_with[0].name == "food_powerup_mushroom"):
                    random_position(collision_with[0])
                    for i in range(3):
                        self.add_limb(self)

                if(collision_with[0].name == "food_nerf_garlic"):
                    random_position(collision_with[0])
                    n = 2
                    i = 0
                    for o in self.child_objects:
                        if o.name != "snake_utf_8_head" and i < n:
                            i+=1
                            self.child_objects.remove(o)

                
                if(collision_with[0].name == "food_powerup_portal"):
                    for o in Object._instances:
                        if o.name == "food_powerup_portal" and o != collision_with[0]:
                            self.head.point_3d.x = o.point_3d.x
                            self.head.point_3d.y = o.point_3d.y

                
                if(collision_with[0].name == "food_powerup_fast"):
                    def snake_speedup(self, obj):
                        obj.speed = 1
                        
                    def snake_speedup_first(self, obj):
                        if(hasattr(obj, "_cached_speed") == False):
                            obj._cached_speed = obj.speed
                        
                    def snake_speedup_last(self, obj):
                        obj.speed = obj._cached_speed

                    temp_render_function = Temp_Render_Function(snake_speedup)
                    temp_render_function.render_function_firstcall = snake_speedup_first
                    temp_render_function.render_function_lastcall = snake_speedup_last
                    temp_render_function.rendered_count_limit = 20

                    self.temp_render_functions.append(temp_render_function)

                if(collision_with[0].name == "food_powerup_clown"):
                    for i in range(6):
                        self.add_limb(self)

                    def trf(self, obj):
                        #obj.head.name = "food_powerup_clown"
                        if(hasattr(obj.head, "_cached_ascii_character") == False):
                            obj.head._cached_ascii_character = obj.parent_class_instance.ascii_map.get_string_by_prop_name(obj.head.name)
                        obj.head.ascii_character = obj.parent_class_instance.ascii_map.get_string_by_prop_name("food_powerup_clown")

                    def trf_start(self, obj):
                        return False

                    def trf_end(self, obj):
                        obj.head._cached_ascii_character = obj.head.ascii_character
                            
                        return False

                    temp_render_function = Temp_Render_Function(trf)
                    temp_render_function.render_function_firstcall = trf_start
                    temp_render_function.render_function_lastcall = trf_end
                    temp_render_function.rendered_count_limit = 20

                    self.temp_render_functions.append(temp_render_function)
                    
                    
        self.snake = Object_Group(self)
        self.snake.name = "snake"
        self.snake.render_function = o1_render_fun
        self.snake.collision_function = snake_collision_function
        self.snake.speed = 0.4

        self.snake.point_3d.z = 2
        #add custom props
        self.snake.direction = "right"

        snake_head = Object(self.snake)
        snake_head.name = "snake_utf_8_head"
        snake_head.point_3d.x = 1
        snake_head.point_3d.y = 1
        snake_head.collidable = True

        self.snake.child_objects.append(snake_head)
        self.snake.head = snake_head

        def add_limb(self):
            self.add_limb_called_tmp_ignore_collisions = True
            snake_limb = Object(self)
            last = self.child_objects[-1]            
            snake_limb.point_3d.x = last.point_3d.x
            snake_limb.point_3d.y = last.point_3d.y
            snake_limb.name = "snake_utf_8_body"
            self.child_objects.append(snake_limb)

        self.snake.add_limb = add_limb

        # player2 two player twoplayer 2player player two
        self.snake2 = Object_Group(self)
        self.snake2.name = "snake2"
        self.snake2.render_function = o1_render_fun
        self.snake2.collision_function = snake_collision_function
        self.snake2.speed = 0.2

        self.snake2.point_3d.z = 2
        #add custom props
        self.snake2.direction = "right"

        snake_head = Object(self.snake2)
        snake_head.name = "snake_utf_8_head"
        snake_head.point_3d.x = 10
        snake_head.point_3d.y = 10
        snake_head.collidable = True

        self.snake2.child_objects.append(snake_head)
        self.snake2.head = snake_head
        self.snake2.add_limb = add_limb


        
        # def weird_face_walk(self):
        #     if((game_self.render_id * self.speed) % 1 != 0):
        #         return False
        #     self.point_3d.x = (self.point_3d.x + 1) % game_self.c.width
        #     self.point_3d.y = (self.point_3d.y + 0) % game_self.c.width
        #     print(self.point_3d.x)

        # self.weird_face = Object_Group(self)
        # self.weird_face.render_function = weird_face_walk

        # self.weird_face.name = "weird_face"
        # #add custom props
        # self.weird_face.direction = "right"
        # self.weird_face.speed = 0.2

        # weird_face_eye_left = Object(self.weird_face)
        # weird_face_eye_left.name = "eye"
        # weird_face_eye_left.point_3d = Point_3D(0,0,0) #relative to parent_class_instance position
        # self.weird_face.child_objects.append(weird_face_eye_left)

        # weird_face_mouth = Object(self.weird_face)
        # weird_face_mouth.name = "mouth"
        # weird_face_mouth.point_3d = Point_3D(1,0,0) #relative to parent_class_instance position
        # self.weird_face.child_objects.append(weird_face_mouth)

        # weird_face_eye_right = Object(self.weird_face)
        # weird_face_eye_right.name = "eye"
        # weird_face_eye_right.point_3d = Point_3D(2,0,0) #relative to parent_class_instance position
        # self.weird_face.child_objects.append(weird_face_eye_right)

        def random_position(self):
            self.point_3d.x = random.randint(0,game_self.c.width-1)
            self.point_3d.y = random.randint(0,game_self.c.height-1)

        
        def food_group_collision_function(self, obj ,collision_with):
            if(collision_with[0].name == "game_utf_8_border"):
                random_position(obj)
            if(collision_with[0].name == "snake_utf_8_head"):
                random_position(obj)

        def food_group_render_function(self):
            if game_self.render_id % random.randint(1,200) == 0: 

                food = Object(self)
                food.collidable = True
                food.rendered_count_limit = 10
                food.name = "food_powerup_clown"
                random_position(food)
                self.child_objects.append(food)


        self.food_group = Object_Group(self)
        self.food_group.name = "food"
        self.food_group.collision_function = food_group_collision_function
        self.food_group.render_function = food_group_render_function

        food = Object(self.food_group)
        food.collidable = True
        food.name = "food_default"
        random_position(food)
        self.food_group.child_objects.append(food)

        food = Object(self.food_group)
        food.collidable = True
        food.name = "food_powerup_mushroom"
        random_position(food)

        self.food_group.child_objects.append(food)

        food = Object(self.food_group)
        food.collidable = True
        food.name = "food_nerf_garlic"
        random_position(food)
        self.food_group.child_objects.append(food)

        food = Object(self.food_group)
        food.collidable = True
        food.name = "food_powerup_portal"
        random_position(food)
        self.food_group.child_objects.append(food)

        food = Object(self.food_group)
        food.collidable = True
        food.name = "food_powerup_portal"
        random_position(food)
        self.food_group.child_objects.append(food)


        food = Object(self.food_group)
        food.collidable = True
        food.name = "food_powerup_fast"
        random_position(food)
        self.food_group.child_objects.append(food)

    
        food = Object(self.food_group)
        food.collidable = True
        food.name = "food_powerup_clown"
        random_position(food)
        self.food_group.child_objects.append(food)

        def add_gun_shot(self):
            food = Object(self.food_group)
            food.collidable = True
            food.name = "food_powerup_gun"
            random_position(food)
            self.food_group.child_objects.append(food)


        self.food_group.add_gun_shot = add_gun_shot


        # def food_render_function(self):
        #     if(self.rendered_count % 100 == 0):
        #         self.random_position()
        # food.render_function = food_render_function

        self.walls = Object_Group(self)
        self.walls.name = "walls"

        for width_index in range(game_self.c.width):
            brick = Object(self.walls)
            self.walls.child_objects.append(brick)
            brick.name = "game_utf_8_border"
            brick.point_3d.x = width_index
            brick.point_3d.y = 0
            
            brick = Object(self.walls)
            self.walls.child_objects.append(brick)
            brick.name = "game_utf_8_border"
            brick.point_3d.x = width_index
            brick.point_3d.y = game_self.c.height - 1

            for height_index in range(game_self.c.height):
                brick = Object(self.walls)
                self.walls.child_objects.append(brick)
                brick.name = "game_utf_8_border"
                brick.point_3d.x = 0
                brick.point_3d.y = height_index
                
                brick = Object(self.walls)
                self.walls.child_objects.append(brick)
                brick.name = "game_utf_8_border"
                brick.point_3d.x = game_self.c.width - 1
                brick.point_3d.y = height_index


    def is_sudo(self): 
        if os.name == 'nt': 
            return True
        else: 
            return os.geteuid() == 0
            # try:
            #     os.rename('/etc/foo', '/etc/bar')
            #     return True
            # except IOError as e:
            #     if (e[0] == errno.EPERM):
            #         return True
            #         sys.exit("You need root permissions to do this, laterz!")


    def render(self): 
        
        self.render_id += 1
        print(self.render_id)

        self.c.clear_ascii_pixel_array(self.ascii_map.get_string_by_prop_name("game_black_pixel"))

        #for obj in gc.get_objects():
        for obj in Object._instances:

            speed = 1

            if hasattr(obj, "speed"):
                speed = obj.speed                 
            else: 
                if hasattr(obj, "parent_class_instance"): 
                    if hasattr(obj.parent_class_instance, "speed"):
                        speed = obj.parent_class_instance.speed   

            #self.collidable = False

            if((self.render_id * speed) % 1 == 0):

                # code for Object and Object_Group, destroy after rendered_count_limit reached, call callbacks etc
                
                if(obj.rendered_count > obj.rendered_count_limit & obj.rendered_count_limit != 0):
                    del obj
                    continue
                
                if(obj.render_function != None):
                    obj.render_function(obj)

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


                #continue if ObejctGroup 
                if isinstance(obj, Object_Group):
                    continue
                

                if obj.collidable == True :
                    # todo , collision detection collisiondetection detect collision, call callback on self.group_object.collision_function() (emit colision to 'parent')
                    for obj2 in gc.get_objects():
                        if isinstance(obj2, Object_Group):
                            continue

                        if isinstance(obj2, Object):
                            if obj2 == obj or obj2.rendered_count < 2: #ignore just spawned objects:
                                continue
                            if ((obj2.point_3d.x == obj.point_3d.x) & (obj2.point_3d.y == obj.point_3d.y)):
                                obj.collision_with.append(obj2)
                

                    if(len(obj.collision_with) > 0):
                        if(obj.parent_class_instance.collision_function != None):
                            # proxy collision function to parent 
                            obj.parent_class_instance.collision_function(obj.parent_class_instance, obj, obj.collision_with)
                        
                        #if(obj.collision_function != None):
                        #    obj.collision_function(obj,obj.collision_with)


            #continue if ObejctGroup 
            if isinstance(obj, Object_Group):
                continue

            # will search for ascii symbol in map or if not found return fallback 
            ascii_string = self.ascii_map.get_string_by_prop_name(obj.name)

            #ascii_string  can be overwritten by having the property ascii character
            if(hasattr(obj, "ascii_character")):
                ascii_string = getattr(obj, "ascii_character")

            # increment the rendered_count on object since it gets rendered
            obj.rendered_count += 1

            #draw relative to parent
            self.c.add_ascii(obj.parent_class_instance.point_3d.x + obj.point_3d.x, obj.parent_class_instance.point_3d.y + obj.point_3d.y, obj.point_3d.z, ascii_string)


    def end(self):
        self.running = False
        p1 = len(self.snake.child_objects)
        p2 = len(self.snake2.child_objects)

        if(len(list(filter(lambda x: x.name == "game_utf_8_border", self.snake.head.collision_with))) > 0):
            print("player 2(arrow keys) wins")
            print("player 1(wasd) collided with wall")
    
        if(len(list(filter(lambda x: x.name == "game_utf_8_border", self.snake2.head.collision_with))) > 0):
            print("player 1(wasd) wins")
            print("player 2(arrow keys) collided with wall")
        
        if(len(list(filter(lambda x: x.name == "snake_utf_8_body", self.snake.head.collision_with))) > 0):
            print("player 2(arrow keys) wins")
            print("player 1(wasd) collided with player 2 body")
    
        if(len(list(filter(lambda x: x.name == "snake_utf_8_body", self.snake2.head.collision_with))) > 0):
            print("player 1(wasd) wins")
            print("player 2(arrow keys) collided with player 1 body")
            
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

        
        self._instances.append(self)


class Object_Group(Object):
    def __init__(self, parent_class_instance):
        Object.__init__(self, parent_class_instance)
        self.child_objects = []        

class Canvas: 
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ascii_pixel_array = [" "] * (self.width*self.height)
        self.ascii_pixel_z_axis_arrays = [[],[],[]]

        """
        @param x int 
        @param y int 
        @param z int 
        """
    def add_ascii(self, x, y, z,  ascii):
        #print("add_ascii: " + str(x) + "|" + str(y) + "|" +str(z) + ", "+ ascii)
        array_index = self.get_array_index_by_x_y(x, y)
        self.ascii_pixel_z_axis_arrays[z].append([x,y,ascii])

    def draw_ascii(self, x, y, ascii):
        array_index = self.get_array_index_by_x_y(x, y)
        try:
            self.ascii_pixel_array[array_index] = ascii
        except IndexError as e:
            print("skipping index " + array_index + ": impossible to draw out of canvas")

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
        self.clear_terminal()
        print(render_string)

    # define our clear function 
    def clear_terminal(self): 
        #print("\n".join([""]*100))
        #print(chr(27) + "[2J")
        os.system('cls' if os.name == 'nt' else 'clear')
        #print("".join(["\n"]*10))
    def render_test(self):

        foo1 = ["🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐨","🐯","🦁","🐮","🐷","🐽","🐸","🐵","🙈","🙉","🙊","🐒","🐔","🐧","🐦","🐤","🐣","🐥","🦆","🦅","🦉","🦇","🐺","🐗","🐴","🦄","🐝","🐛","🦋","🐌","🐚","🐞","🐜","🕷","🕸","🐢","🐍","🦎","🦂","🦀","🦑","🐙","🦐","🐠","🐟","🐡","🐬","🦈","🐳","🐋","🐊","🐆","🐅","🐃","🐂","🐄","🦌","🐪","🐫","🐘","🦏","🦍","🐎","🐖","🐐","🐏","🐑","🐕","🐩","🐈","🐓","🦃","🕊","🐇","🐁","🐀","🐾","🐉","🐲","🌵","🎄","🌲","🌳","🌴","🌱","🌿","🍀","🎍","🎋","🍃","🍂","🍁","🍄","🌾","💐","🌷","🌹","🥀","🌻","🌼","🌸","🌺","🌎","🌍","🌏","🌕","🌖","🌗","🌘","🌑","🌒","🌓","🌔","🌚","🌝","🌞","🌛","🌜","🌙","💫","⭐️","🌟","✨","🔥","💥","🌤","⛅️","🌈","⛄️","💨","🌊","💧","💦","🦓","🦔","🦕"]

        foo = ["1", "$", "#", "%", "%", "¢", "@"]
        foo = foo1
        foo = ["🦔", "🦔"]

        for val in range(0, self.width*self.height):
            #self.ascii_pixel_array[val] = random.choice(foo)
            self.ascii_pixel_array[val] = foo[val%(len(foo)-1)]
            self.render()



game = Game()

def background():
    game.start()
    print("start")
    #c = Canvas(22, 22)
    #c.render_test()

def foreground():
    # init listeners 

    # while True:
    #     if keyboard.read_key() == "p":
    #         setattr(game.o1, "speed" , 0.5)        
    #     if keyboard.read_key() == "w":
    #         setattr(game.o1, "direction" , "up")
    #         continue
    #     if keyboard.read_key() == "s":
    #         setattr(game.o1, "direction" , "down")
    #     if keyboard.read_key() == "a":
    #         setattr(game.o1, "direction" , "left")
    #     if keyboard.read_key() == "d":
    #         setattr(game.o1, "direction" , "right")
    keyboard.on_press_key("v", lambda _:game.end())


    keyboard.on_press_key("w", lambda _:setattr(game.snake, "direction" , "up"))
    keyboard.on_press_key("s", lambda _:setattr(game.snake, "direction" , "down"))
    keyboard.on_press_key("a", lambda _:setattr(game.snake, "direction" , "left"))
    keyboard.on_press_key("d", lambda _:setattr(game.snake, "direction" , "right"))

    keyboard.on_press_key("space", lambda _:setattr(game.food_group.add_gun_shot, "direction" , "right"))



    keyboard.on_press_key("up", lambda _:setattr(game.snake2, "direction" , "up"))
    keyboard.on_press_key("down", lambda _:setattr(game.snake2, "direction" , "down"))
    keyboard.on_press_key("left", lambda _:setattr(game.snake2, "direction" , "left"))
    keyboard.on_press_key("right", lambda _:setattr(game.snake2, "direction" , "right"))

    def add_limbs():
        for i in range(5):
            game.snake.add_limb(game.snake)

    keyboard.on_press_key("l", lambda _:add_limbs())

    def toggle_style(): 
        if(game.ascii_map.name == "emojis"):
            setattr(game.ascii_map, "name" , "classic")
        else: 
            setattr(game.ascii_map, "name" , "emojis")


    keyboard.on_press_key("m", lambda _:toggle_style())
    # What you want to run in the foreground

b = threading.Thread(name='background', target=background)
f = threading.Thread(name='foreground', target=foreground)

b.start()
f.start()


