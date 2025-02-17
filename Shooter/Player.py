import pyglet
import pymunk
from pyglet.gl import GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.graphics import Batch, Group
from pyglet.image import AbstractImage, Animation
from pyglet.graphics.shader import ShaderProgram


class Player(pyglet.sprite.Sprite):
    def __init__(self,
                 img: AbstractImage | Animation, space: pymunk.Space,
                 x: float = 0, y: float = 0, z: float = 0,
                 blend_src: int = GL_SRC_ALPHA,
                 blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
                 batch: Batch | None = None,
                 group: Group | None = None,
                 subpixel: bool = False,
                 program: ShaderProgram | None = None) -> None:
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        super().__init__(img, x, y, z,
                         blend_src, blend_dest,
                         batch, group,
                         subpixel,
                         program)

        self.body = pymunk.Body(1000, float("inf"))
        self.body.position = (x, y)
        self.hit_box = pymunk.Poly.create_box(self.body, (img.width, img.height))
        space.add(self.body, self.hit_box)  # ✅ Добавляем корректно (тело + хитбокс)

        # словаь имеет структуру: [СОСТОЯНИЕ][Таблица спрайтов][индекс спрайта] или [СОСТОЯНИЕ][Скорость анимации]
        self.sprites = dict()
        self.current_state = "IDLE"
        self.animation_index = 0
        self.animation_speed = 5

    def update(self, x: float | None = None, y: float | None = None, z: float | None = None,
               rotation: float | None = None, scale: float | None = None,
               scale_x: float | None = None, scale_y: float | None = None, dt: float = None) -> None:
        self.update_animation(dt)
        self.position = (self.body.position[0], self.body.position[1], self.position[2])

    def update_animation(self, dt):
        prev_index = int(self.animation_index)
        self.animation_index += dt * self.animation_speed
        if self.animation_index >= len(self.sprites[self.current_state]["sprites"]):
            self.animation_index = 0
        if int(self.animation_index) != prev_index:
            new_sprite: pyglet.sprite.Sprite = self.sprites[self.current_state]["sprites"][int(self.animation_index)]
            new_sprite.anchor_x = new_sprite.width // 2
            new_sprite.anchor_y = new_sprite.height // 2
            self.image = self.sprites[self.current_state]["sprites"][int(self.animation_index)]

    def change_state(self, state: str) -> None:
        self.current_state = state
        self.animation_index = 0
        self.animation_speed = self.sprites[self.current_state]["animation_speed"]

    def update_hit_box(self, space: pymunk.Space):
        width = self.image.width #* self.scale_x  # Учитываем масштаб
        height = self.image.height #* self.scale_y  # Учитываем масштаб

        space.remove(self.hit_box)  # Удаляем только хитбокс, не тело
        self.hit_box = pymunk.Poly.create_box(self.body, (width, height))  # Создаем новый хитбокс
        space.add(self.hit_box)  # Добавляем новый хитбокс обратно

    def add_sprites(self, state_key: str, images: pyglet.image.ImageGrid, animation_speed: int = 5):
        self.sprites[state_key] = {
            "sprites": images,
            "animation_speed": animation_speed
        }