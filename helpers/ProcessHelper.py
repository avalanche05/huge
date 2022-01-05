import sys

import pygame

from constant import SETTINGS, SCREEN, BACKGROUND, FPS, CLOCK, DINO, ENEMIES, POLES, TREES, BARRIERS
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
        CLOCK.tick(FPS)
        pygame.display.flip()


def update_screen():
    CLOCK.tick(FPS)
    pygame.display.flip()


def game_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        DINO.update()
        ENEMIES.update()
        update_screen()
        draw_screen()


def draw_screen():
    SCREEN.fill(BACKGROUND)
    BARRIERS.draw(SCREEN)
    POLES.draw(SCREEN)
    TREES.draw(SCREEN)
    DINO.draw(SCREEN)
    ENEMIES.draw(SCREEN)
