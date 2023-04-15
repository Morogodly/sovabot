import random

import pygame
import os
from const import *


def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bee(pygame.sprite.Sprite):
    def __init__(self,pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.start_img = pygame.transform.scale(load_image(image), (50, 50))
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.image.blit(self.start_img, (0, 0, 50, 50))
        self.rect = self.image.get_rect()
        self.x_speed = 8
        self.y_speed = 8
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.is_flower = False
        self.nectar = 0

    def x_motion(self, k_right):
        if self.rect.x <= WIDTH:
            if k_right:
                self.rect.x+=self.x_speed
                img = pygame.transform.flip(self.start_img, True, False)
                self.image.blit(img, (0, 0, 50, 50))

        if self.rect.x >= 0:
            if not k_right:
                self.rect.x-=self.x_speed
                self.image.blit(self.start_img, (0, 0, 50, 50))

    def y_motion(self, k_up):
        if self.rect.y <= HEIGHT:
            if not k_up:
                self.rect.y += self.y_speed
        if self.rect.y >= 0:
            if k_up:
                self.rect.y -= self.y_speed


class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((75, 75), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(pygame.transform.scale(load_image("bee_base.jpg"), (75, 75)), (0, 0, 75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] - 85
        self.rect.y = screen_size[1] - 85


class Flower(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.id = random.randint(0, 1000)
        self.nektar = 10
        self.image = pygame.Surface((75, 75), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(pygame.transform.scale(load_image("bee.png"), (75, 75)), (0, 0, 75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


def Game(screen):
    running = True
    base_sprite = pygame.sprite.Group()
    base_sprite.add(Base())
    bee = Bee((WIDTH // 2, HEIGHT // 2), "bee.png")
    player = pygame.sprite.Group()
    player.add(bee)

    flower_sprites = pygame.sprite.Group()

    for i in range(5):
        flower_sprites.add(Flower((50+i*200, 600)))
    

    while running:
        clock.tick(FPS)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if keys[pygame.K_d] and not bee.is_flower:
            bee.x_motion(k_right=True)
        elif keys[pygame.K_a] and not bee.is_flower:
            bee.x_motion(k_right=False)
        if keys[pygame.K_w]:
            bee.y_motion(True)
        elif not bee.is_flower:
            bee.y_motion(False)

        collisions = pygame.sprite.spritecollide(bee, flower_sprites, False)
        for c in collisions:
            if not bee.is_flower and not keys[pygame.K_w]:
                bee.is_flower = True
                bee.rect.x = c.rect.x
                bee.rect.y = c.rect.y
            else:
                bee.is_flower = False

            bee.nectar+=max(0, c.self.nektar-2/FPS)







        screen.fill(BLACK)
        player.update()
        base_sprite.draw(screen)

        flower_sprites.draw(screen)

        player.draw(screen)
        pygame.display.flip()