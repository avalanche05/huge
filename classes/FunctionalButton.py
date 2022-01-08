import pygame

from classes.Button import Button
from constant import SETTINGS_TEXT_COLOR


class FunctionalButton(Button):
    """Кнопка, выполняющая определённую функцию при нажатии"""

    def __init__(self, text: str, pos: tuple, *groups: pygame.sprite.Group, function):
        super().__init__(text, pos, *groups)
        self.function = function
        self.update_text(self.text, SETTINGS_TEXT_COLOR)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.function()
