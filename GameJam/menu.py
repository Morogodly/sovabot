import pygame
from const import *
from Buttons import *
from Animations import *
from pause import Pause
from game import Game


def test():
    print(1)

def settings():
    global my_position
    my_position = 1

def menu():
    global my_position
    my_position = 0


def makers():
    global my_position
    my_position = 2


def stop():
    global running
    running = False

def move_right():
    global music
    music.change_music()

def move_left():
    global music
    music.change_music(reverse=True)




def Menu(screen):
    global running, music, my_position
    def play():
        Game(screen)

    Vadim =global_font_20.render('Vadim', True, GREEN)
    Alex = global_font_20.render('Alex', True, GREEN)
    Nekich = global_font_20.render('Nekich', True, GREEN)
    Ksu = global_font_20.render('Ksu', True, GREEN)

    makers_names = [
        Maker(Vadim, global_font_15.render('leader vk.com/morogodly\nss', True, GREEN),(WIDTH//2-Vadim.get_size()[0]//2, 250)),
        Maker(Alex, global_font_15.render('coder vk.com/*****', True, GREEN), (WIDTH//2-Alex.get_size()[0]//2, 300)),
        Maker(Nekich, global_font_15.render('tester vk.com/*****', True, GREEN), (WIDTH//2-Nekich.get_size()[0]//2, 350)),
        Maker(Ksu, global_font_15.render('designer vk.com/*****', True, GREEN), (WIDTH//2-Ksu.get_size()[0]//2, 400)),
    ]


    music = Music(['music\load.mp3','music\Lo-Fi.mp3','music\8bit_bits.mp3','music\8bit-robocop.mp3','music\smile.mp3', "music\Dance.mp3", "music\phonk-remix.mp3"],
                  ['8-bit','Lo-Fi hip hop','8-bit bits','8-bit robocop','smile (8 bit)', "Dance", "Phonk Remix"],(400, 300), (303,25))

    background = pygame.image.load('background.png')
    mouse = Mouse(pygame.mouse.get_pos(), 'mouse\mouse.png')

    anims = []
    anims.append(
        animation(["anim\cat1.png", "anim\cat2.png", "anim\cat3.png", "anim\cat4.png", "anim\cat5.png"],(520, 150), 400, 1))

    maker_anim = animation(['capibara\c2.png','capibara\c1.png','capibara\c2.png','capibara\c1.png'], (500, 60), 700, 3)

    menu_buttons = Buttonss()
    menu_buttons.button_insert(
        Button(['menu_buttons\start_button.png'],play,(400, 130)),
        Button(['menu_buttons\makers_button.png'], makers, (400, 210)),
        Button(['menu_buttons\settings_button.png'], settings, (400, 290)),
        Button(['menu_buttons\exit_button.png'], stop, (400, 370))
    )

    back_buttons = Buttonss()
    back_buttons.button_insert(
        Button(['menu_buttons\close_button.png'], menu, (770, 120))
    )

    volume = Volume((400, 200), 303, 25)
    volume_text = global_font_20.render('Volume', True, GREEN)

    music_buttons = Buttonss()
    music_buttons.button_insert(
        Button(['menu_buttons\left_button.png'], move_left, (720, 300-2)),
        Button(['menu_buttons\Right_button.png'], move_right, (760, 300-2))
    )
    my_position = 0

    running = True
    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        mouse.set_new_mousePosition(mouse_pos)

        if my_position == 0:
            menu_buttons.button_collisions(mouse_pos, mouse, click_sound)
        elif my_position == 1:
            back_buttons.button_collisions(mouse_pos, mouse, click_sound)
            music_buttons.button_collisions(mouse_pos, mouse, click_sound)
            vol = volume.collision(mouse_pos)
            if vol != False:
                volume.set_volume(vol)
        elif my_position == 2:
            back_buttons.button_collisions(mouse_pos, mouse, click_sound)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif type(event.type) == int and event.type > pygame.USEREVENT:
                for a in anims:
                    if a.uid == event.type - pygame.USEREVENT:
                        a.change_frame()
                if maker_anim.uid == event.type - pygame.USEREVENT:
                    maker_anim.change_frame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if my_position != 0:
                        my_position = 0
                    else:
                        my_position = 1




        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        if my_position == 0:
            for i in anims:
                screen.blit(i.image, i.position)

            menu_buttons.button_painter(screen)
        elif my_position == 1:
            back_buttons.button_painter(screen)
            volume.draw(screen)
            screen.blit(volume_text, (400, 170))
            music.draw(screen)
            music_buttons.button_painter(screen)
        elif my_position == 2:
            back_buttons.button_painter(screen)
            screen.blit(maker_anim.image, maker_anim.position)

            for i in makers_names:
                i.draw(mouse_pos, screen, mouse)

        screen.blit(mouse.image, mouse.rect)
        pygame.display.flip()