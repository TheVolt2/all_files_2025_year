import pyglet

WIDTH, HEIGHT = 1280, 720
window = pyglet.window.Window(WIDTH, HEIGHT, caption='bruh', resizable=True, vsync=False)

fps = pyglet.window.FPSDisplay(window)

@window.event
def on_draw():
    window.clear()
    fps.draw()

@window.event
def on_mouse_motion(x: int, y: int, dx: int, dy: int):

    None

pyglet.app.run(interval=1/5000)