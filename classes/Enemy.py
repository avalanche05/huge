import pygame

from constant import PLACE_IN_IMAGE, WHITE, WIDTH, FPS, ENEMY_SPEED
from helpers.DataHelper import load_image, cut_sheet


class Enemy(pygame.sprite.Sprite):
    """Враг(птичка)"""
    image = load_image('all_dino_sprites.png', WHITE)

    def __init__(self, pos: tuple, direction: int, *groups: pygame.sprite.Group, is_start=False):
        super().__init__(*groups)
        self.states = cut_sheet(Enemy.image, PLACE_IN_IMAGE['Enemy'])
        self.cur_state = 0
        self.flip = direction > 0
        self.image = pygame.transform.flip(self.states[self.cur_state], self.flip, False)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.direction = direction
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.is_start = is_start

    def start_update(self):
        self.rect.x += self.direction
        self.cur_state += 1
        self.cur_state %= FPS // ENEMY_SPEED * 2
        self.image = self.states[self.cur_state // (FPS // ENEMY_SPEED)]
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.x < -100:
            self.kill()

    def level_update(self):
        self.rect.x += self.direction
        if self.rect.x < 0 or self.rect.x > WIDTH - self.rect.width:
            self.rect.x = sorted([0, self.rect.x, WIDTH - self.rect.w])[1]
            self.direction *= -1
            self.flip = not self.flip
        self.cur_state += 1
        self.cur_state %= FPS // ENEMY_SPEED * 2
        self.image = pygame.transform.flip(self.states[self.cur_state // (FPS // ENEMY_SPEED)],
                                           self.flip, False)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.is_start:
            self.start_update()
        else:
            self.level_update()
