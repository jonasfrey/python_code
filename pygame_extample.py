import pygame
import pygame.freetype  # Import the freetype module.


pygame.init()
screen = pygame.display.set_mode((800, 600))
emoji_font = pygame.freetype.Font("NotoColorEmoji.ttf")
running =  True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))

    # You can use `render` and then blit the text surface ...
    text_surface, rect = emoji_font.render("🔪🔪", (100, 0, 0))

    screen.blit(text_surface, (0, 0))

    pygame.transform.scale(screen, (1000,1000) ), (0, 0)    

    # or just `render_to` the target surface.
    pygame.display.flip()

pygame.quit()