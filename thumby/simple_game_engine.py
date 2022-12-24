
# arrow controls paste the following into the javascript console, -> dev tools (f11) -> console
#  var o_keymap = {
#     "w":"up", 
#     "a":"left",
#     "s":"down", 
#     "d":"right",
#     "ArrowUp":"up", 
#     "ArrowLeft":"left",
#     "ArrowDown":"down", 
#     "ArrowRight":"right", 
# }
# document.addEventListener("keydown", function (e) {
#     console.log(e.key)
#     var s_direction = o_keymap[e.key]
#     console.log(s_direction)
#     var o = document.querySelector(".emulator_dpad_" + s_direction + "_btn")
#     eventFire(o, "mousedown")
#     window.setTimeout(function(){
#         eventFire(o, "mouseup")
#     }, 100)
# })
# function eventFire(el, etype){
#     if (el.fireEvent) {
#         el.fireEvent('on' + etype);
#     } else {
#         var evObj = document.createEvent('Events');
#         evObj.initEvent(etype, true, false);
#         el.dispatchEvent(evObj);
#     }
# }
import random
try: 
    import keyboard
    import cv2
    import numpy
except:
    print("module 'keyboard' not found, try installing it with: 'pip3 install keyboard'")
try: 
    import thumby
    b_thumby = True
except:
    b_thumby = False
    print("module 'thumby' not found, use the web IDE to develop for thumby!: https://code.thumby.us/'")

import time

import os


class O_point_2d:
    def __init__( self, 
        n_x, 
        n_y
    ):
        self.n_x, self.n_y = n_x, n_y # single line multi assignment should be faster


a_o_object2d = []
class O_object_2d:
    def __init__( self, 
        n_x_translation,
        n_y_translation, 
        b_auto_calc_translation = False
    ):
        self.b_auto_calc_translation = b_auto_calc_translation
        # self.o_point_2d_translation = O_point_2d(n_x_translation,n_y_translation)
        # self.o_point_2d_velocity = O_point_2d(0,0)
        # self.o_point_2d_acceleration = O_point_2d(0,0)

        self.a_point_2d_translation = bytearray([n_x_translation,n_y_translation])
        self.a_point_2d_velocity = bytearray([0,0])
        self.a_point_2d_acceleration = bytearray([0,0])
        # self.a_point_2d_translation = ([n_x_translation,n_y_translation])
        # self.a_point_2d_velocity = ([0,0])
        # self.a_point_2d_acceleration = ([0,0])

        a_o_object2d.append(self)
class O_game_object:
    def __init__( self, 
        s_name, 
        n_x, 
        n_y,
        f_render_function = None, 
        f_collision_function = None, 
    ):
        self.s_name = s_name
        self.a_o_object_2d = [
            O_object_2d(
                n_x, n_y
            )
        ] 
        
        self.f_render_function = f_render_function
        self.f_collision_function = f_collision_function

# class O_collision_map_object:
#     def __init__( 
#         self, 
#     ):
#         self.a_o_collision_object = []


class O_collision_object:
    def __init__( self,
        o_game_object,
        o_object_2d, 
    ):
        self.o_game_object = o_game_object
        self.o_object_2d = o_object_2d

