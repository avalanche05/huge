import pygame

from constant import START_SPRITES, SETTINGS_SPRITES
from helpers.DataHelper import load_image


class Settings(pygame.sprite.Sprite):
    """Настройки"""
    settings = load_image("gear.png")  # шестерёнка
    close = load_image("close.png")  # крестик

    def __init__(self, pos: tuple, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image = Settings.settings
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            if self.image == Settings.settings:
                self.image = Settings.close
            else:
                self.image = Settings.settings

    def position(self):
        return START_SPRITES if self.image == Settings.settings else SETTINGS_SPRITES
