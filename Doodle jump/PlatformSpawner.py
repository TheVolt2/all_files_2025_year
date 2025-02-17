# PlatformSpawner.py
import random
import pyglet
import pymunk


class PlatformSpawner:
    def __init__(self, space, collision_type, breakable_collision_type, window_size, platform_size, batch):
        self.space = space
        self.collision_type = collision_type
        self.breakable_collision_type = breakable_collision_type
        self.window_size = window_size
        self.platform_size = platform_size
        self.batch = batch
        self.sprites = []
        self.platforms = []
        self.moving_platforms = []  # Список для хранения двигающихся платформs

    def spawn_platform(self, platform_point_position, platform_image: pyglet.image.AbstractImage, is_breakable=False,
                       is_moving=False):
        """Создание платформы."""
        platform_body = pymunk.Body(1000, float("inf"),
                                    body_type=pymunk.Body.KINEMATIC)
        platform_body.position = platform_point_position

        platform_shape = pymunk.Poly.create_box(platform_body, self.platform_size)
        platform_shape.collision_type = self.breakable_collision_type if is_breakable else self.collision_type
        self.space.add(platform_body, platform_shape)

        platform_image.anchor_x, platform_image.anchor_y = platform_image.width // 2, platform_image.height // 2
        platform_sprite = pyglet.sprite.Sprite(platform_image, platform_point_position[0], platform_point_position[1],
                                               1, batch=self.batch)
        platform_sprite.scale_x, platform_sprite.scale_y = self.platform_size[0] / platform_image.width, \
                                                           self.platform_size[1] / platform_image.height
        self.sprites.append(platform_sprite)
        self.platforms.append(platform_body)

        if is_moving:
            platform_body.velocity = (random.uniform(-100, 100), 0)  # Движение платформы
            self.moving_platforms.append(platform_body)  # Добавляем платформу в список двигающихся

    def spawn_platform_under_player(self, player_position, platform_image):
        """Создание платформы под игроком."""
        platform_x = player_position[0]  # Та же X-координата, что и у игрока
        platform_y = player_position[1] - 100  # Платформа на 100 пикселей ниже игрока
        self.spawn_platform((platform_x, platform_y), platform_image)

    def update_moving_platforms(self, dt):
        """Обновление позиции двигающихся платформ."""
        for platform in self.moving_platforms:
            # Если платформа достигает границы экрана, меняем направление
            if platform.position.x < 0 or platform.position.x > self.window_size[0]:
                platform.velocity = (-platform.velocity.x, 0)

    def generate(self, platform_image, breakable_image, window_size: tuple[int, int],
                 player_position: tuple[int, int, int], count=15,
                 offset_y=0):
        """Генерация платформ."""
        player_relative_point_y = int(player_position[1] + window_size[1] / 2)

        min_horizontal_distance = self.platform_size[0] * 1.5
        max_horizontal_distance = self.platform_size[0] * 2.5
        min_vertical_distance = self.platform_size[1] * 1.0
        max_vertical_distance = self.platform_size[1] * 1.5

        current_x = window_size[0] // 2
        current_y = player_relative_point_y - window_size[1] // 2 + offset_y

        for _ in range(count):
            horizontal_offset = random.uniform(min_horizontal_distance, max_horizontal_distance)
            vertical_offset = random.uniform(min_vertical_distance, max_vertical_distance)
            direction = random.choice([-1, 1])
            new_x = current_x + direction * horizontal_offset
            new_x = max(self.platform_size[0] // 2, min(new_x, window_size[0] - self.platform_size[0] // 2))
            new_y = current_y + vertical_offset

            platform_lot = random.randint(1, 3)
            if platform_lot == 1:
                self.spawn_platform((new_x, new_y), platform_image)
            elif platform_lot == 2:
                self.spawn_platform((new_x, new_y), breakable_image, is_breakable=True)
            else:
                self.spawn_platform((new_x, new_y), platform_image, is_moving=True)  # Спавним двигающуюся платформу

            current_x = new_x
            current_y = new_y

    def remove_platform(self, platform):
        """Удаление платформы."""
        for shape in platform.shapes:
            self.space.remove(platform, shape)
        self.platforms.remove(platform)
        if platform in self.moving_platforms:
            self.moving_platforms.remove(platform)  # Удаляем из списка двигающихся платформ
        for sprite in self.sprites:
            if sprite.x == platform.position.x and sprite.y == platform.position.y:
                sprite.delete()
                self.sprites.remove(sprite)
                break
