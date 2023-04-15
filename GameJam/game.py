import pygame
import os
from const import *
import random
import datetime

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

class Button:
    def __init__(self, text, pos, func, b_width=240, b_height=60):
        self.text = text
        self.pos = pos
        self.func = func
        self.b_width, self.b_height = b_width, b_height
        self.h_color = pygame.Color("White")
        self.button_surface = None

    def render(self):
        self.button_surface = pygame.Surface((self.b_width, self.b_height), pygame.SRCALPHA)
        self.button_surface.convert_alpha()
        self.button_surface.fill(pygame.Color(0, 0, 0, 0))
        pygame.draw.rect(self.button_surface, pygame.Color("Black"), (1, 1, self.b_width - 2, self.b_height - 2),
                         border_radius=10)
        pygame.draw.rect(self.button_surface, self.h_color, (2, 2, self.b_width - 4, self.b_height - 4),
                         border_radius=10)
        font = pygame.font.Font("fonts/Font.ttf", 16)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(120, 30))
        self.button_surface.blit(text, text_rect)

    def is_hovered(self, mouse_pos):
        if (self.pos[0] <= mouse_pos[0] <= self.pos[0] + self.b_width and
                self.pos[1] <= mouse_pos[1] <= self.pos[1] + self.b_height):
            self.h_color = (150, 150, 150)
        else:
            self.h_color = pygame.Color("White")

    def is_clicked(self):
        return self.h_color == (150, 150, 150)

