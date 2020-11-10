import pygame
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from accounts.models import Profile


# Screen settings
screenWidth = 1200
screenHeight = 1000
pygame.display.set_caption("Bridge")


def mainLoop(username):
    run = True
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    while run:
        screen.fill((40, 125, 67))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                profile.play_status = False
                profile.save()
                break
