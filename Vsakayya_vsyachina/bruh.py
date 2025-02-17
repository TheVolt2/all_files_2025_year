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

img = pyglet.image.load('Steam_icon_logo.svg.png')
player = Player(img, space, WIDTH / 2, HEIGHT / 2, 0, (60, 60), batch=main_batch, friction=0.5)

key = None


def add_springboard(x1, y1, x2, y2):
    line_shape = pymunk.Segment(platforms_body, (x1, y1), (x2, y2), 2)
    line_shape.friction = 1
    line_shape.elasticity = 0.5
    space.add(platforms_body, line_shape)

add_springboard(320, 600, 600, 550)

@window.event
def on_key_press(symbol, modifiers):
    print(Player.wasd_keys(symbol, modifiers, key))


@window.event
def on_draw():
    window.clear()
    fps.draw()
    space.debug_draw(draw_options)
    (main_batch.draw())


@window.event
def update(dt):
    space.step(dt)
    player.update()






pyglet.clock.schedule(update)
pyglet.app.run(interval=1 / 120)