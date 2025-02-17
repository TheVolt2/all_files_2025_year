import pyglet
import pymunk
from Enemy import Enemy


class KARTA_ZAGRUZOCHNIK:
    def __init__(self, window, batch, space):
        self.window = window
        self.batch = batch
        self.space = space

        # костыль, чтобы сборщик мусора не удалял спрайты, НЕ ТРОГАТЬ!!!!
        self.sprites_crutch = []

    def load(self, file_path, wall_sprite: pyglet.image.AbstractImage, enemy_sprite: pyglet.image.AbstractImage = None):
        cell_size = 1

        map_file = open(file_path, 'r', encoding='utf-8')
        line = map_file.readline()
        while not "KARTA" in line:
            if "RAZMER_STEN" in line:
                cell_size = int(line.split(":")[1])

            line = map_file.readline()

        map_data = dict()
        map_data["enemies"] = []

        map_file.readline()

        x = 0
        y = self.window.height
        for line in map_file.readlines():
            for symbol in line:
                if symbol == '#':
                    body = pymunk.Body(1000, float("inf"), pymunk.Body.KINEMATIC)
                    body.position = (x, y)
                    shape = pymunk.Poly.create_box(body, (cell_size, cell_size))
                    wall_sprite.anchor_x = wall_sprite.width // 2
                    wall_sprite.anchor_y = wall_sprite.height // 2
                    sprite = pyglet.sprite.Sprite(wall_sprite, x, y, batch=self.batch)
                    sprite.scale_x = cell_size / wall_sprite.width
                    sprite.scale_y = cell_size / wall_sprite.height


                    self.space.add(body, shape)
                    self.sprites_crutch.append(sprite)

                elif symbol == 'E' and enemy_sprite is not None:
                    enemy = Enemy(enemy_sprite, self.space, x, y, batch=self.batch)
                    self.sprites_crutch.append(enemy)
                    if "enemies" in map_data:
                        map_data["enemies"].append(enemy)
                    else:
                        map_data["enemies"] = [enemy]

                elif symbol == "P":
                    map_data["player_position"] = x, y

                x += cell_size

            x = 0
            y -= cell_size

        return map_data