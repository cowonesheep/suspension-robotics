import pygame

pygame.init()
window = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Pygame Demonstration")

mainloop=True
while mainloop:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            mainloop = False

        if event.type == pygame.KEYDOWN:

            print(pygame.key.name(event.key))
            if event.key == pygame.K_p:
                print('If condition is met')
pygame.quit()
