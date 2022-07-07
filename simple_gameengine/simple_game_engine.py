
import random
import keyboard
import time
import os

class O_point_2d:
    def __init__( self, 
        n_x, 
        n_y
    ):
        self.n_x = n_x
        self.n_y = n_y

class O_object_2d:
    def __init__( self, 
        n_x_translation,
        n_y_translation
    ):
        self.o_point_2d_translation = O_point_2d(n_x_translation,n_y_translation)
        self.o_point_2d_velocity = O_point_2d(0,0)
        self.o_point_2d_acceleration = O_point_2d(0,0)
    
class O_game_object:
    def __init__( self, 
        s_name, 
        n_x, 
        n_y,
        f_render_function = lambda self: True, 
        f_collision_function = lambda o_collision_map_object: True, 
    ):
        self.s_name = s_name
        self.a_o_object_2d = [
            O_object_2d(
                n_x, n_y
            )
        ] 
        
        self.f_render_function = f_render_function
        self.f_collision_function = f_collision_function

class O_collision_map_object:
    def __init__( 
        self, 
    ):
        self.a_o_collision_object = []


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
        n_width, 
        n_height
    ): 
        self.n_width = n_width
        self.n_height = n_height
        self.a_a_b = []
        self.f_clear()

    def f_clear(self):
        for n_y in range(0, self.n_height):
            a_row = []
            for n_x in range(0, self.n_width):
                a_row.append(False)

            self.a_a_b.append(a_row)


    def f_render(self):
        s = ""
        for a_y in self.a_a_b:
            for b_x in a_y: 
                if(b_x):
                    s+="x"
                else: 
                    s+=" "
            s+= "\n"
        print(s)

