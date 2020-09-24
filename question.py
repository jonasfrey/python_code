#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import time

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
        pressed_key = how_can_i_get_the_key_here()
        if pressed_key == "s"
            self.stop()

game = Game()
game.start()