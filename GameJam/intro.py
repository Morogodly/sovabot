import random
from menu import Menu
import pygame
from Buttons import *
from const import *

class LoadBars:
    def __init__(self, delay, lenght):
        self.bars = []
        self.delay = delay
        self.lenght = lenght


        add_rects = pygame.event.Event(pygame.USEREVENT + 1)
        pygame.event.post(add_rects)
        pygame.time.set_timer(add_rects, self.delay)

    def addRect(self, width, height):
        if len(self.bars) < self.lenght:
            self.bars.append((width,height))

    def draw(self, screen):
        for i in range(len(self.bars)-1):
            pg.draw.rect(screen, GREEN, (WIDTH//2-250+6+((self.bars[i][0]+2)*i), HEIGHT//2-25+7, self.bars[i][0], self.bars[i][1]))

class LoadText:
    def __init__(self, texts):
        self.texts = texts
        self.frame = 0
        self.frames = len(texts)-1

    def change_frame(self):
        if self.frame<self.frames:
            self.frame+=1
        else:
            self.frame = 0

    def draw(self, screen):
        load_txt = global_font.render(self.texts[self.frame], True, GREEN)
        screen.blit(load_txt, (WIDTH // 2 - load_txt.get_size()[0] // 2, HEIGHT // 2 - 25 - 40))

class ErrorText:
    def __init__(self, texts, delay):
        self.texts = texts
        self.frame = 0
        self.frames = len(texts) - 1
        self.flag = True

        add_rects = pygame.event.Event(pygame.USEREVENT + 2)
        pygame.event.post(add_rects)
        pygame.time.set_timer(add_rects, delay)

    def change_frame(self):
        if self.frame<self.frames:
            self.frame+=1
        else:
            if self.flag:
                self.flag = False
                error_sound.play()
                err_eindow()

    def draw(self, screen):
        for i in range(self.frame+1):
            load_txt = global_font_15.render(self.texts[i], True, GREEN)
            screen.blit(load_txt, (5, i*20+5))

class ErrorWindow:
    def __init__(self, img, buttons, WIDTH, HEIGHT):
        self.image = pygame.image.load(img)
        self.buttons = buttons
        self.pos = (WIDTH//2-self.image.get_size()[0]//2, HEIGHT//2-self.image.get_size()[1]//2)

    def change_pos(self):
        self.pos = (random.randint(0, WIDTH-self.image.get_size()[0]), random.randint(0, HEIGHT-self.image.get_size()[1]))
        self.buttons.buttons[0].position = (self.pos[0]+240, self.pos[1]+205)
        self.buttons.buttons[1].position = (self.pos[0]+293, self.pos[1]+205)

    def draw(self, screen):
        screen.blit(self.image, self.pos)
        self.buttons.button_painter(screen)


def No_button():
    global ErrWindow
    ErrWindow.change_pos()

def Ok_button():
    global running
    Menu(screen)
    running = False

def err_eindow():
    global is_error_window
    is_error_window = True





is_error_window = False
screen_size = WIDTH, HEIGHT = (1180, 720)

buttons = Buttonss()
buttons.button_insert(
    Button(['menu_buttons\_no.png'], No_button, (655, 445)),
    Button(['menu_buttons\ok.png'], Ok_button, (707, 445))
)
ErrWindow = ErrorWindow('err1.png', buttons, WIDTH, HEIGHT)



pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music\load.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
error_sound = pygame.mixer.Sound('sounds\error.wav')


screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Game")

pygame.mouse.set_visible(False)

mouse = Mouse(pygame.mouse.get_pos(), 'mouse\mouse.png')

load_bars = LoadBars(300, 39)
err_text = ErrorText(choise, 400)

global_font = pygame.font.Font('fonts\Font.ttf', 30)
load_text = LoadText(["Loading|","Loading/","Loading-",f"Loading{chr(92)}","Loading|","Loading/", "Loading-", f"Loading{chr(92)}"])

running = True
while running:
    clock.tick(FPS)

    mouse_pos = pygame.mouse.get_pos()
    mouse.set_new_mousePosition(mouse_pos)

    buttons.button_collisions(mouse_pos, mouse, click_sound)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pg.USEREVENT+1:
            load_bars.addRect(20, 36)
            load_text.change_frame()
        elif event.type == pg.USEREVENT + 2:
            err_text.change_frame()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1 or event.key == pygame.K_ESCAPE:
                Menu(screen)
                running = False

    screen.fill(BLACK)

    pygame.draw.rect(screen, GREEN, (WIDTH//2-250, HEIGHT//2-25, 500, 50), 4) #draw load bar
    load_bars.draw(screen)

    load_text.draw(screen)
    err_text.draw(screen)

    if is_error_window:
        ErrWindow.draw(screen)
    screen.blit(mouse.image, mouse.rect)
    pygame.display.flip()