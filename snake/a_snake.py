import os, time, keyboard


class Game: 
    def __init__(self):

        self.running = False
        self.pressed_key = ""
        self.delta_ms = 0
        self.now_ms = 0
        self.then_ms = 0
        self.fps = 100
        self.interval_ms = self.get_interval_ms()
        self.real_interval_ms = 0
        self.t = 0
        self.frame = 0


        self.setup()
    
    def setup(self):
        # rows, columns = os.popen('stty size', 'r').read().split()
        # print(rows, columns)
        # exit()
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
        exit()


    def render_frame(self):
        print("rendering " + str(self.t) + " frame, current fps is:")
        print(1000 / self.real_interval_ms) 


        # if self.pressed_key == "w":
        #     self.o["y"] = self.o["y"] - 1
        # if self.pressed_key == "s":
        #     self.o["y"] = self.o["y"] + 1
        # if self.pressed_key == "a":
        #     self.o["x"] = self.o["x"] - 1
        # if self.pressed_key == "d":
        #     self.o["x"] = self.o["x"] + 1

        #self.canvas.clear()
        os.system('cls' if os.name == 'nt' else 'clear')

        # self.canvas.addPixel(self.o["x"]%self.canvas.width, self.o["y"]%self.canvas.height,self.o["c"])
        self.canvas.draw()

        if self.pressed_key == "x":
            self.stop()


class Object():
    def __init__(self, name, co_existence_limit, iteration_count, iteration_count_limit, collision_happened, repeat_func):
        self.name = name
        self.co_existence_limit = co_existence_limit
        self.iteration_count = iteration_count
        self.iteration_count_limit = iteration_count_limit
        self.collision_happened = collision_happened
        self.repeat_func = repeat_func
        self.limbs = [Limb()]

    def afunction(self, item):
        self.item = item


class Limb():
    def __init__(self, position): 
        self.position = Position()


class Position():
    def __init__(self, x, y, z, utf_8, detect_collision):
        self.x = x
        self.y = y
        self.z = z
        self.utf_8 = utf_8
        self.collidable = collidable
        self.collidet_with = []
    
    def collision_happened(self):
        print("collision")

    def detect_collision(self):
        self.collidet_with = []
        if(self.collidable):
            for limb in Game.limbs:
                if(
                    self.position.x == limb.position.x and
                    self.position.y == limb.position.y and
                    self.position.z == limb.position.z ):
                    self.collidet_with.append(limb)
            
            if(self.collidet_with): 
                self.collision_happened(self.collidet_with)

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.output = ""
        self.pixel_matrix = []
        self.clear_pixel_matrix = []
        self.counter = 0
        self.white_pixel = " "
        self.black_pixel = "*"
        
        self.pixel_matrix = self.get_cleared_matrix()
        #print(self.pixel_matrix)

    def get_cleared_matrix(self):
        clear_pixel_matrix = []
        for y in range(0, self.height):
            y_array = []
            for x in range(0, self.width):
                y_array.append([" "])
            clear_pixel_matrix.append(y_array)
        return clear_pixel_matrix
    def clear(self):
        
        #self.pixel_matrix = self.get_cleared_matrix()
        os.system('cls')

    def get_index_by_xy(self, x , y): 
        return y * self.height + x
    
    def get_xy_by_index(self, index):
        return int(index/self.width) + index % self.width

    def add_pixel(self, x,y,z,character_set_property_name):
        
        utf_8 = self.character_set[character_set_property_name] 

        x = int(x)
        y = int(y)
        z = int(z)

        if x > self.width | y > self.height:
            print("canvas is not big enought to add a pixel at this position")
        else:
            self.pixel_matrix[y][x][z] = utf_8


    def draw(self):
        global character_set

        self.output = ""
        for x in self.pixel_matrix:
            for y in x:
                z = 0
                pixel_matrix_value = y[z]
                self.output += pixel_matrix_value
                # if isinstance(value, str):
                #     self.output += value
                # else:
                #     self.output += character_set[self.character_set_property_name_white_pixel]
            self.output +="\n"

        print(self.output)


game = Game()
game.start()

keyboard.on_press_key("p", lambda _:print("You pressed p"))