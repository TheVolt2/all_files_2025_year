import math

import pyglet
import pymunk


class Projectile(pyglet.sprite.Sprite):
    def __init__(self, img, space, x, y, z, angle, speed, batch):
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        super().__init__(img, x, y, z, batch=batch)

        self.angle = angle

        self.dx = speed * math.cos(angle)
        self.dy = speed * math.sin(angle)

        self.speed = speed

    def update(self, dt):
        self.x += self.dx
        self.y += self.dy