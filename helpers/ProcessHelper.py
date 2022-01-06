import sys
from random import randint, randrange

import pygame

from classes.Barrier import Barrier
from classes.ChooseButton import ChooseButton
from classes.Dino import Dino
from classes.Enemy import Enemy
from classes.FunctionalButton import FunctionalButton
from classes.Pole import Pole
from classes.TextButton import TextButton
from constant import SETTINGS, SCREEN, BACKGROUND, FPS, CLOCK, DINO, ENEMIES, POLES, TREES, BARRIERS, \
    HEIGHT, PLATFORM_SPRITE_LENGTH, SPEED_BOOST, WIDTH, SETTINGS_SPRITES, GENERATE_CHANCE, BLACK
from helpers.GenerationHelper import generate_level
from widgets import settings


def terminate():
    """Выход из игры"""
    pygame.quit()
    sys.exit()


def started_window():
    """Работа стартового окна"""

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
        if not randrange(0, 1 // enemy_chance) and is_generate_correct():
            Enemy((WIDTH, HEIGHT - 600), -(platform_speed + 240) // FPS, ENEMIES, is_start=True)

    def generate_barriers():
        # генерация барьера происходит случайно
        if not randrange(0, 1 // barrier_chance) and is_generate_correct():
            barrier = Barrier((WIDTH, HEIGHT - 580), BARRIERS)
            barrier.move(randint(0, 15))

    # инициализация спрайтов
    username_button = TextButton('Name', (WIDTH // 2, HEIGHT // 2 - 100), SETTINGS_SPRITES,
                                 start_text='user')
    difficult_button = ChooseButton('Difficult', (WIDTH // 2, HEIGHT // 2), SETTINGS_SPRITES,
                                    args=['<Easy>', '<Medium>', '<Hard>'])
    FunctionalButton('Quit', (WIDTH // 2, HEIGHT // 2 + 100), SETTINGS_SPRITES, function=terminate)
    dino = Dino((100, HEIGHT - 570), DINO, is_start=True)
    platform_1 = Pole((0, HEIGHT - 500), PLATFORM_SPRITE_LENGTH, POLES, start_pos=0)
    platform_2 = Pole((0, HEIGHT - 500), PLATFORM_SPRITE_LENGTH, POLES, start_pos=0)
    # инициализация переменных
    difficult_degree = difficult_button.get_text()
    barrier_chance, enemy_chance = GENERATE_CHANCE[difficult_degree][:2]
    current_x = 0
    platform_speed = 600
    is_step = False
    is_dino_dead = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if not is_step and event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_UP, pygame.K_DOWN):
                difficult_degree = difficult_button.get_text()
                barrier_chance, enemy_chance = GENERATE_CHANCE[difficult_degree][:2]
                is_step = True
            if not is_step:
                settings.position().update(event)
                SETTINGS.update(event)
            if is_dino_dead and event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE,):
                game_window(difficult_degree)
        if is_dino_dead:
            continue
        # генерация объектов
        generate_barriers()
        generate_enemies()

        # обновление координат всех объектов
        update_platform()
        BARRIERS.update(platform_speed // FPS)

        if is_step:
            is_dino_dead = DINO.update(False, False, False, False)
            platform_speed += SPEED_BOOST
        else:
            is_up = is_barrier_near(100) and is_enemy_near(200) or is_barrier_near(
                20) or is_barrier_near(150) and is_enemy_near(150)
            is_down = is_enemy_near(30) and dino.fly_height() < 100 and not is_barrier_near(50)
            DINO.update(is_up, is_down, False, False)

        ENEMIES.update()

        # изменение текущего положение всех объектов
        current_x -= platform_speed // FPS
        current_x %= PLATFORM_SPRITE_LENGTH

        draw_screen()
        if not is_step:
            SETTINGS.draw(SCREEN)
            settings.position().draw(SCREEN)
        update_screen()


def update_screen():
    CLOCK.tick(FPS)
    pygame.display.flip()


def game_window(difficult_degree):
    barrier_chance, max_enemy_count = GENERATE_CHANCE[difficult_degree][2:]
    generate_level(barrier_chance, max_enemy_count)
    is_dino_dead = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if is_dino_dead and event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE,):
                generate_level(barrier_chance, max_enemy_count)
                is_dino_dead = False
        if is_dino_dead:
            continue
        is_dino_dead = DINO.update()
        ENEMIES.update()
        draw_screen()
        update_screen()


def draw_screen():
    SCREEN.fill(BACKGROUND)
    BARRIERS.draw(SCREEN)
    POLES.draw(SCREEN)
    TREES.draw(SCREEN)
    DINO.draw(SCREEN)
    ENEMIES.draw(SCREEN)
