import pyglet
import pymunk

class Bullet:
    def __init__(self, x, y, direction, space, batch):
        self.speed = 300
        self.body = pymunk.Body(1, float("inf"))
        self.body.position = x, y
        self.body.velocity = direction * self.speed
        self.shape = pymunk.Circle(self.body, 5)
        self.shape.collision_type = 2  # Тип коллизии для снаряда
        space.add(self.body, self.shape)
        self.sprite = pyglet.sprite.Sprite(
            img=pyglet.image.load('ASSETS/IMAGES/bullet.png'),
            x=x, y=y,
            batch=batch
        )
        self.sprite.scale = 0.5
        handler = space.add_collision_handler(2, 1)  # 2 - тип коллизии пули, 1 - тип коллизии игрока
        handler.begin = self.bullet_player_collision

    def update(self, dt):
        self.sprite.position = self.body.position.x, self.body.position.y, self.sprite.position[2]

    # Обработчик коллизий пуль и игрока
    def bullet_player_collision(self, arbiter, space, data):
        bullet_shape = arbiter.shapes[0]
        player_shape = arbiter.shapes[1]

        # Удаляем пулю из пространства и из списка пуль
        for enemy in map_data["enemies"]:
            for bullet in enemy.bullets:
                if bullet.shape == bullet_shape:
                    space.remove(bullet.body, bullet.shape)
                    enemy.bullets.remove(bullet)
                    break

        # Здесь можно добавить логику нанесения урона игроку
        print("Player hit by bullet!")
        return True