from random import randint

import pygame

from constant import PLACE_IN_IMAGE, WHITE
from helpers.DataHelper import load_image, cut_sheet


class Pole(pygame.sprite.Sprite):
    """Жёрдочка"""
    image = load_image('all_dino_sprites.png', WHITE)

    def __init__(self, pos: tuple, length: int, *groups: pygame.sprite.Group, start_pos=None):
        super().__init__(*groups)
        raw = cut_sheet(Pole.image, PLACE_IN_IMAGE['Pole'])[0]
        if start_pos is None:
            start_pos = randint(0, raw.get_width() - length)
        self.image = raw.subsurface(pygame.Rect(start_pos, 0, length, 30))
        self.mask = pygame.mask.from_surface(raw.subsurface(pygame.Rect(0, 0, length, 15)))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
