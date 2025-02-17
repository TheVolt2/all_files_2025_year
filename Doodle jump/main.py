# main.py
import pyglet
import pymunk
import pymunk.pyglet_util
from Player import Player
from PlatformSpawner import PlatformSpawner
from EnemyManager import EnemyManager

# Инициализация окна и физических параметров
window = pyglet.window.Window(800, 600, vsync=False)
main_batch = pyglet.graphics.Batch()
space = pymunk.Space()
space.gravity = 0, -999

# Опции отладки
debug_draw_options = pymunk.pyglet_util.DrawOptions()

# Загрузка изображений
player_image = pyglet.image.load("doodle.png")
platform_image = pyglet.image.load("platform.png")
platform_brake_image = pyglet.image.load("platform_brake.png")  # Текстура для хрупкой платформы
background_image = pyglet.image.load("background.jpg")
background_image.anchor_x, background_image.anchor_y = 0, background_image.height // 2
background = pyglet.sprite.Sprite(background_image, x=0, y=0)
background.scale_x = 800 / background_image.width

# Инициализация игрока
player_size = (50, 50)
player = Player(player_image, space, player_size, 200, 250, batch=main_batch)

# Загрузка звука прыжка
jump_sound = pyglet.media.load("nebolshoy-zvuk-pryijka-kotoryiy-mojno-ispolzovat-dlya-vorchaniya-vo-vremya-pryijka.wav",
                               streaming=False)

# Создание менеджера платформd
platform_manager = PlatformSpawner(space, 1, 2, (800, 600), (85, 30), main_batch)
platform_manager.generate(platform_image, platform_brake_image, window.size, player.position, count=15)

# Создание менеджера врагов
enemy_manager = EnemyManager(space, window.size, main_batch)
enemy_manager.spawn_enemy((400, 300))  # Спавним первого врага

# Обработчики столкновений
handler = space.add_collision_handler(0, 1)  # Игрок и платформы
fragile_handler = space.add_collision_handler(0, 2)  # Игрок и хрупкие платформы
enemy_handler = space.add_collision_handler(0, 3)  # Игрок и враги


def on_player_hit_platform(arbiter, space, data):
    """Обработка столкновения игрока с платформой."""
    platform = arbiter.shapes[1]
    platform_position = platform.body.position
    platform_top = platform_position.y + platform.get_vertices()[0].y

    if player.body.velocity.y < 0 and player.body.position.y - player_size[1] // 2 > platform_top:
        player.body.velocity = (player.body.velocity.x, 800)
        jump_sound.play()
        return True
    return False


def on_player_hit_fragile_platform(arbiter, space, data):
    """Обработка столкновения игрока с хрупкой платформой."""
    if player.body.velocity.y < 0:
        player.body.velocity = (player.body.velocity.x, 800)
        jump_sound.play()
        for platform in platform_manager.platforms:
            if platform is arbiter.shapes[1].body:
                platform_manager.remove_platform(platform)
                return True
    return False


def on_player_hit_enemy(arbiter, space, data):
    """Обработка столкновения игрока с врагом."""
    global game_over
    game_over = True
    print("Game Over! You hit an enemy.")
    pyglet.app.exit()
    return False


# Назначение обработчиков столкновений
handler.pre_solve = on_player_hit_platform
fragile_handler.pre_solve = on_player_hit_fragile_platform
enemy_handler.pre_solve = on_player_hit_enemy

# Инициализация счётчика
score = 0
score_label = pyglet.text.Label(f"Score: {score}", font_name='Arial', font_size=18,
                                x=10, y=window.height - 30, anchor_x='left', anchor_y='top', color=(0, 0, 0, 255))

# Переменная для отслеживания состояния игры
game_over = False

# Линия проигрыша (на уровне нижней границы экрана)
lose_line_y = 0


def update(dt):
    """Обновление состояния игры."""
    global score, game_over, lose_line_y

    if game_over:
        return

    # Обновление игрока и врагов
    player.update(dt=dt)
    enemy_manager.update(dt)

    # Обновление двигающихся платформ
    platform_manager.update_moving_platforms(dt)

    # Обновление счёта
    score = max(score, int(player.body.position.y))
    score_label.text = f"Score: {score}"

    # Проверка на проигрыш
    if player.body.position.y < lose_line_y:
        game_over = True
        print("Game Over! Your score:", score)
        pyglet.app.exit()

    # Поднимаем линию проигрыша
    new_lose_line_y = player.body.position.y - window.height // 2
    if new_lose_line_y > lose_line_y:
        lose_line_y = new_lose_line_y

    # Генерация новых платформ, если их мало
    if len(platform_manager.platforms) < 16:
        platform_manager.generate(platform_image, platform_brake_image, window.size, player.position, count=15,
                                  offset_y=300)

    # Удаление платформ ниже линии проигрыша
    for platform in platform_manager.platforms[:]:
        if platform.position.y < lose_line_y:
            platform_manager.remove_platform(platform)

    # Обновление позиции фона и счётчика
    background.position = -90, player.position[1], 0
    score_label.position = -90, player.position[1] + 300, 0

    # Проверка границ экрана для игрока
    if player.body.position.x < -player.width * 2:
        player.body.position = (window.width - player.width / 2, player.body.position.y)
    elif player.body.position.x > window.width:
        player.body.position = (-player.width * 2, player.body.position.y)

    # Обновление камеры
    window.view = pyglet.math.Mat4()
    window.view = window.view.translate((90, -player.position[1] + window.height // 2, 0))


@window.event
def on_draw():
    """Отрисовка игры."""
    window.clear()
    background.draw()
    main_batch.draw()
    score_label.draw()


def fixed_update(dt):
    """Обновление физики."""
    space.step(dt)


@window.event
def on_key_press(symbol, modifiers):
    """Обработка нажатия клавиш."""
    if symbol == pyglet.window.key.A:
        player.body.velocity = (-300, player.body.velocity.y)
    elif symbol == pyglet.window.key.D:
        player.body.velocity = (300, player.body.velocity.y)
    elif symbol == pyglet.window.key.S:
        # Спавним платформу под игроком
        platform_manager.spawn_platform_under_player(player.body.position, platform_image)


@window.event
def on_key_release(symbol, modifiers):
    """Обработка отпускания клавиш."""
    if symbol in (pyglet.window.key.A, pyglet.window.key.D):
        player.body.velocity = (0, player.body.velocity.y)


# Планировщики обновлений
pyglet.clock.schedule_interval(fixed_update, 1 / 90)  # Физика
pyglet.clock.schedule_interval(update, 1 / 90)  # Логика игры
pyglet.app.run(interval=1 / 144)  # Запуск игры
