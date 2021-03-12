# Simple pygame program
# Import and initialize the pygame library

import pygame
import pygame.freetype

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])
# Run until the user asks to quit

running = True

while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white



    # Draw a solid blue circle in the center



    emoji_font = pygame.freetype.Font("NotoColorEmoji.ttf", True)
    text_surface, rect = emoji_font.render("🎢", (0, 0, 0))

    screen.blit(text_surface, (4,4)) #Draw image to screen.

    # Flip the display
    pygame.display.flip()


# Done! Time to quit.

pygame.quit()

