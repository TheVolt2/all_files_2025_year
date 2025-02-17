# Player.py
import pyglet
import pymunk
from pyglet.gl import GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.graphics import Batch, Group
from pyglet.image import AbstractImage, Animation
from pyglet.graphics.shader import ShaderProgram


class Player(pyglet.sprite.Sprite):
    def __init__(self,
                 img: AbstractImage | Animation, space: pymunk.Space, size: tuple[float, float],
                 x: float = 0, y: float = 0, z: float = 0,
                 blend_src: int = GL_SRC_ALPHA,
                 blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
                 batch: Batch | None = None,
                 group: Group | None = None,
                 subpixel: bool = False,
                 program: ShaderProgram | None = None) -> None:
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2

        super().__init__(img, x, y, z, blend_src, blend_dest, batch, group, subpixel, program)

        self.scale_x = size[0] / self.image.width
        self.scale_y = size[1] / self.image.height

        self.body = pymunk.Body(100, float("inf"))
        self.body.position = (x, y)
        self.shape = pymunk.Poly.create_box(self.body, size)
        space.add(self.body, self.shape)

    def update(self, dt):
        """Обновление позиции игрока."""
        self.position = (self.body.position.x, self.body.position.y, self.position[2])
