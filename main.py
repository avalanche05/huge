import pygame

from classes.ChooseButton import ChooseButton
from classes.Dino import Dino
from classes.Enemy import Enemy
from classes.FunctionalButton import FunctionalButton
from classes.TextButton import TextButton
from constant import HEIGHT, WIDTH, START_SPRITES, SETTINGS_SPRITES, BIRDS, DINO, \
    GAME_TITLE
from helpers.GenerationHelper import generate_level
from helpers.ProcessHelper import game_window, terminate, started_window

pygame.init()

FunctionalButton('Play', (WIDTH // 2, HEIGHT // 2), START_SPRITES, function=game_window)
TextButton('Name', (WIDTH // 2, HEIGHT // 2 - 100), SETTINGS_SPRITES, start_text='user')
ChooseButton('Difficult', (WIDTH // 2, HEIGHT // 2), SETTINGS_SPRITES, args=['<Easy>', '<Hard>'])
FunctionalButton('Quit', (WIDTH // 2, HEIGHT // 2 + 100), SETTINGS_SPRITES, function=terminate)

Dino((100, 0), DINO)


def main():
    pygame.display.set_caption(GAME_TITLE)
    generate_level()
    started_window()


if __name__ == '__main__':
    main()
