
import pygame as pg
from random import randint

# Инициализация Pygame
pg.init()
pg.mixer.init()
pg.font.init()

# Загрузка звуков
miss_sound = pg.mixer.Sound('6_sto-k-odnomu-ne-pra_ilnyy-ot_e.mp3')  # Замените на путь к вашему звуковому файлу
hit_sound = pg.mixer.Sound('upali-dengi-na-igrovoy-schet.mp3')  # Замените на путь к вашему звуковому файлу
miss_sound.set_volume(0.1)
hit_sound.set_volume(0.1)

# Настройки экрана
axis_X = 1280
axis_Y = 720
screen = pg.display.set_mode((axis_X, axis_Y))  # Экран создали
screen_color = (0, 0, 0)

# Параметры монет
money_rects = [pg.Rect(randint(0, axis_X - 50), 0, 50, 50) for _ in range(5)]
money_die_platform = pg.Rect(0, 0, 400, 10)

# Скорость падения монет, устанавливаем значение 0.5
fall_speed = 0.5  # Падение монет в 4 раза медленнее первоначального значения

# Счет
score = 0

font_score = pg.font.SysFont("Calibri", 24)

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    # Получаем позицию мыши для платформы
    mouse_x, mouse_y = pg.mouse.get_pos()
    money_die_platform.center = (mouse_x, mouse_y)



    # Стираем экран
    screen.fill(screen_color)

    label = font_score.render(str(score), True, (255, 255, 255))
    screen.blit(label, (0, 0))

    # Двигаем монеты
    for money_rect in money_rects:
        money_rect.y += fall_speed  # Двигаем монету вниз

        # Если монета вышла за пределы экрана, воспроизводим звук и перемещаем её в верхнюю часть с новой рандомной позицией
        if money_rect.y > axis_Y:
            miss_sound.play()  # Воспроизводим звук, когда монета падает в нижней части экрана
            money_rect.x = randint(0, axis_X - 50)
            money_rect.y = 0
            score-=1

        # Проверяем столкновение с платформой
        if money_rect.colliderect(money_die_platform):
            hit_sound.play()  # Воспроизводим звук при столкновении с платформой
            score += 1  # Увеличиваем счет

            # Перемещаем монету обратно в верхнюю часть
            money_rect.x = randint(0, axis_X - 50)
            money_rect.y = 0

        # Рисуем монету
        pg.draw.rect(screen, (252, 186, 3), money_rect)

    label = font_score.render(str(score), True, (255, 255, 255))
    screen.blit(label, (0, 0))

    pg.draw.rect(screen, (255, 0, 0), money_die_platform)

    pg.display.update()


pg.quit()


print(f'Ваш счёт: {score}')
