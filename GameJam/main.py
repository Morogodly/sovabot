import random
import Animations
from Buttons import *
import pygame
from pause import Pause

WIDTH = 1180
HEIGHT = 720
FPS = 60
pygame.init()
pygame.mixer.init()
click_sound = pygame.mixer.Sound('click.wav')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

def b1_funk():
    print(random.randint(1, 100))


anims = []
anims.append(Animations.animation(["anim\cat1.png","anim\cat2.png","anim\cat3.png","anim\cat4.png","anim\cat5.png"], (100,100), 400, 1))
anims.append(Animations.animation(["anim\cat1.png","anim\cat2.png","anim\cat3.png","anim\cat4.png","anim\cat5.png"], (300,100), 400, 1))
anims.append(Animations.animation(["anim\cat1.png","anim\cat2.png","anim\cat3.png","anim\cat4.png","anim\cat5.png"], (500,100), 400, 1))
anims.append(Animations.animation(["anim\cat1.png","anim\cat2.png","anim\cat3.png","anim\cat4.png","anim\cat5.png"], (700,100), 400, 1))



pygame.mouse.set_visible(False)
mouse = Mouse(pygame.mouse.get_pos(), 'mouse.png')



running = True
while running:
    clock.tick(FPS)

    pos = pygame.mouse.get_pos()
    mouse.set_new_mousePosition(pos)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif type(event.type) == int and event.type>pygame.USEREVENT:
            for a in anims:
                if a.uid == event.type-pygame.USEREVENT:
                    a.change_frame()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1 or event.key == pygame.K_ESCAPE:
                Pause(clock, WIDTH, HEIGHT, mouse)

    screen.fill((10,10, 10))
    for i in anims:
        screen.blit(i.image, i.position)

    screen.blit(mouse.image, mouse.rect)
    pygame.display.flip()