from random import choice, randrange
from const import  *
import pygame
import pygame as pg



def Pause(screen, mouse):
    class Symbol:
        def __init__(self, x, y, speed):
            self.x, self.y = x, y
            self.speed = speed
            self.value = choice(green_katakana)
            self.interval = randrange(20, 40)
            self.color = (30, randrange(60, 120),30)

        def draw(self, color):
            frames = pg.time.get_ticks()
            if not frames % self.interval:
                self.value = choice(green_katakana if color == 'green' else lightgreen_katakana)
            self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE
            surface.blit(self.value, (self.x, self.y))

    class SymbolColumn:
        def __init__(self, x, y):
            self.column_height = randrange(30, 50)
            self.speed = randrange(3, 5)
            self.symbols = [Symbol(x, i, self.speed) for i in range(y, y - FONT_SIZE * self.column_height, -FONT_SIZE-5)]

        def draw(self):
            [symbol.draw('green') if i else symbol.draw('lightgreen') for i, symbol in enumerate(self.symbols)]

    FONT_SIZE = 10
    alpha_value = 180


    surface = pg.Surface((WIDTH, HEIGHT))
    surface.set_alpha(alpha_value)

    katakana = [chr(int('0x30a0', 16) + i) for i in range(96)]
    font = pg.font.Font('fonts\miho.ttf', FONT_SIZE)
    green_katakana = [font.render(char, True, (30, randrange(60, 150), 30)) for char in katakana]
    lightgreen_katakana = [font.render(char, True, (40, 230, 40)) for char in katakana]

    symbol_columns = [SymbolColumn(x, randrange(-HEIGHT, 0)) for x in range(0, WIDTH, FONT_SIZE)]

    running = True


    while running:
        clock.tick(FPS)

        pos = pygame.mouse.get_pos()
        mouse.set_new_mousePosition(pos)


        for event in pg.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1 or event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pg.QUIT:
                running = False

        screen.blit(surface, (0, 0))
        surface.fill(pg.Color('black'))

        [symbol_column.draw() for symbol_column in symbol_columns]


        screen.blit(mouse.image, mouse.rect)

        pg.display.flip()