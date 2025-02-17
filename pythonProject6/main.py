import pyglet
from pyglet.gl import *
import pymunk
import pymunk.pyglet_util
from pyglet.window import FPSDisplay

from GLOBAL import KEY_HANDLER, CAMERA_OFFSET
from Player import Player
from Enemy import Enemy
from KARTA_ZAGRUZKA import KARTA_ZAGRUZOCHNIK
from Bullet import Bullet  # Импортируем класс Bullet

DRAW_OPTIONS = pymunk.pyglet_util.DrawOptions()
window = pyglet.window.Window(width=800, height=600)
fps = FPSDisplay(window)
window.push_handlers(KEY_HANDLER)
main_batch = pyglet.graphics.Batch()
space = pymunk.Space()
space.gravity = 0, -1750

# Загрузка спрайтов
wall_sprite = pyglet.image.load('ASSETS/IMAGES/wall.png')
enemy_static_image = pyglet.image.load('ASSETS/IMAGES/Enemy.jpeg')  # Статическое изображение врага

# Загрузчик карты
map_loader = KARTA_ZAGRUZOCHNIK(window, main_batch, space)
map_data = map_loader.load("ASSETS/MAPS/MAP_1_UHAUHAUHAUAHUAHUHA", wall_sprite, enemy_static_image)

# Загрузка анимаций для игрока
player_idle_images = pyglet.image.ImageGrid(pyglet.image.load('ASSETS/IMAGES/IDLE.png'), 1, 10, item_height=65)
player_run_images = pyglet.image.ImageGrid(pyglet.image.load('ASSETS/IMAGES/RUN.png'), 1, 16, item_height=65)
player_start_image = player_idle_images[0]

# Создание игрока
player = Player(player_start_image, space, map_data["player_position"][0], map_data["player_position"][1], batch=main_batch)
player.scale = 3
player.add_sprites("IDLE", player_idle_images, 10)
player.add_sprites("RUN", player_run_images, 20)
window.push_handlers(player)

# Установка статического изображения для каждого врага
for enemy in map_data.get("enemies"):
    enemy.image = enemy_static_image  # Установите статическое изображение
    enemy.window = window  # Передаем объект окна каждому врагу

# Создание платформы
test_platform = pymunk.Poly.create_box(space.static_body, (800, 100))
space.add(test_platform)

# Обработчик коллизий пуль и игрока
def bullet_player_collision(arbiter, space, data):
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

# Добавляем обработчик коллизий
handler = space.add_collision_handler(2, 1)  # 2 - тип коллизии пули, 1 - тип коллизии игрока
handler.begin = bullet_player_collision

@window.event
def on_draw():
    window.clear()
    space.debug_draw(DRAW_OPTIONS)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    main_batch.draw()

def update(dt):
    player.update(dt=dt)
    window.view = pyglet.math.Mat4()

    CAMERA_OFFSET[0] = -player.position[0] + 300
    CAMERA_OFFSET[1] = -player.position[1] + 250

    window.view = window.view.translate(
        pyglet.math.Vec3(CAMERA_OFFSET[0], CAMERA_OFFSET[1], 0)  # Убедитесь, что z = 0
    )

    # Обновляем врагов и передаем игрока
    for enemy in map_data["enemies"]:
        enemy.update(dt, player)
        # Обновляем снаряды врага
        if hasattr(enemy, "bullets"):
            for bullet in enemy.bullets[:]:  # Используем копию списка для безопасного удаления
                bullet.update(dt)
                # Удаляем пулю, если она вышла за пределы экрана
                if not (0 < bullet.body.position.x < window.width and
                        0 < bullet.body.position.y < window.height):
                    enemy.bullets.remove(bullet)
                    space.remove(bullet.body, bullet.shape)

def fixed_update(dt):
    space.step(dt)

pyglet.clock.schedule(update)
pyglet.clock.schedule_interval(fixed_update, 1 / 120)
pyglet.app.run()