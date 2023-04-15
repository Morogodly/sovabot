import pygame
import os
from const import *


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
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
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.image.blit(pygame.image.load(image), (0, 0, 50, 50))
        self.rect = self.image.get_rect()
        self.x_speed = 8
        self.y_speed = 8
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def x_motion(self, k_right):
        if self.rect.x <= WIDTH:
            if k_right:
                self.rect.x+=self.x_speed
        if self.rect.x >= 0:
            if not k_right:
                self.rect.x-=self.x_speed

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
        self.image.blit(pygame.transform.scale(load_image("sprites\\bee_base.jpg"), (75, 75)), (0, 0, 75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] - 85
        self.rect.y = screen_size[1] - 85


def Game(screen):
    running = True
    base_sprite = pygame.sprite.Group()
    base_sprite.add(Base())
    bee = Bee((WIDTH // 2, HEIGHT // 2), "menu_buttons\ok.png")
    player = pygame.sprite.Group()
    player.add(bee)

    while running:
        clock.tick(FPS)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if keys[pygame.K_d]:
            bee.x_motion(k_right=True)
        elif keys[pygame.K_a]:
            bee.x_motion(k_right=False)
        if keys[pygame.K_w]:
            bee.y_motion(True)
        else:
            bee.y_motion(False)


        screen.fill(BLACK)
        player.update()
        player.draw(screen)
        base_sprite.draw(screen)
        pygame.display.flip()