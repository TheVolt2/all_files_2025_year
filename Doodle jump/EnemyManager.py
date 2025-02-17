# EnemyManager.py
import random
import pyglet
import pymunk


class EnemyManager:
    def __init__(self, space, window_size, batch):
        self.space = space
        self.window_size = window_size
        self.batch = batch
        self.enemies = []
        self.enemy_image = pyglet.image.load("enemy.png")  # Загрузите изображение врага

    def spawn_enemy(self, platform_position):
        """Создание врага."""
        enemy_size = (30, 30)
        enemy_body = pymunk.Body(10, float("inf"))
        enemy_body.position = platform_position
        enemy_shape = pymunk.Poly.create_box(enemy_body, enemy_size)
        enemy_shape.collision_type = 3  # Уникальный тип для врагов
        self.space.add(enemy_body, enemy_shape)

        enemy_sprite = pyglet.sprite.Sprite(self.enemy_image, platform_position[0], platform_position[1],
                                            batch=self.batch)
        enemy_sprite.scale_x = enemy_size[0] / self.enemy_image.width
        enemy_sprite.scale_y = enemy_size[1] / self.enemy_image.height
        self.enemies.append((enemy_body, enemy_sprite))

    def update(self, dt):
        """Обновление врагов."""
        for enemy_body, enemy_sprite in self.enemies:
            # Обновляем позицию спрайта, передавая только x и y
            enemy_sprite.position = enemy_body.position[0], enemy_body.position[1], 0
            enemy_body.velocity = (random.uniform(-100, 100), 0)  # Движение врага

    def remove_enemy(self, enemy):
        """Удаление врага."""
        for shape in enemy.shapes:
            self.space.remove(enemy, shape)
        for enemy_body, enemy_sprite in self.enemies:
            if enemy_body == enemy:
                enemy_sprite.delete()
                self.enemies.remove((enemy_body, enemy_sprite))
                break
