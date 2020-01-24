import pygame
winw = 1280
winh = 640
vec = pygame.math.Vector2

if __name__ == "__main__":

    from flappyBird import *
    while(True):
        g = Game(gameArgs={'fps':30})
        print(g.main())
