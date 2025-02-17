import pyglet
import pymunk
from pyglet.window import key
from PhysicsSprite import PhysicsSprite

def get_axis(neg, pos):
    return int(pos) - int(neg)

class Player(PhysicsSprite):
    def __init__(self,
                 img, space: pymunk.Space,
                 key_handler: pyglet.window.key.KeyStateHandler,
                 x=0, y=0, z=0,
                 size=None,
                 mass=1, moment=999,
                 elasticity=0.5, friction=0.5,
                 batch=None,
                 group=None):
        super().__init__(img, space, x, y, z, size, mass, moment, elasticity, friction, batch=batch, group=group)
        self.keys = key_handler
        self.move_speed = 220
        self.jump_height = 560
        self.can_jump = False
        self.ground_sensor = pymunk.Segment(self.body, (-size[0] // 2, -size[1] // 2),
                                            (size[0] // 2, -size[1] // 2), 2)
        self.ground_sensor.sensor = True
        self.ground_sensor.collision_type = 1
        space.add(self.ground_sensor)

    def move(self):
        direction = pymunk.Vec2d(
            get_axis(self.keys[key.A], self.keys[key.D]),
            0
        )
        self.body.velocity = (direction.x * self.move_speed, self.body.velocity.y)

    def jump(self):
        if self.can_jump:
            self.body.velocity = (self.body.velocity.x, self.jump_height)
            self.can_jump = False

    def update(self, dt):
        super().update()
        self.move()
        self.check_ground_collision()
        if self.keys[key.SPACE]:
            self.jump()

    def check_ground_collision(self):
        if abs(self.body.velocity.y) < 0.1:
            self.can_jump = True
        else:
            self.can_jump = False
