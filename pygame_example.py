import pygame
from pygame.locals import *
import pygame.freetype  # Import the freetype module.
import time 



class Pygame_Printer: 
    def __init__(self):
        self.string = ""
        self.size_factor = 200
        pygame.init()
        self.emoji_font = pygame.freetype.Font("NotoColorEmoji.ttf")
        self.screen = pygame.display.set_mode((1000, 1000),HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.fake_screen = self.screen.copy()


        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.display.quit()
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)



    def print(self, string):
        self.string = string
        text_surface, rect = self.emoji_font.render(self.string, (0, 0, 0))
        self.screen.blit(text_surface, (0, 0))
        
        self.screen.fill('white')
        self.fake_screen.fill('white')
        self.fake_screen.blit(text_surface,(200,10))
        resize_factor = int(self.size_factor)
        
        self.screen.blit(pygame.transform.scale(self.fake_screen, ( resize_factor, resize_factor) ), (0, 0))
        pygame.display.flip()

        pygame.display.update()


pptr = Pygame_Printer()

for value in range(0, 1000):
    # time.sleep(0.016)
    # string_list = list("⬛".join([""]*10))
    # string_list[(value%9)] = "🤣"
    # string_string = ''.join(string_list)
    # print(string_string)
    # pptr.print(string_string)

    time.sleep(0.016)
    if(value % 2 == 0):
        pptr.print("⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣")
    else: 
        pptr.print("🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛🤣⬛")
