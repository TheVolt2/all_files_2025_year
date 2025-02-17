import pyglet
from pyglet.window import key, mouse
import pymunk
from pymunk import pyglet_util
from random import randint
from PhysicSprite import PhysicsSprite
from Player import Player

WIDTH, HEIGHT = 1280, 720
window = pyglet.window.Window(WIDTH, HEIGHT, vsync=False)
keys = key.KeyStateHandler()
window.push_handlers(keys)
main_batch = pyglet.graphics.Batch()

fps = pyglet.window.FPSDisplay(window)

space = pymunk.Space()
space.gravity = 0, -999
draw_options = pyglet_util.DrawOptions()

floor_body_down = pymunk.Body(body_type=pymunk.Body.STATIC)
floor_body_down.position = (WIDTH / 2, 0)
floor_shape = pymunk.Poly.create_box(floor_body_down, (WIDTH, 30))
floor_shape.friction = 1
floor_shape.elasticity = 0.5
space.add(floor_body_down, floor_shape)

platforms_body = pymunk.body.Body(1, 9999, pymunk.Body.KINEMATIC)

img = pyglet.image.load('images (3).png')
img_2 = pyglet.image.load('images (5).jpeg')
print(img.width)
sprite = PhysicsSprite(img, space, WIDTH / 2, HEIGHT / 2, 0, (img.width, img.height),batch=main_batch, friction=0.5)

# Список для хранения всех физических спрайтов
sprites = []

def add_springboard(x1, y1, x2, y2):
    line_shape = pymunk.Segment(platforms_body, (x1, y1), (x2, y2), 2)
    line_shape.friction = 1
    line_shape.elasticity = 0.5
    space.add(platforms_body, line_shape)


add_springboard(320, 600, 600, 550)

label1 = pyglet.text.Label("Привет мир!", 0, HEIGHT / 2, 0,
                           font_name="Calibri",
                           font_size=100)


def spawn_box(x, y, size_x=20, size_y=20):
    body = pymunk.Body(1, 9999)
    body.position = (x, y)
    shape = pymunk.Poly.create_box(body, (size_x, size_y))
    shape.friction = 1
    shape.elasticity = 1
    space.add(body, shape)


def spawn_ball(x, y, radius=20, mass=1):
    moment = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, 9999)
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    shape.friction = 0.5
    shape.elasticity = 0.8
    space.add(body, shape)


@window.event
def on_draw():
    window.clear()
    fps.draw()
    #space.debug_draw(draw_options)
    main_batch.draw()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    # Добавляем новый PhysicsSprite при перетаскивании мыши
    new_sprite = PhysicsSprite(img_2, space, x, y, 0, (60, 30), batch=main_batch, friction=0.5)
    sprites.append(new_sprite)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.B:
        spawn_ball(window._mouse_x, window._mouse_y)
    if symbol == key.R:
        spawn_box(window._mouse_x, window._mouse_y, randint(5, 500), randint(5, 500))


def update(dt):
    space.step(dt)
    sprite.update()
    # Обновляем все созданные спрайты
    for spr in sprites:
        spr.update()


pyglet.clock.schedule(update)
pyglet.app.run(interval=1 / 120)
