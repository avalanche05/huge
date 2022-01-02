from random import randint

import pygame

from classes.Barrier import Barrier
from classes.Dino import Dino
from classes.Enemy import Enemy
from classes.Pole import Pole
from constant import HEIGHT, POLES, DINO, BIRDS, CLOCK, BARRIERS, FPS, SCREEN, \
    BACKGROUND, WIDTH, PLATFORM_SPRITE_LENGTH, PLATFORM_SPEED
from helpers.ProcessHelper import draw_screen, update_screen, terminate

BARRIER_CHANCE = 1 / 300
ENEMY_CHANCE = 1 / 400


def is_barrier_near():
    """функция проверяет наличие препятсвия на расстоянии 30 пикселей от игрока"""
    for barrier in BARRIERS:
        if barrier.rect.x - dino.rect.x <= dino.rect.width + 30 and barrier.rect.x > dino.rect.x:
            return True

    return False


def update_platform():
    """функция двигает платформу на константную скорость"""
    platform_1.rect.x = current_x
    platform_2.rect.x = current_x - PLATFORM_SPRITE_LENGTH


def generate_enemies():
    # генерация врага происходит случайно
    if not randint(0, int(1 / ENEMY_CHANCE)):
        Enemy((WIDTH, HEIGHT - 580), -PLATFORM_SPEED // FPS, BIRDS, is_start=True)


def generate_barriers():
    # генерация барьера происходит случайно
    if not randint(0, int(1 / BARRIER_CHANCE)):
        Barrier((WIDTH, HEIGHT - 580), BARRIERS)


# инициализация спрайтов
dino = Dino((100, HEIGHT - 570), DINO, is_start=True)
platform_1 = Pole((0, HEIGHT - 500), PLATFORM_SPRITE_LENGTH, POLES, start_pos=0)
platform_2 = Pole((0, HEIGHT - 500), PLATFORM_SPRITE_LENGTH, POLES, start_pos=0)
# инициализация переменных
current_x = 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

    if is_barrier_near():
        dino.update(up=True)

    # генерация объектов
    generate_barriers()
    generate_enemies()

    # обновление координат всех объектов
    update_platform()
    BARRIERS.update(PLATFORM_SPEED // FPS)
    DINO.update()
    BIRDS.update()

    # изменение текущего положение всех объектов
    current_x -= PLATFORM_SPEED // FPS
    current_x %= PLATFORM_SPRITE_LENGTH

    draw_screen()
    update_screen()
