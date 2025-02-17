import pygame as pg

pg.font.init()

WIDTH, HEIGHT = 1280, 720
screen = pg.display.set_mode((WIDTH, HEIGHT))

player_rect = pg.Rect(200, 200, 100, 100)
player_direction = pg.math.Vector2(0, 0)

wall_rect_1 = pg.Rect(0, 570, 150, 150)
wall_rect_2 = pg.Rect(150, 420, 150, 150)
wall_rect_3 = pg.Rect(300, 270, 150, 150)
wall_rect_4 = pg.Rect(450, 120, 150, 150)

main_font = pg.font.SysFont("Arial", 20)

def get_axis(negative, positive):
    return int(positive) - int(negative)

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    pg.draw.rect(screen, (255, 0, 0), player_rect)
    pg.draw.rect(screen, (0, 255, 0), wall_rect_1)
    pg.draw.rect(screen, (0, 255, 0), wall_rect_2)
    pg.draw.rect(screen, (0, 255, 0), wall_rect_3)
    pg.draw.rect(screen, (0, 255, 0), wall_rect_4)

    keys = pg.key.get_pressed()

    player_direction = pg.Vector2(0, 0)
    player_direction.x = get_axis(keys[pg.K_a], keys[pg.K_d])
    player_direction.y = 0.5 + get_axis(keys[pg.K_w], keys[pg.K_s]) * 2
    player_rect.x += player_direction.x

    if player_rect.colliderect(wall_rect_1):
        if player_direction.x > 0:
            player_rect.right = wall_rect_1.left
        if player_direction.x < 0:
            player_rect.left = wall_rect_1.right

    player_rect.y += player_direction.y
    if player_rect.colliderect(wall_rect_1):
        if player_direction.y > 0:
            player_rect.bottom = wall_rect_1.top
        if player_direction.y < 0:
            player_rect.top = wall_rect_1.bottom

    player_rect.x += player_direction.x
    if player_rect.colliderect(wall_rect_2):
        if player_direction.x > 0:
            player_rect.right = wall_rect_2.left
        if player_direction.x < 0:
            player_rect.left = wall_rect_2.right

    player_rect.y += player_direction.y
    if player_rect.colliderect(wall_rect_2):
        if player_direction.y > 0:
            player_rect.bottom = wall_rect_2.top
        if player_direction.y < 0:
            player_rect.top = wall_rect_2.bottom

    player_rect.x += player_direction.x
    if player_rect.colliderect(wall_rect_3):
        if player_direction.x > 0:
            player_rect.right = wall_rect_3.left
        if player_direction.x < 0:
            player_rect.left = wall_rect_3.right

    player_rect.y += player_direction.y
    if player_rect.colliderect(wall_rect_3):
        if player_direction.y > 0:
            player_rect.bottom = wall_rect_3.top
        if player_direction.y < 0:
            player_rect.top = wall_rect_3.bottom

    player_rect.x += player_direction.x
    if player_rect.colliderect(wall_rect_4):
        if player_direction.x > 0:
            player_rect.right = wall_rect_4.left
        if player_direction.x < 0:
            player_rect.left = wall_rect_4.right

    player_rect.y += player_direction.y
    if player_rect.colliderect(wall_rect_4):
        if player_direction.y > 0:
            player_rect.bottom = wall_rect_4.top
        if player_direction.y < 0:
            player_rect.top = wall_rect_4.bottom

    screen.blit(
        main_font.render(f"Направление: {player_direction.x}; {player_direction.y}", True, (255, 255, 255)),
                (0, 0))

    pg.display.update()
    screen.fill((0, 0, 0))