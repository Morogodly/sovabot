import time
from const import *
import pygame as pg
import pygame.image

pygame.init()
pygame.mixer.init()

class Buttonss():
    def __init__(self):
        self.buttons = []

    def button_insert(self, *args):
        buttons = args
        for button in buttons:
            self.buttons.append(button)

    def button_collisions(self, pos, mouse ,click_sound = None):
        collide_flag = False
        for b in self.buttons:
            mouse_collide = b.check_collide(pos)

            if mouse_collide:
                b.check_click(pygame.mouse.get_pressed(3)[0], click_sound)
                collide_flag = True
        if collide_flag:
            mouse.image = pygame.image.load('mouse\mouse_click.png')


    def button_painter(self, screen):
        for button in self.buttons:
            screen.blit(button.image, button.position)


class Button(pg.sprite.Sprite):
    def __init__(self, images, funktion, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(images[0])
        self.rect = self.image.get_rect()
        self.position = position
        self.funktion = funktion

    def check_collide(self, pos):
        if self.position[0] <= pos[0] <= self.position[0]+self.rect.width:
            if self.position[1] <= pos[1] <= self.position[1]+self.rect.height:
                return True
        return False

    def check_click(self,mouse_click ,sound = None):
        if mouse_click:
                if sound != None:
                    sound.play()

                self.funktion()
                pygame.time.wait(120)


class Mouse(pg.sprite.Sprite):
    def __init__(self, position, image):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image)
        self.size = self.image.get_size()
        self.rect = pg.Rect(position[0], position[1], self.size[0], self.size[1])

    def set_new_mousePosition(self, pos):
        mouse_x, mouse_y = pos
        self.rect = pygame.rect.Rect(mouse_x, mouse_y, self.size[0], self.size[1])
        self.image = pg.image.load("mouse\mouse.png")

class Volume:
    def __init__(self, position, wight, height):
        self.position = position
        self.width, self.height = wight, height
        self.volume = 30

    def collision(self, pos):
        if self.position[0]<pos[0]<self.position[0]+self.width+2:
            if self.position[1]<pos[1]<self.position[1]+self.height:
                return (pos[0]-self.position[0])/self.width*100
        return False

    def set_volume(self, volume):
        if pygame.mouse.get_pressed(3)[0]:
            self.volume = int(volume)
            pygame.mixer.music.set_volume(self.volume/100)


    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.position[0], self.position[1], self.width, self.height), 1)
        screen.blit(global_font_20.render(f"{self.volume}%", True, GREEN), (self.position[0]+self.width+20, self.position[1]))
        for i in range(self.volume):
            pygame.draw.rect(screen, GREEN, (self.position[0]+3*i+2, self.position[1]+2, 2, self.height-4))

class Maker:
    def __init__(self, name, description, position):
        self.name = name
        self.description = description
        self.position = position

    def draw(self, pos, screen, mouse):
        screen.blit(self.name, self.position)
        if self.position[0]<pos[0]< self.position[0]+self.name.get_size()[0]:
            if self.position[1] < pos[1] < self.position[1] + self.name.get_size()[1]:
                mouse.image = pygame.image.load('mouse\_action_mouse.png')
                pygame.draw.rect(screen, BLACK, (pos[0]+20, pos[1]-40, self.description.get_size()[0]+8,30))
                pygame.draw.rect(screen, GREEN, (pos[0] + 20, pos[1] - 40, self.description.get_size()[0] + 8, 30),2)
                screen.blit(self.description, (pos[0]+24, pos[1]-38))

class Music:
    def __init__(self, music, names, position, size):
        self.music = music
        self.names = names
        self.now_music = 0
        self.position = position
        self.width, self.height = size

    def change_music(self, reverse = False):
        if reverse:
            if self.now_music > 0:
                self.now_music-=1
            else:
                self.now_music = len(self.music)-1
        else:
            if self.now_music < len(self.music)-1:
                self.now_music+=1
            else:
                self.now_music = 0

        pygame.mixer.music.load(self.music[self.now_music])
        pygame.mixer.music.play(-1)

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.position[0], self.position[1], self.width, self.height), 1)
        name = global_font_15.render(f'{self.names[self.now_music]}', True, GREEN)
        screen.blit(name, (self.position[0]+5, self.position[1]+2))
        screen.blit(global_font_20.render('music', True, GREEN), (400, 270))