class Bee(pygame.sprite.Sprite):
    def __init__(self,pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(load_image(f"bee\\bee{i}.png"), (50, 50)) for i in range(1,10)]
        self.frame = 0
        self.start_img = self.images[0]
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.image.blit(self.start_img, (0, 0, 50, 50))
        self.rect = self.image.get_rect()
        self.x_speed = 8
        self.y_speed = 8
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.is_flower = False
        self.is_nest = False
        self.nectar = 0

    def x_motion(self, k_right, windy):
        if self.rect.x <= WIDTH:
            if k_right:
                self.rect.x+=(self.x_speed-int(4/25*self.nectar)-windy)
                img = pygame.transform.flip(self.start_img, True, False)
                self.image.blit(img, (0, 0, 50, 50))

        if self.rect.x >= 0:
            if not k_right:
                self.rect.x-=(self.x_speed-int(4/25*self.nectar)+windy)
                self.image.blit(self.start_img, (0, 0, 50, 50))

    def y_motion(self, k_up):
        if self.rect.y <= HEIGHT-50:
            if not k_up:
                self.rect.y += self.y_speed + int(2/25*self.nectar)
        if self.rect.y >= 00:
            if k_up:
                self.rect.y -= self.y_speed - int(4/25*self.nectar)
    def change_frames(self):
        if self.frame < 40:
            self.frame +=1
        else:
            self.frame = 0
        self.start_img = self.images[self.frame//5]
        self.image.fill((0,0,0,0))
        self.image.blit(self.start_img, (0, 0, 50, 50))

class Base(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((150, 150), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(pygame.transform.scale(load_image("bee_base.png"), (150, 150)), (0, 0, 150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = screen_size[0] - 140
        self.rect.y = 50
        self.nectar = 100
        self.health = 100

    def update(self, bee):
        if self.nectar > 0:
            if not bee.is_nest:
                self.nectar = max(0, self.nectar - 3/FPS)
        else:
            self.health = max(0, self.health - 5/FPS)

    def draw_bars(self, screen):
        pygame.draw.rect(screen, (255,0,0), (WIDTH-100, self.rect.y+160, self.health, 5))
        pygame.draw.rect(screen, (255, 255, 0),(WIDTH-100, self.rect.y + 180, self.nectar, 5))

class Leg(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((200, 720), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(pygame.transform.scale(load_image("leg.png"), (200, 720)), (0, 0, 200, 720))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-400)
        self.rect.y = -720
        self.active = False
        self.is_punch = False

    def y_motiont(self):
        if self.active:
            if self.rect.y <= 0:
                self.rect.y += 10
            else:
                self.active = False
        else:
            if self.rect.y > -720:
                self.rect.y -=15
            else:
                self.rect.x = random.randint(0, WIDTH - 400)
                self.rect.y = -720
                self.is_punch = False


class Flower(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.id = random.randint(0, 1000)
        self.nectar = 15
        self.image = pygame.Surface((60, 100), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(pygame.transform.scale(load_image(random.choice(['f2.png','f3.png','f4.png'])), (60, 100)), (0, 0, 60, 100))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.died_timestamp = -1
        self.expected_timestamp = -1
        self.died = False

    def update(self):
        if self.nectar == 0 and not self.died:
            self.died = True
            self.died_timestamp = datetime.datetime.now()
            self.expected_timestamp = datetime.datetime.now() + datetime.timedelta(seconds=15)
        else:
            if self.expected_timestamp != -1:
                if self.expected_timestamp <= datetime.datetime.now():
                    self.died = False
                    self.died_timestamp = -1
                    self.expected_timestamp = -1
                    self.nectar = 15

def Game(screen):
    running = True
    base = Base()
    base_sprite = pygame.sprite.Group()
    base_sprite.add(base)
    bee = Bee((WIDTH // 2, HEIGHT // 2), "bee\\bee.png")
    player = pygame.sprite.Group()
    player.add(bee)
    font = pygame.font.Font("fonts/Font.ttf", 24)

    change_windy = pygame.event.Event(pygame.USEREVENT + 10)
    pygame.event.post(change_windy)
    pygame.time.set_timer(change_windy, 15 * 1000)

    add_leg = pygame.event.Event(pygame.USEREVENT + 11)
    pygame.event.post(add_leg)
    pygame.time.set_timer(add_leg, 5 * 1000)

    windy = 0

    start_nectar = 0
    score = 0

    leg = pygame.sprite.Group()
    legg = Leg()
    leg.add(legg)
    flower_sprites = pygame.sprite.Group()
    flower_array = []
    for i in range(7):
        tmp = Flower((50 + i * 200, 480))
        flower_array.append(tmp)
        flower_sprites.add(tmp)

    for i in range(5):
        tmp = Flower((125 + i * 200, 620))
        flower_array.append(tmp)
        flower_sprites.add(tmp)

    while running:

        bee.change_frames()

        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT + 10:
                if windy < 4:
                    windy += 1
                else:
                    windy = 0
            if event.type == pygame.USEREVENT + 11:
                legg.active = True
                print(1)

        if keys[pygame.K_d] and not bee.is_flower and not bee.is_nest:
            bee.x_motion(k_right=True, windy=windy)
        elif keys[pygame.K_a] and not bee.is_flower and not bee.is_nest:
            bee.x_motion(k_right=False, windy=windy)
        if keys[pygame.K_w]:
            bee.y_motion(True)
        elif not bee.is_flower and not bee.is_nest:
            bee.y_motion(False)

        collisions = pygame.sprite.spritecollide(bee, flower_sprites, False)
        for c in collisions:
            if not bee.is_flower and not keys[pygame.K_w] and c.nectar > 0:
                bee.is_flower = True
                bee.rect.x = c.rect.x
                bee.rect.y = c.rect.y
            else:
                bee.is_flower = False
            if c.nectar > 0:
                bee.nectar = min(25, bee.nectar + 4 / FPS)
                c.nectar = max(0, c.nectar - 4 / FPS)

        nest_collide = pygame.sprite.spritecollide(bee, base_sprite, False)
        legg.y_motiont()

        legg_collide = pygame.sprite.spritecollide(bee, leg, False)
        if legg_collide:
            if not legg_collide[0].is_punch:
                bee.nectar = 0
                legg_collide[0].active = False
                punch_sound.play()
                legg_collide[0].is_punch = True


        if nest_collide:
            if not bee.is_nest and not keys[pygame.K_w] and bee.nectar > 0:
                bee.is_nest = True
                start_nectar = bee.nectar
                bee.rect.x = base.rect.x
                bee.rect.y = base.rect.y
            else:
                score += 5 * max(start_nectar - bee.nectar, 0)
                bee.is_nest = False

            if nest_collide[0].nectar != 100:
                if min(nest_collide[0].nectar + 5/FPS, 100) == 100:
                    bee.nectar = max(bee.nectar - 100 - nest_collide[0].nectar, 0)
                    nest_collide[0].nectar = 100
                else:
                    bee.nectar = max(bee.nectar - 5/FPS, 0)
                    nest_collide[0].nectar += 5/FPS

        if base.health <= 0:
            transparent_background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            transparent_background.convert_alpha()
            transparent_background.fill((0, 0, 0, 100))
            pygame.mouse.set_visible(True)
            screen.blit(transparent_background, (0, 0))
            button = Button("MAIN MENU", (1180 // 2 - 240 // 2, 400), lambda: 0)
            font = pygame.font.Font("fonts/Font.ttf", 28)
            text = font.render("GAME OVER", True, (255, 255, 255))
            text_rect = text.get_rect(center=(1180 // 2, 200))
            screen.blit(text, text_rect)
            while True:
                clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.mouse.set_visible(False)
                        running = False
                if pygame.mouse.get_pressed(3)[0]:
                    button.is_hovered(pygame.mouse.get_pos())
                    if button.is_clicked():
                        pygame.mouse.set_visible(False)
                        break
                button.is_hovered(pygame.mouse.get_pos())
                button.render()
                screen.blit(button.button_surface, button.pos + (240, 60))
                pygame.display.flip()
            break

        screen.fill((100, 100, 100))

        health = font.render(f"Health: {round(base.health)}", True, (255, 0, 0))
        health_rect = health.get_rect()
        health_rect.x, health_rect.y = 0, 0
        screen.blit(health, health_rect)

        nectar = font.render(f"Nectar: {round(base.nectar)}", True, (255, 255, 0))
        nectar_rect = nectar.get_rect()
        nectar_rect.x, nectar_rect.y = 0, 50
        screen.blit(nectar, nectar_rect)
        score_text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.topright = (1170, 10)
        screen.blit(score_text, score_rect)

        bee_nectar = global_font_15.render(f"{round(bee.nectar)}", True,  (int(255 * (bee.nectar/25)), int(255 * (1-bee.nectar/25)), 0))
        bee_nectar_rect = bee_nectar.get_rect(center=(bee.rect.x + 25, bee.rect.y - 10))
        screen.blit(bee_nectar, bee_nectar_rect)

        for flower in flower_array:
            if flower.died:
                flower_timer = global_font_15.render(f"{int((flower.expected_timestamp - datetime.datetime.now()).total_seconds())}", True,
                                                   (255, 255, 255))
                flower_timer_rect = flower_timer.get_rect(center=(flower.rect.x + 37, flower.rect.y - 10))
                screen.blit(flower_timer, flower_timer_rect)

        flower_sprites.update()
        player.update()
        base.update(bee)
        base.draw_bars(screen)
        flower_sprites.draw(screen)
        base_sprite.draw(screen)
        player.draw(screen)
        leg.update()
        leg.draw(screen)
        pygame.display.flip()