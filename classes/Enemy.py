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
        self.image = pygame.transform.flip(self.states[self.cur_state], is_start, False)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(0, 0, self.image.get_width(), 1)
        self.direction = direction
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.is_start = is_start

    def start_update(self):
        self.rect.x += self.direction
        self.cur_state += 1
        self.cur_state %= FPS // ENEMY_SPEED * 2
        self.image = self.states[self.cur_state // (FPS // ENEMY_SPEED)]
        if self.rect.x < -100:
            self.kill()

    def level_update(self):
        self.rect.x += self.direction
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            self.rect.x -= self.direction
            self.direction *= -1
            for i in range(len(self.states)):
                self.states[i] = pygame.transform.flip(self.states[i], True, False)
        self.cur_state += 1
        self.cur_state %= FPS // ENEMY_SPEED * 2
        self.image = self.states[self.cur_state // (FPS // ENEMY_SPEED)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.is_start:
            self.start_update()
        else:
            self.level_update()
