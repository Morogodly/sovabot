import pygame
import os
from const import *
import random

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
                self.rect.x+=(self.x_speed-int(4/25*self.nectar))
                img = pygame.transform.flip(self.start_img, True, False)
                self.image.blit(img, (0, 0, 50, 50))

        if self.rect.x >= 0:
            if not k_right:
                self.rect.x-=(self.x_speed-int(4/25*self.nectar))
                self.image.blit(self.start_img, (0, 0, 50, 50))

    def y_motion(self, k_up):
        if self.rect.y <= HEIGHT:
            if not k_up:
                self.rect.y += (self.y_speed-int(4/25*self.nectar))
        if self.rect.y >= 0:
            if k_up:
                self.rect.y -= (self.y_speed-int(4/25*self.nectar))


class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((75, 75), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(pygame.transform.scale(load_image("bee_base.jpg"), (75, 75)), (0, 0, 75, 75))
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] - 85
        self.rect.y = 85
        self.nectar = 100
        self.health = 100

    def update(self):
        if self.nectar > 0:
            self.nectar = max(0, self.nectar - 3/FPS)
        else:
            self.health = max(0, self.health - 5/FPS)


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
    base = Base()
    base_sprite = pygame.sprite.Group()
    base_sprite.add(base)
    bee = Bee((WIDTH // 2, HEIGHT // 2), "bee.png")
    player = pygame.sprite.Group()
    player.add(bee)
    font = pygame.font.Font("fonts/Font.ttf", 24)
    health = font.render("Health: 100", True, (255, 0, 0))
    health_rect = health.get_rect()
    health_rect.x, health_rect.y = 0, 0
    screen.blit(health, health_rect)
    flower_sprites = pygame.sprite.Group()
    for i in range(5):
        flower_sprites.add(Flower((50 + i * 200, 600)))

    while running:
        clock.tick(FPS)
        print(base.nectar)
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
            if not bee.is_flower and not keys[pygame.K_w] and c.nektar>0:
                bee.is_flower = True
                bee.rect.x = c.rect.x
                bee.rect.y = c.rect.y
            else:
                bee.is_flower = False
            if c.nektar > 0:
                bee.nectar = min(25, bee.nectar+2/FPS)
                c.nektar = max(0, c.nektar-2/FPS)


        nest_collide = pygame.sprite.spritecollide(bee, base_sprite, False)

        if nest_collide:
            if nest_collide[0].nectar != 100:
                if min(nest_collide[0].nectar + 5/FPS, 100) == 100:
                    bee.nectar = max(bee.nectar - 100 - nest_collide[0].nectar, 0)
                    nest_collide[0].nectar = 100
                else:
                    bee.nectar = max(bee.nectar - 5/FPS, 0)
                    nest_collide[0].nectar += 5/FPS

        screen.fill(BLACK)

        health = font.render(f"Health: {round(base.health)}", True, (255, 0, 0))
        health_rect = health.get_rect()
        health_rect.x, health_rect.y = 0, 0
        screen.blit(health, health_rect)

        nectar = font.render(f"Nectar: {round(base.nectar)}", True, (255, 255, 0))
        nectar_rect = nectar.get_rect()
        nectar_rect.x, nectar_rect.y = 0, 50
        screen.blit(nectar, nectar_rect)

        bee_nectar = global_font_15.render(f"{round(bee.nectar)}", True, (255, 255, 255))
        bee_nectar_rect = bee_nectar.get_rect(center=(bee.rect.x + 25, bee.rect.y - 10))
        screen.blit(bee_nectar, bee_nectar_rect)

        player.update()
        base.update()
        flower_sprites.draw(screen)
        base_sprite.draw(screen)
        player.draw(screen)
        pygame.display.flip()