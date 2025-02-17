import math
import pyglet
import pymunk
from pyglet.gl import GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.graphics import Batch, Group
from pyglet.graphics.shader import ShaderProgram
from pyglet.image import AbstractImage, Animation
from PhysicSprite import PhysicsSprite


class Player(PhysicsSprite):
    def __init__(self,
                 img: AbstractImage | Animation, space: pymunk.Space,

                 x: float = 0, y: float = 0, z: float = 0,
                 size: tuple | list | None = None,
                 keys: int | None = None,
                 mass: float = 1, moment: float = 999,
                 elasticity: float = 0.5, friction: float = 0.5,
                 blend_src: int = GL_SRC_ALPHA,
                 blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
                 batch: Batch | None = None,
                 group: Group | None = None,
                 subpixel: bool = False,
                 program: ShaderProgram | None = None) -> None:
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2

        super().__init__(img, space, x, y, z, size, mass, moment, elasticity, friction
                         , blend_src, blend_dest, batch, group, subpixel, program)

        self.keys = keys
        self.key = None

    def update(self, x: float | None = None, y: float | None = None, z: float | None = None,
               rotation: float | None = None, scale: float | None = None,
               scale_x: float | None = None, scale_y: float | None = None) -> None:
        super().update(x, y, z, rotation, scale, scale_x, scale_y)
        self.position = (self.body.position.x, self.body.position.y, 0)
        self.rotation = -math.degrees(self.body.angle)