class O_game:
    def __init__(
        self
    ): 
        self.n_fps = 1
        self.o_grid = O_grid(
            20, 
            20
        )
        self.a_o_collision_map_object = [] 
        self.o_collision_map = {}
        self.o_collision_map_with_collisions = {}
        self.a_o_game_object = []
        self.b_keydown_once = False
        def f_render_function_o_snake(self):
                o_object_2d_head = self.a_o_object_2d[0]

                if(keyboard.is_pressed("up")):
                    o_object_2d_head.o_point_2d_velocity.n_x = 0
                    o_object_2d_head.o_point_2d_velocity.n_y = -1
                
                if(keyboard.is_pressed("left")):
                    o_object_2d_head.o_point_2d_velocity.n_x = -1
                    o_object_2d_head.o_point_2d_velocity.n_y = 0
                
                if(keyboard.is_pressed("down")):
                    o_object_2d_head.o_point_2d_velocity.n_x = 0
                    o_object_2d_head.o_point_2d_velocity.n_y = 1    
                
                if(keyboard.is_pressed("right")):
                    o_object_2d_head.o_point_2d_velocity.n_x = 1
                    o_object_2d_head.o_point_2d_velocity.n_y = 0

                n_i_reversed = len(self.a_o_object_2d) -1
                while(n_i_reversed > 0):
                    if(n_i_reversed > 0):
                        o_object_2d_1 =  self.a_o_object_2d[n_i_reversed]
                        o_object_2d_2 =  self.a_o_object_2d[n_i_reversed-1]
                        o_object_2d_1.o_point_2d_translation.n_x = o_object_2d_2.o_point_2d_translation.n_x
                        o_object_2d_1.o_point_2d_translation.n_y = o_object_2d_2.o_point_2d_translation.n_y
                    
                    n_i_reversed-=1
                
        def f_collision_function_o_snake(self, o_collision_map_object):
                a_o_game_object_food = [
                    o for o in o_collision_map_object.a_o_collision_object
                    if (o.o_game_object.s_name == "food")
                ]
                # console.log(a_o_game_object_food)
                if(len(a_o_game_object_food) > 0):
                    # add limb
                    self.a_o_object_2d.append(
                        O_object_2d(
                            self.a_o_object_2d[len(self.a_o_object_2d)-1].o_point_2d_translation.n_x,
                            self.a_o_object_2d[len(self.a_o_object_2d)-1].o_point_2d_translation.n_y
                        )
                    )
                
        o_snake = O_game_object(
            "snake",
            0,
            0,
            f_render_function_o_snake, 
            f_collision_function_o_snake
        )

        self.a_o_game_object.append(o_snake)

        def f_create_food():
            def f_collision_function_o_food(self, o_collision_map_object):
                a_o_game_object_snake = [
                    o for o in o_collision_map_object.a_o_collision_object
                    if (o.o_game_object.s_name == "snake")
                ]
                # console.log(a_o_game_object_snake)
                if(len(a_o_game_object_snake) > 0):
                    # // add limb
                    n_index = self.a_o_game_object.index(self);
                    if (n_index > -1): #// only splice array when item is found
                        self.a_o_game_object.splice(n_index, 1); #// 2nd parameter means remove one item only
                    f_create_food()
                
                
            o_food = O_game_object(
                "food",
                int(random.uniform(0, 1)*self.o_grid.n_width),
                int(random.uniform(0, 1)*self.o_grid.n_height), 
                lambda self: True, 
                f_collision_function_o_food
            )
            self.a_o_game_object.append(o_food)
        

        f_create_food()

    def f_render(self):

        self.a_o_collision_map_object = []
        self.o_collision_map = {}

        # print(self.a_o_game_object)
        for o_game_object in self.a_o_game_object:
            o_game_object.f_render_function(o_game_object)
            for o_object_2d in o_game_object.a_o_object_2d:

                o_object_2d.o_point_2d_velocity.n_x += o_object_2d.o_point_2d_acceleration.n_x
                o_object_2d.o_point_2d_velocity.n_y += o_object_2d.o_point_2d_acceleration.n_y
                n_new_x = o_object_2d.o_point_2d_translation.n_x + o_object_2d.o_point_2d_velocity.n_x
                n_new_y = o_object_2d.o_point_2d_translation.n_y + o_object_2d.o_point_2d_velocity.n_y
                o_object_2d.o_point_2d_translation.n_x = n_new_x
                o_object_2d.o_point_2d_translation.n_y = n_new_y
                s_prop = f"a_{n_new_x}_{n_new_y}"
                if hasattr(self.o_collision_map, s_prop) == False:
                    o_collision_map_object = O_collision_map_object()
                    self.o_collision_map[s_prop] = o_collision_map_object
                    # setattr(self.o_collision_map, s_prop, o_collision_map_object)
                else:
                    o_collision_map_object = getattr(self.o_collision_map,s_prop)
                
                o_collision_map_object.a_o_collision_object.append(
                    O_collision_object(
                        o_game_object, 
                        o_object_2d
                    )
                )
                if(len(o_collision_map_object.a_o_collision_object) > 1):
                    self.a_o_collision_map_object.append(o_collision_map_object)
                
            
            

        for o_collision_map_object in self.a_o_collision_map_object:
            for o_collision_object in o_collision_map_object.a_o_collision_object:
                o_collision_object.o_game_object.f_collision_function(
                    o_collision_map_object
                )
            
        
        self.o_grid.f_clear()
        # print("render")
        # for n_i in range(0, 10):
            # print("a")
        os.system('cls' if os.name == 'nt' else 'clear')
        for o_game_object in self.a_o_game_object:
            for o_object_2d in o_game_object.a_o_object_2d:
                self.o_grid.a_a_b[o_object_2d.o_point_2d_translation.n_y][o_object_2d.o_point_2d_translation.n_x] = True
        self.o_grid.f_render()

        time.sleep(1/self.n_fps)
        self.f_render()

    def f_start(self):
        self.f_render()

if __name__ == "__main__":
    o_game = O_game()
    o_game.f_start()