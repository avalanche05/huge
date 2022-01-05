import sys

import pygame

from constant import SETTINGS, SCREEN, BACKGROUND, FPS, CLOCK, DINO, ENEMIES, POLES, TREES, BARRIERS
from helpers.GenerationHelper import generate_level
from widgets import settings


def terminate():
    """Выход из игры"""
    pygame.quit()
    sys.exit()


def started_window():
    """Работа стартового окна"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            settings.position().update(event)
            SETTINGS.update(event)
        SCREEN.fill(BACKGROUND)
        SETTINGS.draw(SCREEN)
        settings.position().draw(SCREEN)
        update_screen()


def update_screen():
    CLOCK.tick(FPS)
    pygame.display.flip()


def game_window():
    is_dino_dead = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if is_dino_dead and event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE,):
                generate_level()
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
