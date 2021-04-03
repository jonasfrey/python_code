# import pygame 
# import time
# bool_is_true = True
# i = 0
# pygame.init()
# while bool_is_true and i < 1000:
#     i+=1
#     time.sleep(0.1)
#     print(i)
#     events = pygame.event.get()
#     for event in events:
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_LEFT:
#                 bool_is_true = False


import pygame
pygame.init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                print("Hey, you pressed the key, '0'!")
            if event.key == pygame.K_1:
                print("Doing whatever")
