import time
import keyboard
import mouse


class Time_measuring:
    def __init__(self):
        self.tss_ms = []

    def measure(self):
        self.tss_ms.append(time.time())

    @property 
    def delta_ts_ms(self):
        if(len(self.tss_ms) < 2):
            return 0
        second_last_ts_ms = self.tss_ms[-2]
        last_ts_ms = self.tss_ms[-1]
        return last_ts_ms - second_last_ts_ms
        
    @property  
    def fps(self):
        return 1000/self.delta_ts_ms

if __name__ == "__main__":


    print("test")
    t = 0
    tt = 0
    while_loop_t = Time_measuring()
    alt_pressed_measuring = Time_measuring()
    fps_screen_nowadays = 144

    last_move_mouse = False
    current_speed_function = "speed_function_quadric"

    def speed_function_quadric(speed, t):
        a = 0.1
        speed = speed + 1
        return a*speed*speed

    def speed_function_linear(speed, t):
        max_speed = 20
        speed = (speed+t) *0.2
        if(speed >= max_speed):
            return max_speed
        else: 
            return speed


    def speed_function(speed, t):
        #return locals()[current_speed_function](speed, t)
        #return speed_function_quadric(speed, t)
        speed = speed_function_quadric(speed, t)
        speed = speed_function_linear(speed, t)
        return speed

    while True:  # making a loop
        while_loop_t.measure()
        tt+=1
        this_ts_ms = time.time()
        if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            break
        
        if keyboard.is_pressed('alt'):  # if key 'q' is pressed 
            alt_pressed_measuring.measure()

            #print(alt_pressed_measuring.delta_ts_ms)

            o_x, o_y = mouse.get_position()
            t+=1
            if(last_move_mouse):
                speed = speed_function(speed, t)
            else: 
                speed = 1
                t = 1
            
            x = o_x
            y = o_y
            move_mouse = False
            if keyboard.is_pressed('i'):  # if key 'q' is pressed 
                y = o_y - speed

            if keyboard.is_pressed('k'):  # if key 'q' is pressed 
                y = o_y + speed

            if keyboard.is_pressed('l'):  # if key 'q' is pressed 
                x = o_x + speed

            if keyboard.is_pressed('j'):  # if key 'q' is pressed 
                x = o_x - speed

            if keyboard.is_pressed("ctrl"):
                if keyboard.is_pressed('space'):  # if key 'q' is pressed 
                    print("space")
                    mouse.click(button='left')
                else: 
                    mouse.release()

            
            move_mouse = (x != o_x or y != o_y)

            if(move_mouse):
                #pyautogui.moveTo(x,y)
                mouse.move(x,y)
                # ctypes.windll.user32.SetCursorPos(x, y)
            last_move_mouse = move_mouse

        time.sleep(1/fps_screen_nowadays)

    print("test")
