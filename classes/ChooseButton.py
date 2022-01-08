import pygame

from classes.Button import Button
from constant import SETTINGS_TEXT_COLOR


class ChooseButton(Button):
    """Кнопка выбора определённого параметра"""

    def __init__(self, text: str, pos: tuple, *groups: pygame.sprite.Group, args: iter):
        super().__init__(text, pos, *groups)
        self.arguments = args
        self.cur_argument = 0
        self.activated = False
        self.update_text(self.text + ': ' + str(self.arguments[self.cur_argument]),
                         SETTINGS_TEXT_COLOR)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.activated = True
            self.cur_argument += 1
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                not self.rect.collidepoint(args[0].pos):
            self.activated = False
        if args and args[0].type == pygame.KEYDOWN and self.activated:
            if args[0].key == pygame.K_RETURN:
                self.activated = False
            elif args[0].key == pygame.K_LEFT:
                self.cur_argument -= 1
            elif args[0].key == pygame.K_RIGHT:
                self.cur_argument += 1
        self.cur_argument %= len(self.arguments)
        self.update_text(self.text + ': ' + str(self.arguments[self.cur_argument]),
                         SETTINGS_TEXT_COLOR)
