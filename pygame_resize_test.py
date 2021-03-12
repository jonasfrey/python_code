import pygame
import pygame.freetype



pygame.init()
emoji_font = pygame.freetype.Font("NotoColorEmoji.ttf")
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
done = False

emoji_font.render_to(screen, (0, 0), '🤣')


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
    

    pygame.display.flip()
    clock.tick(60)