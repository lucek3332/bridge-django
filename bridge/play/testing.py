import pygame


# Screen settings
screenWidth = 1200
screenHeight = 1000
pygame.display.set_caption("Bridge")


def mainLoop():
    run = True
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    while run:
        screen.fill((40, 125, 67))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
