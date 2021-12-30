import sys

import pygame

from constant import SETTINGS, SCREEN, BACKGROUND, FPS, CLOCK, DINO, BIRDS, POLES, TREES
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


def game_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        DINO.update()
        BIRDS.update()
        draw_screen()
        CLOCK.tick(FPS)
        pygame.display.flip()


def draw_screen():
    SCREEN.fill(BACKGROUND)
    POLES.draw(SCREEN)
    TREES.draw(SCREEN)
    DINO.draw(SCREEN)
    BIRDS.draw(SCREEN)
