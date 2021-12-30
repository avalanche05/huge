import pygame

from classes.Button import Button
from constant import BLACK


class TextButton(Button):
    """Кнопка ввода информации"""

    def __init__(self, text: str, pos: tuple, *groups: pygame.sprite.Group, start_text: str):
        super().__init__(text, pos, *groups)
        self.added_text = start_text
        self.activated = False
        self.update_text(self.text + ': ' + self.added_text, BLACK)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.activated = True
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                not self.rect.collidepoint(args[0].pos):
            self.activated = False
        if args and args[0].type == pygame.KEYDOWN and self.activated:
            if args[0].key == pygame.K_RETURN:
                self.activated = False
            elif args[0].key == pygame.K_BACKSPACE:
                self.added_text = self.added_text[:-1]
            else:
                self.added_text += args[0].unicode if args[0].unicode.isalnum() or args[
                    0].unicode == ' ' else ''
        self.update_text(self.text + ': ' + self.added_text, BLACK)
