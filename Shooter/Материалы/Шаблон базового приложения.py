import pyglet
import pymunk
import pymunk.pyglet_util

DRAW_OPTIONS = pymunk.pyglet_util.DrawOptions()


window = pyglet.window.Window(width=800, height=600)
main_batch = pyglet.graphics.Batch()
space = pymunk.Space()
space.gravity = 0, 1


@window.event
def on_draw():
    window.clear()
    space.debug_draw(DRAW_OPTIONS)
    main_batch.draw()

def update(dt):
    pass

def fixed_update(dt):
    space.step(dt)

pyglet.clock.schedule(update)
pyglet.clock.schedule(fixed_update)
pyglet.app.run()