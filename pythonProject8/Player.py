import pygame as pg


def get_axis(negative, positive):
    return int(positive) - int(negative)


class Player:
    def __init__(self, pos, size, color):
        self.rect = pg.Rect(pos, size)
        self.color = color

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)

    def move(self):
        keys = pg.key.get_pressed()

        self.rect.x += get_axis(keys[pg.K_a], keys[pg.K_d])
        self.rect.y += get_axis(keys[pg.K_w], keys[pg.K_s])
