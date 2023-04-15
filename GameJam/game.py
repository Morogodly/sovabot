import pygame

import const
from const import *

class Bee():
    def __init__(self, pos, image):
        self.x = pos[0]
        self.y = pos[1]
        self.image = pygame.image.load(image)
        self.x_speed = 8
        self.y_speed = 8

    def x_motion(self, k_right):
        if 0<self.x<WIDTH:
            if k_right:
                self.x += self.x_speed
            else:
                self.x -= self.y_speed

    def y_motion(self, k_up):
        if 0<self.y<HEIGHT:
            if k_up:
                self.y -= self.y_speed
            else:
                self.y += self.x_speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))






def Game(screen):
    running = True

    player = Bee((WIDTH//2, HEIGHT//2), "menu_buttons\ok.png")


    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.x_motion(True)

        screen.fill(BLACK)
        player.draw(screen)
        pygame.display.flip()