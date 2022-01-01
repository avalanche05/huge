from random import choice, randint

import pygame

from constant import WHITE, PLACE_IN_IMAGE, POLES
from helpers.DataHelper import load_image, cut_sheet


class Barrier(pygame.sprite.Sprite):
    """Дерево"""
    image = load_image('all_dino_sprites.png', WHITE)

    def __init__(self, pos: tuple, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        size = randint(40, 70)
        self.image = pygame.transform.scale(choice(cut_sheet(Barrier.image, PLACE_IN_IMAGE['Tree'])),
                                            (size, size * 1.75))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        # while True:
        #     for elem in POLES:
        #         if pygame.sprite.collide_mask(self, elem):
        #             break
        #     else:
        #         self.rect.y += 1
        #         continue
        #     break

    def update(self, *args):
        self.rect.x -= int(args[0])
        if self.rect.x <= -123:
            self.kill()
        print(self.rect.x)
