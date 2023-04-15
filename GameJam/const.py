import pygame
choise = [
    'game is running',
    'Null...',
    'Null...',
    'Null...',
    'The waiting time limit has been exceeded',
    'retring...',
    'retring...',
    'retring...',
    'The waiting time limit has been exceeded',
    'the error detection algorithm has been started',
    'work status:',
    '0%...',
    '4%...',
    '8%...',
    '12%...',
    '13%...',
    '18%...',
    '22%...',
    '25%...',
    '29%...',
    '33%...',
    '35%...',
    '39%...',
    '46%...',
    '49%...',
    '51%...',
    '62%...',
    '70%...',
    '75%...',
    '80%...',
    '88%...',
    '93%...',
    '99%...',
    'scan completed',
    '1 error was detected'
]
pygame.init()
FPS = 60
screen_size = WIDTH, HEIGHT = (1180, 720)
BLACK = (0, 0, 0)
GREEN = (109, 174, 129)
clock = pygame.time.Clock()
pygame.mixer.init()
click_sound = pygame.mixer.Sound('sounds\click.wav')
my_position = 0
global_font_20 = pygame.font.Font('fonts\Font.ttf', 20)
global_font_15 = pygame.font.Font('fonts\Font.ttf', 15)