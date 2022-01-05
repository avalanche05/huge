import pygame

from constant import GAME_TITLE
from helpers.ProcessHelper import started_window

pygame.init()


def main():
    pygame.display.set_caption(GAME_TITLE)
    started_window()


if __name__ == '__main__':
    main()
