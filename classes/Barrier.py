from random import choice

import pygame

from constant import WHITE, PLACE_IN_IMAGE, POLES
from helpers.DataHelper import load_image, cut_sheet


class Barrier(pygame.sprite.Sprite):
    """Дерево"""
    image = load_image('all_dino_sprites.png', WHITE)

    def __init__(self, pos: tuple, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image = choice(cut_sheet(Barrier.image, PLACE_IN_IMAGE['Tree']))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        while True:
            for elem in POLES:
                if pygame.sprite.collide_mask(self, elem):
                    break
            else:
                self.rect.y += 1
                continue
            break
