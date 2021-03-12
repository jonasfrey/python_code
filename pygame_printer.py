import pygame
from pygame.locals import *
import pygame.freetype  # Import the freetype module.
import time 
import sys
import os

class Pygame_Printer: 
    def __init__(self):
        self.string = ""
        self.clear_color = (33,33,33)
        self.font_color = (210, 210, 210)
        #the default notoColorEmoji must be overwritten somehow
        self.size_factor = 25
        self.noto_font_size_which_cant_be_changed = 136
        self.size_dividend = self.noto_font_size_which_cant_be_changed / self.size_factor
        self.lines_array = []
        self.window_width = 1000
        self.window_height = 1000
        pygame.init()
        #self.emoji_font = pygame.freetype.Font("seguiemj.ttf", self.size_factor)
        #self.emoji_font = pygame.freetype.Font("OpenSansEmoji.ttf", self.size_factor)
        #self.emoji_font = pygame.freetype.Font("NotoColorEmoji.ttf")
        #self.emoji_font = pygame.freetype.Font("NotoColorEmoji_changed#2.ttf")
        self.emoji_font = pygame.freetype.Font("NotoColorEmoji_WindowsCompatible.ttf")
        self.emoji_font = pygame.freetype.Font("NotoColorEmoji.ttf")
        
        #if windows 
        if os.name == 'nt':
            self.emoji_font = pygame.freetype.Font("seguiemj2.ttf", self.size_factor)

        #self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.screen = pygame.display.set_mode((self.window_width, self.window_height),pygame.RESIZABLE)
        self.scale = 0.5

        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.display.quit()
            elif event.type == VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.size)


    def print(self, string):

        self.lines_array = string.splitlines()
        self.print_lines_array()

    
    def print_lines_array(self): 
        self.screen.fill(self.clear_color)
        x = 0
        y = 0
        for chars_array in self.lines_array:
            #a line could possibily  extend the maximum characters per line, so we split the chars_array into multiple by max size !                
            #chars_array_lines = list(self.divide_chunks(chars_array, int(self.window_width/(self.size_factor))))
            chars_array_lines = [chars_array]

            for chars_array in chars_array_lines: 
                y+=1
                line_string = "".join(chars_array)

                text_surface, rect = self.emoji_font.render(line_string, (210,210,210))
                if os.name != 'nt':
                    text_surface = pygame.transform.scale(text_surface, ( int(text_surface.get_size()[0]/self.size_dividend), int(text_surface.get_size()[1]/self.size_dividend),))
                    size_factor_new_line = 1
                else: 
                    size_factor_new_line = self.size_factor * 1

                self.screen.blit(text_surface, (0, y*(size_factor_new_line)))
                
                #self.screen.blit(text_surface, (0, y*(self.size_factor*1)))
                # x = 0
                # for char in chars_array:
                #     x+=1
                #     self.canvas.create_text(x*self.size_factor, y*self.size_factor, font=self.font, text=char,fill="red")

        pygame.display.flip()
        pygame.display.update()

    def divide_chunks(self, l, n): 
        
        # looping till length l 
        for i in range(0, len(l), n):  
            yield l[i:i + n] 

    def clear(self):
        self.lines_array = []

if len(sys.argv) > 1:
    pptr = Pygame_Printer()
    lasdf = 5
    for value in range(0, 1000):
        time.sleep(0.032)
        string_list = list("⬛".join([""]*lasdf))
        string_list[(value%lasdf-1)] = "🍇"
        string_string = ''.join(string_list)
        #print(string_string)
        pptr.clear()
        print(string_string)
        pptr.print(string_string)


