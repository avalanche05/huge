import pygame

from constant import PLACE_IN_IMAGE, POLES
from helpers.DataHelper import load_image, cut_sheet


class Portal(pygame.sprite.Sprite):
    """Портал"""
    image = load_image('portal.png', -1)

    def __init__(self, pos: tuple, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        raw = cut_sheet(Portal.image, PLACE_IN_IMAGE['Portal'])[0]
        self.image = raw
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def set_on_pole(self):
        is_up = self.cross(POLES)
        while self.cross(POLES):
            self.rect.y -= 1
        if is_up:
            self.rect.y += 1

    def cross(self, group):
        """метод проверяет пересечение спрайта Portal с любым из спрайтов группы group"""

        for sprite in group:
            if pygame.sprite.collide_mask(self, sprite):
                return True
        return False
