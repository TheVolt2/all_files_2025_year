import pyglet
import pymunk
import pymunk.pyglet_util
from pyglet.gl import GL_NEAREST, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER
from pyglet.gl.gl_compat import GL_TEXTURE_2D

from Player import Player

window = pyglet.window.Window(1280, 720, vsync=False)
main_batch = pyglet.graphics.Batch()
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

space = pymunk.Space()
space.gravity = 0, -999
draw_options = pymunk.pyglet_util.DrawOptions()

dino_sprites = pyglet.image.ImageGrid(pyglet.image.load("DinoSprites - mort.png"), 1, 24)
dino_animation = pyglet.image.Animation.from_image_sequence(dino_sprites, duration=0.05, loop=True)

player = Player(dino_animation, space, keys, 640, 100, 0, (120, 120), batch=main_batch)

platform_body_static = pymunk.Body(body_type=pymunk.Body.STATIC)
platform_body_static.position = 640, 50
platform_shape_static = pymunk.Poly.create_box(platform_body_static, (400, 50))
space.add(platform_body_static, platform_shape_static)

platform_body_kinematic = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
platform_body_kinematic.position = 400, 200
platform_shape_kinematic = pymunk.Poly.create_box(platform_body_kinematic, (200, 30))
space.add(platform_body_kinematic, platform_shape_kinematic)

platform_speed = 100
platform_direction = 1

grass_sound = pyglet.media.load("shagi-po-trave-minecraft.wav", streaming=False)
metal_sound = pyglet.media.load("jixaw-metal-pipe-falling-sound.wav", streaming=False)

player_collision_type = 1
grass_platform_collision_type = 2
metal_platform_collision_type = 3

platform_shape_static.collision_type = grass_platform_collision_type
platform_shape_kinematic.collision_type = metal_platform_collision_type

def handle_grass_collision(arbiter, space, data):
    grass_sound.play()
    return True

def handle_metal_collision(arbiter, space, data):
    metal_sound.play()
    return True

space.add_collision_handler(player_collision_type, grass_platform_collision_type).begin = handle_grass_collision
space.add_collision_handler(player_collision_type, metal_platform_collision_type).begin = handle_metal_collision

@window.event
def on_draw():
    window.clear()
    pyglet.gl.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    pyglet.gl.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    main_batch.draw()
    space.debug_draw(draw_options)

def update(dt):
    player.update(dt)
    global platform_direction
    platform_body_kinematic.position += pymunk.Vec2d(platform_direction * platform_speed * dt, 0)
    if platform_body_kinematic.position.x > 800 or platform_body_kinematic.position.x < 200:
        platform_direction *= -1

def fixed_update(dt):
    space.step(dt)

pyglet.clock.schedule_interval(fixed_update, 1 / 120)
pyglet.clock.schedule(update)
pyglet.app.run()
