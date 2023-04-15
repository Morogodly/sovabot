import pygame as pg
import glob

import pygame.time

pygame.init()
class animation(pg.sprite.Sprite):
    def __init__(self, images, position, delay, uid):
        pg.sprite.Sprite.__init__(self)

        imgs = []
        for img in images:
            imgs.append(pg.image.load(img))

        self.image = imgs[0]
        self.now_frame = 0
        self.position = position
        self.frames = imgs
        self.uid = uid

        event = pg.event.Event(pg.USEREVENT+uid)
        pg.event.post(event)
        pygame.time.set_timer(event, delay)

    def change_frame(self):
        if self.now_frame<len(self.frames)-1:
            self.now_frame+=1
        else:
            self.now_frame = 1
        self.image = self.frames[self.now_frame]