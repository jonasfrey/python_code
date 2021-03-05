import os
import time  
import random
import gc 
import keyboard
import threading

class Ascii_Map:
    def __init__(self,
        name = "emojis",
        game_white_pixel = "🌑",
        game_black_pixel = "🌑",
        canvas_white_pixel = "🌑",
        canvas_black_pixel = "🌑",
        game_utf_8_border = "🧱",
        snake_utf_8_head = "🌝",
        snake_utf_8_body = "🌕",
        snake_utf_8_tail = "🌕",
        food_powerup_mushroom = "🍄",
        food_powerup_slow = "🐢",
        food_powerup_portal = "🌀",
        food_powerup_brick = "🧱",
        food_powerup_fast = "💨",
        food_powerup_tornado = "💫",
        food_powerup_character_set = "💱",
        food_default = "🍏",
        fallback = "🌑",
    ):
        self.name = name
        self.game_white_pixel = game_white_pixel
        self.game_black_pixel = game_black_pixel
        self.canvas_white_pixel = canvas_white_pixel
        self.canvas_black_pixel = canvas_black_pixel
        self.game_utf_8_border = game_utf_8_border
        self.snake_utf_8_head = snake_utf_8_head
        self.snake_utf_8_body = snake_utf_8_body
        self.snake_utf_8_tail = snake_utf_8_tail
        self.food_powerup_mushroom = food_powerup_mushroom
        self.food_powerup_slow = food_powerup_slow
        self.food_powerup_portal = food_powerup_portal
        self.food_powerup_brick = food_powerup_brick
        self.food_powerup_fast = food_powerup_fast
        self.food_powerup_tornado = food_powerup_tornado
        self.food_powerup_character_set = food_powerup_character_set
        self.food_default = food_default
        self.fallback = fallback

