import pygame as pg

screen = pg.display.set_mode((1280, 720))

player_rect = pg.Rect(120, 120, 50, 50)
player_speed = 0.5

frog_image = pg.image.load("frog.jpg").convert_alpha()
frog_image = pg.transform.scale(frog_image, (130, 120))

FPS = 14400
clock = pg.time.Clock()
delta_time = 1

frogs = []

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()

    if keys[pg.K_w]:
        player_rect.y -= 1 * delta_time
    if keys[pg.K_s]:
        player_rect.y += 1 * delta_time
    if keys[pg.K_a]:
        player_rect.x -= 1 * delta_time
    if keys[pg.K_d]:
        player_rect.x += 1 * delta_time

    if pg.mouse.get_pressed()[0]:
        frogs.append((frog_image, pg.mouse.get_pos()))

    pg.draw.rect(screen, (255, 0, 0), player_rect)
    screen.blit(frog_image, player_rect)

    for frog in frogs:
        screen.blit(frog[0], frog[1])

    pg.display.update()

    delta_time = clock.tick(FPS)
    print(len(frogs))

    screen.fill((0, 0, 0))

    pg.display.set_caption(str(clock.get_fps()))