class O_grid:
    def __init__(
        self, 
        n_pixel_width, 
        n_pixel_height
    ): 
        self.n_scale_x = 3
        self.n_scale_y = 3
        self.n_pixel_width = n_pixel_width
        self.n_pixel_height = n_pixel_height

        if(b_thumby): 
            self.n_pixel_width = 72
            self.n_pixel_height = 40
            self.n_bytes_sprite_fullscreen = thumby.display.width * 5
            self.a_n_byte = [0 for n in range(0, self.n_bytes_sprite_fullscreen)]

        self.n_width = int(self.n_pixel_width / self.n_scale_x)
        self.n_height = int(self.n_pixel_height / self.n_scale_y)
        self.a_a_b = self.f_a_a_b()
        # print(len(self.a_a_b))
        # exit()
    def f_set_pixel_fast(
        self,
        n_x, 
        n_y, 
        b_value
        ):
        if(
            n_x > thumby.display.width
            or 
            n_x < 0
            or 
            n_y > thumby.display.height
            or 
            n_y < 0 
        ): 
            return False
        
        n = int(n_y / 8) * 72
        n_bit = n_y % 8
        n_index = n + n_x
        n_byte_with_bit_set = 1 << n_bit
        if(b_value):
            n_byte = self.a_n_byte[n_index] | n_byte_with_bit_set
        else: 
            n_byte = self.a_n_byte[n_index] & ~(n_byte_with_bit_set)
            
        self.a_n_byte[n_index] = n_byte

    def f_a_a_b(self):
        a_a_b = []
        for n_index in range(0, self.n_pixel_width * self.n_pixel_height):
            n_x = n_index % self.n_pixel_width
            n_y = int(n_index / self.n_pixel_width)
            if(n_x == 0): 
                a = [] 
                a_a_b.append(a)
            a.append(False)
        return a_a_b

    def f_clear(self):
        if(b_thumby):
            self.a_n_byte = [0 for n in range(0, self.n_bytes_sprite_fullscreen)] 
            thumby.display.fill(0)
        else: 
            self.a_a_b = self.f_a_a_b()
    def f_set_cell(
        self, 
        n_x,
        n_y, 
        b
    ): 
        n_x = int(self.n_scale_x) * int(n_x)
        n_y = int(self.n_scale_y) * int(n_y)
        for n_y_2 in range(0, self.n_scale_y):
            for n_x_2 in range(0, self.n_scale_x):
                if(b_thumby):
                    # thumby.display.setPixel(n_x+n_x_2, n_y+n_y_2, 1) # very very slow , sprites are much faster
                    self.f_set_pixel_fast(n_x+n_x_2, n_y+n_y_2, int(b))
                else:
                    try:
                        self.a_a_b[n_y+n_y_2][n_x+n_x_2] = b
                    except:
                        pass
                    # print(self.a_a_b[n_y+n_y_2][n_x+n_x_2])

        # exit()

    def f_render(self):
        # print("f_render called")
        if(b_thumby):
            a_bytes = bytearray(self.a_n_byte)
            o_sprite = thumby.Sprite(72, 40, a_bytes, 0, 0)
            thumby.display.drawSprite(o_sprite)
            thumby.display.update()
        else:
            a_img = numpy.zeros((self.n_pixel_height,self.n_pixel_width,1), numpy.uint8)
            s = ""
            n_y = 0
            a_s_line = []
            for a_y in self.a_a_b:
                s = ""
                n_x = 0
                for b_x in a_y:
                    if(b_x):
                        s+="x"
                        a_img[n_y][n_x] = 0
                    else: 
                        s+="-"
                        a_img[n_y][n_x] = 255
                    n_x += 1 
                n_y += 1
                a_s_line.append(s)
            
            cv2.imshow("asdf", a_img)
            cv2.waitKey(1)
            # print(a_s_line)

            print("\n".join(a_s_line))