class Game: 
    def __init__(self):
        self.ascii_map_emojis = Ascii_Map()
        self.ascii_map_oldschool = Ascii_Map()
        self.ascii_map_oldschool.name = "oldschool"
        self.ascii_map_oldschool.game_white_pixel = " " 
        self.ascii_map_oldschool.game_black_pixel = " " 
        self.ascii_map_oldschool.canvas_white_pixel = " " 
        self.ascii_map_oldschool.canvas_black_pixel = " " 
        self.ascii_map_oldschool.game_utf_8_border = "#" 
        self.ascii_map_oldschool.snake_utf_8_head = "O"
        self.ascii_map_oldschool.snake_utf_8_body = "o"
        self.ascii_map_oldschool.snake_utf_8_tail = "9"
        self.ascii_map_oldschool.food_powerup_mushroom = "Ͳ"
        self.ascii_map_oldschool.food_powerup_slow = "◷"
        self.ascii_map_oldschool.food_powerup_portal = "α"
        self.ascii_map_oldschool.food_powerup_brick = "#"
        self.ascii_map_oldschool.food_powerup_fast = "☇"
        self.ascii_map_oldschool.food_powerup_character_set = "?"
        self.ascii_map_oldschool.food_powerup_tornado = "X"
        self.ascii_map_oldschool.food_default = "@"
        self.ascii_map_oldschool.fallback = " "

        if self.is_sudo() != True:
            print("run with sudo ")    
            exit()
        
        self.running = False
        self.render_id = 0

        self.ascii_map_active = self.ascii_map_emojis

        self.c = Canvas(22, 22)
        #self.c.render_test()
        
        game_self = self

        def o1_render_fun(self):
            #self.collidable = False
            if((game_self.render_id * self.parent_class_instance.speed) % 1 != 0):
                return False

            #self.collidable = True
            if(self.parent_class_instance.direction == "right"): 
                x_summand = + 1
                y_summand = 0
            if(self.parent_class_instance.direction == "left"): 
                x_summand = - 1
                y_summand = 0
            if(self.parent_class_instance.direction == "up"): 
                x_summand = 0
                y_summand = - 1
            if(self.parent_class_instance.direction == "down"): 
                x_summand = 0
                y_summand = + 1

            if(int(self.rendered_count) % 3 == 0): self.ascii_character = "🌎"
            if(int(self.rendered_count) % 3 == 1): self.ascii_character = "🌍"
            if(int(self.rendered_count) % 3 == 2): self.ascii_character = "🌏"

            if(int(self.rendered_count) % 3 == 0): self.ascii_character = "🙈"
            if(int(self.rendered_count) % 3 == 1): self.ascii_character = "🙉"
            if(int(self.rendered_count) % 3 == 2): self.ascii_character = "🙊"

            child_objects_len = len(self.parent_class_instance.child_objects)

            for key, val in enumerate(self.parent_class_instance.child_objects):
                key = child_objects_len - (key+1)


                val = self.parent_class_instance.child_objects[key]
                if val.name == "snake_utf_8_head":
                    continue

                val_before_in_array = self.parent_class_instance.child_objects[key-1]

                val.point_3d.x = val_before_in_array.point_3d.x
                val.point_3d.y = val_before_in_array.point_3d.y

        
            self.point_3d.x = (self.point_3d.x + x_summand) % game_self.c.width
            self.point_3d.y = (self.point_3d.y + y_summand) % game_self.c.width

        def snake_head_collision_function(self,collision_with):
            if(collision_with[0].name == "snake_utf_8_body"):
                game_self.end()
            if(collision_with[0].name == "food_default"):
                self.parent_class_instance.add_limb(self.parent_class_instance)


        self.snake = ObjectGroup(self)
        self.snake.name = "snake"
        #add custom props
        self.snake.direction = "right"
        self.snake.speed = 0.2

        snake_head = Object(self.snake)
        snake_head.name = "snake_utf_8_head"
        snake_head.render_function = o1_render_fun
        snake_head.collision_function = snake_head_collision_function
        snake_head.collidable = True
        self.snake.child_objects.append(snake_head)

        def add_limb(self):
            snake_limb = Object(self)
            snake_limb.name = "snake_utf_8_body"
            self.child_objects.append(snake_limb)

        self.snake.add_limb = add_limb



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
        
        self.c.clear_ascii_pixel_array(self.ascii_map_active.game_black_pixel)

        for obj in gc.get_objects():
            if isinstance(obj, Object):
                # code for Object and ObjectGroup, destroy after rendered_count_limit reached, call callbacks etc
                obj.rendered_count = obj.rendered_count+1
                if(obj.rendered_count > obj.rendered_count_limit & obj.rendered_count_limit != 0):
                    del obj
                    continue
                
                if(obj.render_function != None):
                    obj.render_function(obj)

                #continue if ObejctGroup 
                if isinstance(obj, ObjectGroup):
                    continue
                

                if obj.collidable == True:
                    obj.collision_with = []
                    # todo , collision detection collisiondetection detect collision, call callback on self.group_object.collision_function() (emit colision to 'parent')
                    for obj2 in gc.get_objects():
                        if isinstance(obj2, ObjectGroup):
                            continue

                        if isinstance(obj2, Object):
                            if obj2 == obj:
                                continue
                            if ((obj2.point_3d.x == obj.point_3d.x) & (obj2.point_3d.y == obj.point_3d.y)):
                                obj.collision_with.append(obj2)

                
                    if(len(obj.collision_with) > 0):
                        if(obj.collision_function != None):
                            obj.collision_function(obj,obj.collision_with)


                if(hasattr(self.ascii_map_active, obj.name) == False):
                    ascii_string = self.ascii_map_active.fallback
                else:
                    ascii_string = getattr(self.ascii_map_active, obj.name)

                if(hasattr(obj, "ascii_character")):
                    ascii_string = getattr(obj, "ascii_character")
                
                self.c.draw_ascii(obj.point_3d.x, obj.point_3d.y, ascii_string)


    def end(self):
        self.running = False

    def start(self):
        self.running = True
        
        while self.running:
            self.render()
            self.c.render()

class Point_3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Object: 
    def __init__(self, parent_class_instance):
        # 'parent' object
        self.parent_class_instance = parent_class_instance
        #  point
        self.point_3d = Point_3D(0,0,0)
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

        # a callback which is getting exectued when the object collides with other objects
        #optional , by default None 
        self.collision_function = None


class ObjectGroup(Object):
    def __init__(self, parent_class_instance):
        Object.__init__(self, parent_class_instance)
        self.child_objects = []


