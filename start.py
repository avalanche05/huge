from random import randint

import pygame

from classes.Barrier import Barrier
from classes.Dino import Dino
from classes.Enemy import Enemy
from classes.Pole import Pole
from constant import HEIGHT, POLES, DINO, ENEMIES, BARRIERS, FPS, WIDTH, PLATFORM_SPRITE_LENGTH, \
    SPEED_BOOST
from helpers.ProcessHelper import draw_screen, update_screen, terminate

BARRIER_CHANCE = 1 / 100
ENEMY_CHANCE = 1 / 300


def biggest_x():
    ans = -200

    for sprite in BARRIERS:
        ans = max(ans, sprite.rect.x)
    for sprite in ENEMIES:
        ans = max(ans, sprite.rect.x)

    return ans


def is_generate_correct():
    return biggest_x() < WIDTH - 400


def is_barrier_near(count):
    """функция проверяет наличие препятсвия на расстоянии count пикселей от игрока"""
    for barrier in BARRIERS:
        if barrier.rect.x - dino.rect.x <= dino.rect.width + count and barrier.rect.x > dino.rect.x:
            return True

    return False


def is_enemy_near(count):
    """функция проверяет наличие врага в радиусе count пикселей от игрока"""
    for enemy in ENEMIES:
        if enemy.rect.x - dino.rect.x <= dino.rect.width + count:
            return True

    return False


def update_platform():
    """функция двигает платформу на константную скорость"""
    platform_1.rect.x = current_x
    platform_2.rect.x = current_x - PLATFORM_SPRITE_LENGTH


def generate_enemies():
    # генерация врага происходит случайно
    if not randint(0, int(1 // ENEMY_CHANCE)) and is_generate_correct():
        Enemy((WIDTH, HEIGHT - 600), -(platform_speed + 240) // FPS, ENEMIES, is_start=True)


def generate_barriers():
    # генерация барьера происходит случайно
    if not randint(0, int(1 // BARRIER_CHANCE)) and is_generate_correct():
        barrier = Barrier((WIDTH, HEIGHT - 580), BARRIERS)
        barrier.move(randint(0, 15))


# инициализация спрайтов
dino = Dino((100, HEIGHT - 570), DINO, is_start=True)
platform_1 = Pole((0, HEIGHT - 500), PLATFORM_SPRITE_LENGTH, POLES, start_pos=0)
platform_2 = Pole((0, HEIGHT - 500), PLATFORM_SPRITE_LENGTH, POLES, start_pos=0)
# инициализация переменных
current_x = 0
platform_speed = 600
is_step = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_UP, pygame.K_DOWN):
            is_step = True

    # генерация объектов
    generate_barriers()
    generate_enemies()

    # обновление координат всех объектов
    update_platform()
    BARRIERS.update(platform_speed // FPS)
    if is_step:
        DINO.update(False, False, False, False)
        platform_speed += SPEED_BOOST
    else:
        is_up = is_barrier_near(100) and is_enemy_near(200) or is_barrier_near(
            20) or is_barrier_near(150) and is_enemy_near(150)
        is_down = is_enemy_near(30) and dino.fly_height() < 80 and not is_barrier_near(50)
        DINO.update(is_up, is_down, False, False)
    ENEMIES.update()

    # изменение текущего положение всех объектов
    current_x -= platform_speed // FPS
    current_x %= PLATFORM_SPRITE_LENGTH

    draw_screen()
    update_screen()
