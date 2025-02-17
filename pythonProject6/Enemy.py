import pyglet
import pymunk
from pyglet.gl import GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA
from pyglet.graphics import Batch, Group
from pyglet.image import AbstractImage, Animation
import math
from Bullet import Bullet


class Enemy(pyglet.sprite.Sprite):
    def __init__(self,
                 img: AbstractImage | Animation, space: pymunk.Space,
                 x: float = 0, y: float = 0, z: float = 0,
                 blend_src: int = GL_SRC_ALPHA,
                 blend_dest: int = GL_ONE_MINUS_SRC_ALPHA,
                 batch: Batch | None = None,
                 group: Group | None = None,
                 subpixel: bool = False,
                 window: pyglet.window.Window = None) -> None:
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        super().__init__(img, x, y, z,
                         blend_src, blend_dest,
                         batch, group,
                         subpixel)
        self.scale_x = 22 / self.image.width
        self.scale_y = 33 / self.image.width
        self.speed = 60
        self.detection_radius = 200  # Радиус обнаружения игрока
        self.shoot_cooldown = 1.0  # Время между выстрелами
        self.shoot_timer = 0.0
        self.body = pymunk.Body(1000, float("inf"))
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (220 * self.scale_x, 330 * self.scale_y))
        space.add(self.body, self.shape)
        self.space = space
        self.batch = batch
        self.window = window  # Сохраняем ссылку на окно
        self.sprites = dict()
        self.current_state = "IDLE"
        self.animation_index = 0
        self.animation_speed = 10
        self.bullets = []  # Список пуль врага

    def add_sprites(self, state_key: str, images: pyglet.image.ImageGrid, animation_speed: int = 5):
        """Добавляет анимации для указанного состояния."""
        self.sprites[state_key] = {
            "sprites": images,
            "animation_speed": animation_speed
        }

    def update(self, dt, player):
        self.position = self.body.position.x, self.body.position.y, self.position[2]
        self.move(dt, player)
        self.update_animation(dt)
        # Обновляем пули
        for bullet in self.bullets:
            bullet.update(dt)

    def move(self, dt, player):
        distance_to_player = math.sqrt((player.body.position.x - self.body.position.x) ** 2 +
                                       (player.body.position.y - self.body.position.y) ** 2)
        if distance_to_player < self.detection_radius:
            direction = pymunk.Vec2d(player.body.position.x - self.body.position.x,
                                     player.body.position.y - self.body.position.y).normalized()
            self.body.velocity = direction * self.speed
            if distance_to_player < 100 and self.shoot_timer <= 0:
                self.shoot(player)
                self.shoot_timer = self.shoot_cooldown
            else:
                self.shoot_timer = max(0, self.shoot_timer - dt)

    def shoot(self, player):
        print(f"Enemy at {self.body.position} shoots at player at {player.body.position}")
        direction = pymunk.Vec2d(player.body.position.x - self.body.position.x,
                                 player.body.position.y - self.body.position.y).normalized()
        bullet = Bullet(self.body.position.x, self.body.position.y, direction, self.space, self.batch)
        self.bullets.append(bullet)

    def update_animation(self, dt):
        if not self.sprites or self.current_state not in self.sprites:
            return

        prev_index = int(self.animation_index)
        self.animation_index += dt * self.animation_speed
        if self.animation_index >= len(self.sprites[self.current_state]["sprites"]):
            self.animation_index = 0
        if int(self.animation_index) != prev_index:
            new_sprite = self.sprites[self.current_state]["sprites"][int(self.animation_index)]
            new_sprite.anchor_x = new_sprite.width // 2
            new_sprite.anchor_y = new_sprite.height // 2
            self.image = new_sprite

    def change_state(self, state: str) -> None:
        if self.current_state != state and state in self.sprites:
            self.current_state = state
            self.animation_index = 0
            self.animation_speed = self.sprites[self.current_state]["animation_speed"]