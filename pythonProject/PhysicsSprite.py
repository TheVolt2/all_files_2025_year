import math
import pyglet
import pymunk
from pyglet.graphics import Batch, Group


class PhysicsSprite(pyglet.sprite.Sprite):
    def __init__(self,
                 img, space: pymunk.Space,
                 x=0, y=0, z=0,
                 size=None,
                 mass=1, moment=999,
                 elasticity=0.5, friction=0.5,
                 batch: Batch = None,
                 group: Group = None) -> None:
        image = img.frames[0].image if isinstance(img, pyglet.image.Animation) else img
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        super().__init__(img, x, y, z, batch=batch, group=group)

        self.body = pymunk.Body(mass, moment)
        self.body.position = (x, y)
        self.width, self.height = size[0], size[1]
        self.scale_x = self.width / image.width
        self.scale_y = self.height / image.height
        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.elasticity = elasticity
        self.shape.friction = friction
        space.add(self.body, self.shape)
        self.z = z

    def update(self):
        self.position = (self.body.position.x, self.body.position.y, self.z)
        self.rotation = -math.degrees(self.body.angle)
