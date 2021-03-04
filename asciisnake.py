from os import system, name 
from time import sleep 
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

        self.running = False

        self.ascii_map_active = self.ascii_map_emojis

        self.c = Canvas(22, 22)
        #self.c.render_test()
        game_self = self
        def o1_render_fun(self):
            if(self.direction == "right"): 
                x_summand = + 1*self.speed
                y_summand = 0
            if(self.direction == "left"): 
                x_summand = - 1*self.speed
                y_summand = 0
            if(self.direction == "up"): 
                x_summand = 0
                y_summand = - 1*self.speed
            if(self.direction == "down"): 
                x_summand = 0
                y_summand = + 1*self.speed

            if(int(self.rendered_count*self.speed) % 3 == 0): self.ascii_character = "🌎"
            if(int(self.rendered_count*self.speed) % 3 == 1): self.ascii_character = "🌍"
            if(int(self.rendered_count*self.speed) % 3 == 2): self.ascii_character = "🌏"

            if(int(self.rendered_count*self.speed) % 3 == 0): self.ascii_character = "🙈"
            if(int(self.rendered_count*self.speed) % 3 == 1): self.ascii_character = "🙉"
            if(int(self.rendered_count*self.speed) % 3 == 2): self.ascii_character = "🙊"

            self.point_3d.x = (self.point_3d.x + x_summand) % game_self.c.width
            self.point_3d.y = (self.point_3d.y + y_summand) % game_self.c.width

        #group object
        self.snake = ObjectGroup("snake")
        def add_limb(self)
            limb_object = Object(Point_3D(0,0,0), "snake_utf_8_head", 1, 0, 0,  None, None)
            self.children_objects.add(limb_object)

        # actual objects
        self.o1 = Object(Point_3D(0,0,0), "snake_utf_8_head", 1, 0, 0,  o1_render_fun, lambda a : 1+1)
        self.o1.speed = 0.1
        self.o1.direction = "right"

    def render(self): 
        
        self.c.clear_ascii_pixel_array(self.ascii_map_active.game_black_pixel)

        for obj in gc.get_objects():
            if isinstance(obj, Object):
                obj.rendered_count = obj.rendered_count+1
                if(obj.rendered_count > obj.rendered_count_limit & obj.rendered_count_limit != 0):
                    del obj
                    continue

                obj.render_function(obj)
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

class ObjectGroup():
    def __init__(self, name, children_objects = None):
        self.name = name
        self.children_objects = children_objects

class Object: 
    def __init__(self, object_group,  point_3d, name, co_existance_limit, rendered_count, rendered_count_limit, render_function, collision_function):
        # 'parent' object
        self.object_group = object_group, 
        #  point
        self.point_3d = point_3d
        # snake, item, enemy... 
        self.name = name
        # defines how many with the same name can exists at the same time
        self.co_existance_limit = co_existance_limit
        # on every render this gets incremented
        self.rendered_count = rendered_count
        # when the render_count has reached the render_count_limit, the object gets destroyed
        self.rendered_count_limit = rendered_count_limit
        # a callback which is getting executed on every render 
        self.render_function = render_function
        # a callback which is getting exectued when the object collides with other objects
        self.collision_function = collision_function

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
        self.clear_terminal()
        render_string = ""
        for key, val in enumerate(self.ascii_pixel_array):
            key = key + 1
            if key % self.width == 0:
                render_string += val
                render_string += "\n"
            else:
                render_string += val
        
        print(render_string)
        sleep(0.016)

    # define our clear function 
    def clear_terminal(self): 
    
        # for windows 
        if name == 'nt': 
            _ = system('cls') 
    
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear') 

    def render_test(self):

        foo = ["🐶"
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
        ,"🐿"
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
        ,"🌥"
        ,"🌦"
        ,"🌈"
        ,"🌧"
        ,"⛈"
        ,"🌩"
        ,"🌨"
        ,"⛄️"
        ,"🌬"
        ,"💨"
        ,"🌪"
        ,"🌫"
        ,"🌊"
        ,"💧"
        ,"💦"
        ,"🦓"
        ,"🦔"
        ,"🦕"]

        
        for val in range(0, self.width*self.height):
            self.clear_terminal()
            #self.ascii_pixel_array[val] = random.choice(foo)
            self.ascii_pixel_array[val] = foo[val%(len(foo)-1)]
            self.render()
            sleep(0.001)



game = Game()

def background():
    game.start()

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

    keyboard.on_press_key("w", lambda _:setattr(game.o1, "direction" , "up"))
    keyboard.on_press_key("s", lambda _:setattr(game.o1, "direction" , "down"))
    keyboard.on_press_key("a", lambda _:setattr(game.o1, "direction" , "left"))
    keyboard.on_press_key("d", lambda _:setattr(game.o1, "direction" , "right"))


    keyboard.on_press_key("m", lambda _:setattr(game, "ascii_map_active" , game.ascii_map_oldschool))



    # What you want to run in the foreground

b = threading.Thread(name='background', target=background)
f = threading.Thread(name='foreground', target=foreground)

b.start()
f.start()


