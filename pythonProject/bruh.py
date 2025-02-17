import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions

window = pyglet.window.Window(800, 600, vsync=False)
space = pymunk.Space()
space.gravity = 0, -900
draw_options = DrawOptions()
sound_ding = pyglet.media.load("jixaw-metal-pipe-falling-sound.wav", streaming=False)


@window.event
def on_draw():
    window.clear()
    space.debug_draw(draw_options)


def fixed_update(dt):
    space.step(dt)


def floor_collision(arbiter, space, data):
    shape1, shape2 = arbiter.shapes
    body = shape1.body if shape1.body.position.y < shape2.body.position.y else shape2.body
    if body.velocity.y <= 0:
        body.velocity = (body.velocity.x, 200)
    print('Da')
    return True


def ball_collision(arbiter, space, data):
    player = pyglet.media.Player()
    # player.queue(sound_ding)
    player.play()
    pyglet.clock.schedule_once(lambda dt: player.delete(), sound_ding.duration)
    return True


floor_handler = space.add_collision_handler(0, 52)
floor_handler.begin = floor_collision

ball_handler = space.add_collision_handler(0, 0)
ball_handler.begin = ball_collision


def create_platform(a, b, width, colision):
    shape = pymunk.Segment(space.static_body, a, b, width)
    shape.elasticity = 1.0
    shape.collision_type = colision
    space.add(shape)


def create_ball(x, y, radius, collision_type=0):
    body = pymunk.Body(10, pymunk.moment_for_circle(10, 0, radius))
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.5
    shape.collision_type = collision_type
    space.add(body, shape)


def create_rectangle(x, y, width, height):
    body = pymunk.Body(10, pymunk.moment_for_box(10, (width, height)))
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.elasticity = 0.5
    space.add(body, shape)


def create_wall(a, b, width):
    shape = pymunk.Segment(space.static_body, a, b, width)
    shape.elasticity = 1.0
    space.add(shape)


create_platform((0, 0), (window.width, 0), 10, 52)
create_wall((0, 0), (0, window.height), 10)
create_wall((window.width, 0), (window.width, window.height), 10)
create_wall((0, window.height), (window.width, window.height), 10)
create_ball(200, 300, 20)
create_ball(600, 300, 30)
create_ball(400, 400, 25)
create_rectangle(300, 500, 50, 30)
create_rectangle(500, 450, 60, 40)
create_platform((0, 500), (window.width, 500), 10, 52)
create_ball(300, 550, 20, collision_type=0)
create_ball(500, 550, 20, collision_type=0)

pyglet.clock.schedule_interval(fixed_update, 1 / 120)
pyglet.app.run()
