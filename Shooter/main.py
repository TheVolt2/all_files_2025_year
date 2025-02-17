import pyglet
import pymunk
import pymunk.pyglet_util

from Player import Player

DRAW_OPTIONS = pymunk.pyglet_util.DrawOptions()


window = pyglet.window.Window(width=800, height=600)
main_batch = pyglet.graphics.Batch()
space = pymunk.Space()
space.gravity = 0, 0


player_idle_images = pyglet.image.ImageGrid(pyglet.image.load('Материалы/IDLE.png'), 1, 10, item_height=50)
player_run_images = pyglet.image.ImageGrid(pyglet.image.load('Материалы/RUN.png'), 1, 16)
player_start_image = player_idle_images[0]

player = Player(player_start_image, space, 120, 120, batch=main_batch)
player.scale = 3
# Состояние IDLE - должно быть настроено обязательно
player.add_sprites("IDLE", player_idle_images, 5)
player.add_sprites("RUN", player_run_images, 20)

#player.change_state("RUN") # Меняем состояние на бег
player.change_state("IDLE")  # Меняем состояние на стойку


@window.event
def on_draw():
    window.clear()
    space.debug_draw(DRAW_OPTIONS)
    main_batch.draw()

def update(dt):
    player.update(dt=dt)

def fixed_update(dt):
    space.step(dt)

pyglet.clock.schedule(update)
pyglet.clock.schedule(fixed_update)
pyglet.app.run()