import pygame

from constant import PLACE_IN_IMAGE, WHITE
from helpers.DataHelper import load_image, cut_sheet


class Cloud(pygame.sprite.Sprite):
    """Облако"""
    image = load_image('all_dino_sprites.png', WHITE)

    def __init__(self, pos: tuple, speed, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.states = cut_sheet(Cloud.image, PLACE_IN_IMAGE['Cloud'])
        self.image = self.states[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()
        self.speed = speed
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        self.rect.x += self.speed
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.x < -100:
            self.kill()

    def move(self, y):
        self.rect.y += y