class O_game:
    def __init__(
        self
    ): 
        self.n_fps = 30
        self.o_grid = O_grid(
            72, 
            40
        )
        # self.a_o_collision_map_object = [] 
        # self.o_collision_map = {}
        # self.o_collision_map_with_collisions = {}
        self.a_o_game_object = []
        self.b_keydown_once = False
        self.b_thumby = True
        if(b_thumby):
            thumby.display.setFPS(self.n_fps)
            
        def f_render_function_o_snake(
            self, 
            o_game
        ):
            o_object_2d_head = self.a_o_object_2d[0]
            n_velocity = 1
            a_point_2d_velocity = o_object_2d_head.a_point_2d_velocity
            if(o_game.f_b_button_pressed("up")):
                a_point_2d_velocity[0] = 0
                a_point_2d_velocity[1] = -n_velocity
            
            if(o_game.f_b_button_pressed("left")):
                a_point_2d_velocity[0] = -n_velocity
                a_point_2d_velocity[1] = 0
            
            if(o_game.f_b_button_pressed("down")):
                a_point_2d_velocity[0] = 0
                a_point_2d_velocity[1] = n_velocity    
            
            if(o_game.f_b_button_pressed("right")):
                a_point_2d_velocity[0] = n_velocity
                a_point_2d_velocity[1] = 0

            n_i_reversed = len(self.a_o_object_2d) -1
            while(n_i_reversed > 0):
                # since the snake speed is slower than 1 ( 0.1) the translation will only change every 10th render function
                if(n_i_reversed > 0):
                    o_object_2d_1 =  self.a_o_object_2d[n_i_reversed]
                    o_object_2d_2 =  self.a_o_object_2d[n_i_reversed-1]
                    o_object_2d_1.a_point_2d_translation[0] = o_object_2d_2.a_point_2d_translation[0]
                    o_object_2d_1.a_point_2d_translation[1] = o_object_2d_2.a_point_2d_translation[1]
                
                n_i_reversed-=1
        
        # def f_collision_function_o_snake(
        #     o_game_object,
        #     o_collision_map_object
        #     ):
        #         a_o_game_object_food = [
        #             o for o in o_collision_map_object.a_o_collision_object
        #             if (o.o_game_object.s_name == "food")
        #         ]

        #         if(len(a_o_game_object_food) > 0):
        #             # add limb
        #             o_game_object.a_o_object_2d.append(
        #                 O_object_2d(
        #                     o_game_object.a_o_object_2d[len(o_game_object.a_o_object_2d)-1].o_point_2d_translation.n_x,
        #                     o_game_object.a_o_object_2d[len(o_game_object.a_o_object_2d)-1].o_point_2d_translation.n_y
        #                 )
        #             )

                
        o_snake = O_game_object(
            "snake",
            10,
            10,
            f_render_function_o_snake, 
            # f_collision_function_o_snake
        )
        self.o_snake = o_snake
        for n in range(0,50):
            o_snake.a_o_object_2d.append(
                O_object_2d(
                    0,0
                )
            )
        o_snake.a_o_object_2d[0].b_auto_calc_translation = True
        self.a_o_game_object.append(o_snake)

        def f_create_food():
            # def f_collision_function_o_food(o_game_object, o_collision_map_object):
            #     a_o_game_object_snake = [
            #         o for o in o_collision_map_object.a_o_collision_object
            #         if (o.o_game_object.s_name == "snake")
            #     ]
            #     # console.log(a_o_game_object_snake)
            #     if(len(a_o_game_object_snake) > 0):
            #         n_index = self.a_o_game_object.index(o_game_object)
            #         if (n_index > -1): #// only splice array when item is found
            #             self.a_o_game_object.pop(n_index); #// 2nd parameter means remove one item only
            #         f_create_food()
                
                
            o_food = O_game_object(
                "food",
                int(random.uniform(0, 1)*self.o_grid.n_width),
                int(random.uniform(0, 1)*self.o_grid.n_height), 
                # lambda self, o_game: True, 
                # f_collision_function_o_food
            )
            self.a_o_game_object.append(o_food)
        

        f_create_food()

    def f_render(self):
        while(1):# while(1) should be faster than while(True)
            self.o_grid.f_clear()

            # print("f_render called")
            # self.a_o_collision_map_object = []
            # self.o_collision_map = {}

            # print(self.a_o_game_object)
                        
            for o_object_2d in a_o_object2d:
                a_point_2d_translation = o_object_2d.a_point_2d_translation
                if(o_object_2d.b_auto_calc_translation == True):
                    a_point_2d_velocity = o_object_2d.a_point_2d_velocity
                    a_point_2d_acceleration = o_object_2d.a_point_2d_acceleration
                    a_point_2d_velocity[0] += a_point_2d_acceleration[0]
                    a_point_2d_velocity[1] += a_point_2d_acceleration[1]
                    n_new_x = a_point_2d_translation[0] + a_point_2d_velocity[0]
                    n_new_y = a_point_2d_translation[1] + a_point_2d_velocity[1]
                    a_point_2d_translation[0] = n_new_x
                    a_point_2d_translation[1] = n_new_y
                self.o_grid.f_set_cell(
                    a_point_2d_translation[0],
                    a_point_2d_translation[1],
                    True
                )

            o_object_2d_head = self.o_snake.a_o_object_2d[0]
            n_velocity = 1
            a_point_2d_velocity = o_object_2d_head.a_point_2d_velocity
            if(o_game.f_b_button_pressed("up")):
                a_point_2d_velocity[0] = 0
                a_point_2d_velocity[1] = -n_velocity
            
            if(o_game.f_b_button_pressed("left")):
                a_point_2d_velocity[0] = -n_velocity
                a_point_2d_velocity[1] = 0
            
            if(o_game.f_b_button_pressed("down")):
                a_point_2d_velocity[0] = 0
                a_point_2d_velocity[1] = n_velocity    
            
            if(o_game.f_b_button_pressed("right")):
                a_point_2d_velocity[0] = n_velocity
                a_point_2d_velocity[1] = 0

            n_i_reversed = len(self.o_snake.a_o_object_2d) -1
            while(n_i_reversed > 0):
                # since the snake speed is slower than 1 ( 0.1) the translation will only change every 10th render function
                if(n_i_reversed > 0):
                    o_object_2d_1 =  self.o_snake.a_o_object_2d[n_i_reversed]
                    o_object_2d_2 =  self.o_snake.a_o_object_2d[n_i_reversed-1]
                    o_object_2d_1.a_point_2d_translation[0] = o_object_2d_2.a_point_2d_translation[0]
                    o_object_2d_1.a_point_2d_translation[1] = o_object_2d_2.a_point_2d_translation[1]
                
                n_i_reversed-=1
            # for o_game_object in self.a_o_game_object:
            #     if o_game_object.f_render_function != None:
            #         o_game_object.f_render_function(o_game_object, self)


                    # s_prop = f"a_{int(n_new_x)}_{int(n_new_y)}"
                    # if s_prop not in self.o_collision_map:
                    #     o_collision_map_object = O_collision_map_object()
                    #     self.o_collision_map[s_prop] = o_collision_map_object
                    #     # setattr(self.o_collision_map, s_prop, o_collision_map_object)
                    # else:
                    #     o_collision_map_object = self.o_collision_map[s_prop]
                    
                    # o_collision_map_object.a_o_collision_object.append(
                    #     O_collision_object(
                    #         o_game_object, 
                    #         o_object_2d
                    #     )
                    # )
                    # if(len(o_collision_map_object.a_o_collision_object) > 1):
                    #     self.a_o_collision_map_object.append(o_collision_map_object)
            
            # a_o_object_2d_treated = []
            # a_a_o_object_2d_collsions = []

            # for o_game_object in self.a_o_game_object:
            #     for o_object_2d in o_game_object.a_o_object_2d:
            #         if o_object_2d in a_o_object_2d_treated:
            #             continue

            #         n_x = o_object_2d.o_point_2d_translation.n_x
            #         n_y = o_object_2d.o_point_2d_translation.n_y

            #         a_o_object_2d_same_translation = [
            #             [
            #                     o_o2d for o_o2d in ogo.a_o_object_2d 
            #                     if(
            #                         int(o_o2d.o_point_2d_translation.n_x) == n_new_x
            #                         and
            #                         int(o_o2d.o_point_2d_translation.n_y) == n_new_y
            #                     )
            #                 ]
            #             for ogo in self.a_o_game_object
            #             if(
            #                 len([
            #                     o_o2d for o_o2d in ogo.a_o_object_2d 
            #                     if(
            #                         int(o_o2d.o_point_2d_translation.n_x) == n_new_x
            #                         and
            #                         int(o_o2d.o_point_2d_translation.n_y) == n_new_y
            #                     )
            #                 ]) > 0
            #             )
            #         ]
            #         a_o_object_2d_same_translation_flattend = [x for xs in a_o_object_2d_same_translation for x in xs]
            #         # print(a_o_object_2d_same_translation)
            #         # exit()
            #         a_o_object_2d_treated  = a_o_object_2d_treated + a_o_object_2d_same_translation_flattend
            #         if(len(a_o_object_2d_same_translation) > 1):
            #             a_a_o_object_2d_collsions.append(a_o_object_2d_same_translation_flattend)
            #             print(a_o_object_2d_same_translation)
            #             exit()
                
            # for o_collision_map_object in self.a_o_collision_map_object:
            #     for o_collision_object in o_collision_map_object.a_o_collision_object:
            #         # print(o_collision_object.o_game_object.f_collision_function)
            #         # exit()
            #         if(o_collision_object.o_game_object.f_collision_function != None):
            #             o_collision_object.o_game_object.f_collision_function(
            #                 o_collision_object.o_game_object,
            #                 o_collision_map_object
            #             )
                
            

            if(self.b_thumby == False):
                # print("render")
                # for n_i in range(0, 10):
                    # print("a")
                os.system('cls' if os.name == 'nt' else 'clear')

            # this is better for the game logic since the translation can be changed in the render or collision function
            # before it is "rendered" but to improve speed for thumby i set the cell right after the calculation of translation
            # for o_game_object in self.a_o_game_object:
            #     for o_object_2d in o_game_object.a_o_object_2d:
            #         self.o_grid.f_set_cell(
            #             o_object_2d.o_point_2d_translation.n_x,
            #             o_object_2d.o_point_2d_translation.n_y, 
            #             True
            #         )

            self.o_grid.f_render()
        
            time.sleep(1/self.n_fps)
        # self.f_render() # recursion is not so good in python 

    def f_b_button_pressed(
        self, 
        s_button_name
    ):
        if(self.b_thumby):
            # print(s_button_name)
            return getattr(thumby, "button"+s_button_name[0].upper()).pressed()
        else:
            return keyboard.is_pressed(s_button_name)

    def f_start(self):
        self.f_render()


o_game = O_game()
o_game.b_thumby = b_thumby
o_game.f_start()