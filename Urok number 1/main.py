import pygame as pg
from random import randint

pg.font.init()

axis_X = 1280
axis_Y = 720
screen = pg.display.set_mode((axis_X, axis_Y)) #Экран создали
screenfill_image = pg.image.load("images.jpg")
screenfill_image = pg.transform.scale(screenfill_image, (1280, 720))
screen_rect = pg.Rect(0, 0, 1280, 720)

screen_color = (0, 0, 0)

frog_rect = pg.Rect(120, 120, 130, 120)
player_speed = 0.5


frog_image = pg.image.load("frog-transformed.png")
frog_image = pg.transform.scale(frog_image, (130, 120))

steve_image = pg.image.load("img.png")
steve_image = pg.transform.scale(steve_image, (150, 300))
steve_rect = pg.Rect(240, 240, 150, 300)

emerald_image = pg.image.load("img_1.png")
emerald_image = pg.transform.scale(emerald_image, (130, 120))


emeralds = [pg.Rect(randint(0, 1150), randint(0, 600), 130, 120) for i in range(10)] #Добавил чат gpt
steve_score = 0
frog_score = 0


FPS = 60
clock = pg.time.Clock()
delta_time = 1

font_score = pg.font.SysFont("Calibri", 24)

frogs = []

checklist = 0

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()

    if keys[pg.K_w]:    # Управление лягухой
        frog_rect.y -= 1 * delta_time
    if keys[pg.K_s]:
        frog_rect.y += 1 * delta_time
    if keys[pg.K_a]:
        frog_rect.x -= 1 * delta_time
    if keys[pg.K_d]:
        frog_rect.x += 1 * delta_time

    if keys[pg.K_UP]:   # Управление стивом
        steve_rect.y -= 1 * delta_time
    if keys[pg.K_DOWN]:
        steve_rect.y += 1 * delta_time
    if keys[pg.K_LEFT]:
        steve_rect.x -= 1 * delta_time
    if keys[pg.K_RIGHT]:
        steve_rect.x += 1 * delta_time

    for emerald in emeralds:
        if emerald.colliderect(frog_rect):
            frog_score += 1
            emeralds.remove(emerald)
            break

        if emerald.colliderect(steve_rect):
            steve_score += 1
            emeralds.remove(emerald)
            break


    screen.blit(screenfill_image, screen_rect)
    pg.draw.rect(screen, screen_color, steve_rect, 1)
    pg.draw.rect(screen, screen_color, frog_rect, 1)
    screen.blit(frog_image, frog_rect)
    screen.blit(steve_image, steve_rect)


    for emerald in emeralds:
        screen.blit(emerald_image, emerald)


    for frog in frogs:
        screen.blit(frog[0], frog[1])

    steve_label = font_score.render(str(steve_score), True, (255, 255, 255))
    screen.blit(steve_label, (0, 0))

    frog_label = font_score.render(str(frog_score), True, (255, 255, 255))
    screen.blit(frog_label, (24, 0))


    pg.display.update()

    delta_time = clock.tick(FPS)
    #print(len(frogs))



    screen.fill(screen_color)


    pg.display.set_caption(str(clock.get_fps()))

print("Счёт:", checklist)