class Canvas: 
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ascii_pixel_array = [" "] * (self.width*self.height)

    def draw_ascii(self, x, y, ascii):
        array_index = self.get_array_index_by_x_y(x, y)
        self.ascii_pixel_array[array_index] = ascii

    def get_array_index_by_x_y(self, x, y):
        index = int(y) * self.width + int(x)
        return index 

    def get_x_y_by_array_index(self, array_index): 
        y = int(array_index/self.width)
        x = int(array_index % self.width)
        return Point_3D(x,y)

    def clear_ascii_pixel_array(self, black_pixel = " "):
        self.ascii_pixel_array =  [black_pixel] * (self.width*self.height)
    
    def render(self):
        render_string = ""
        for key, val in enumerate(self.ascii_pixel_array):
            if (key+1) % self.width == 0:
                render_string += val
                render_string += "\n"
            else:
                render_string += val
        
        time.sleep(0.016) # 1000(ms)/60(fps) => 0.016 ms sleep
        self.clear_terminal()
        print(render_string)

    # define our clear function 
    def clear_terminal(self): 
        #print("\n".join([""]*100))
        #print(chr(27) + "[2J")
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_test(self):

        foo1 = ["🐶"
        ,"🐱"
        ,"🐭"
        ,"🐹"
        ,"🐰"
        ,"🦊"
        ,"🐻"
        ,"🐼"
        ,"🐨"
        ,"🐯"
        ,"🦁"
        ,"🐮"
        ,"🐷"
        ,"🐽"
        ,"🐸"
        ,"🐵"
        ,"🙈"
        ,"🙉"
        ,"🙊"
        ,"🐒"
        ,"🐔"
        ,"🐧"
        ,"🐦"
        ,"🐤"
        ,"🐣"
        ,"🐥"
        ,"🦆"
        ,"🦅"
        ,"🦉"
        ,"🦇"
        ,"🐺"
        ,"🐗"
        ,"🐴"
        ,"🦄"
        ,"🐝"
        ,"🐛"
        ,"🦋"
        ,"🐌"
        ,"🐚"
        ,"🐞"
        ,"🐜"
        ,"🕷"
        ,"🕸"
        ,"🐢"
        ,"🐍"
        ,"🦎"
        ,"🦂"
        ,"🦀"
        ,"🦑"
        ,"🐙"
        ,"🦐"
        ,"🐠"
        ,"🐟"
        ,"🐡"
        ,"🐬"
        ,"🦈"
        ,"🐳"
        ,"🐋"
        ,"🐊"
        ,"🐆"
        ,"🐅"
        ,"🐃"
        ,"🐂"
        ,"🐄"
        ,"🦌"
        ,"🐪"
        ,"🐫"
        ,"🐘"
        ,"🦏"
        ,"🦍"
        ,"🐎"
        ,"🐖"
        ,"🐐"
        ,"🐏"
        ,"🐑"
        ,"🐕"
        ,"🐩"
        ,"🐈"
        ,"🐓"
        ,"🦃"
        ,"🕊"
        ,"🐇"
        ,"🐁"
        ,"🐀"
        ,"🐾"
        ,"🐉"
        ,"🐲"
        ,"🌵"
        ,"🎄"
        ,"🌲"
        ,"🌳"
        ,"🌴"
        ,"🌱"
        ,"🌿"
        ,"🍀"
        ,"🎍"
        ,"🎋"
        ,"🍃"
        ,"🍂"
        ,"🍁"
        ,"🍄"
        ,"🌾"
        ,"💐"
        ,"🌷"
        ,"🌹"
        ,"🥀"
        ,"🌻"
        ,"🌼"
        ,"🌸"
        ,"🌺"
        ,"🌎"
        ,"🌍"
        ,"🌏"
        ,"🌕"
        ,"🌖"
        ,"🌗"
        ,"🌘"
        ,"🌑"
        ,"🌒"
        ,"🌓"
        ,"🌔"
        ,"🌚"
        ,"🌝"
        ,"🌞"
        ,"🌛"
        ,"🌜"
        ,"🌙"
        ,"💫"
        ,"⭐️"
        ,"🌟"
        ,"✨"
        ,"🔥"
        ,"💥"
        ,"🌤"
        ,"⛅️"
        ,"🌈"
        ,"⛄️"
        ,"💨"
        ,"🌊"
        ,"💧"
        ,"💦"
        ,"🦓"
        ,"🦔"
        ,"🦕"]

        foo = ["{", "*", "1", "$", "#", "%", "%", "¢", "@"]
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

    def add_limbs():
        game.snake.add_limb(game.snake)
        game.snake.add_limb(game.snake)
        game.snake.add_limb(game.snake)
        game.snake.add_limb(game.snake)
        game.snake.add_limb(game.snake)


    keyboard.on_press_key("l", lambda _:add_limbs())

    def toggle_style(): 
        if(game.ascii_map_active == game.ascii_map_oldschool):
            setattr(game, "ascii_map_active" , game.ascii_map_emojis)
        else: 
            setattr(game, "ascii_map_active" , game.ascii_map_oldschool)

    keyboard.on_press_key("m", lambda _:toggle_style())
    # What you want to run in the foreground

b = threading.Thread(name='background', target=background)
f = threading.Thread(name='foreground', target=foreground)

b.start()
f.start()


