import pygame

from constant import WHITE, PLACE_IN_IMAGE, POLES, DINO_SPEED, FPS, WIDTH
from helpers.DataHelper import load_image, cut_sheet
from helpers.ProcessHelper import draw_screen


class Dino(pygame.sprite.Sprite):
    """Друг(диинозаврик)"""
    image = load_image('all_dino_sprites.png', WHITE)

    def __init__(self, pos: tuple, *groups: pygame.sprite.Group, is_start=False):
        super().__init__(*groups)
        self.situations = {'stay': [0, 0], 'run': [2, 3], 'sit': [6, 7], 'dead': [4, 4]}
        self.states = cut_sheet(Dino.image, PLACE_IN_IMAGE['Dino'])
        self.cur_state = 0
        self.step = 10
        self.jump_step = -17 if is_start else -25
        self.vertical_speed = 0
        self.gravity = 1
        self.flip = False
        self.image = self.states[self.situations['stay'][0]]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()
        self.is_start = is_start
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.start_y = pos[1]

    def start_update(self, up, down, left, right):
        situation = 'run'

        if down:
            situation = 'sit'
            if not self.cross(POLES):
                self.vertical_speed += 5
        if up:
            if self.cross(POLES):
                self.vertical_speed = self.jump_step
        self.image = self.states[self.situations[situation][self.cur_state // (FPS // DINO_SPEED)]]

        if self.vertical_speed < 0:
            for _ in range(abs(self.vertical_speed)):
                self.rect.y -= 1
        else:
            for _ in range(abs(self.vertical_speed)):
                self.rect.y += 1
                if self.rect.y >= self.start_y:
                    self.rect.y = self.start_y
                    break
        if not self.cross(POLES):
            self.vertical_speed += self.gravity
        self.cur_state += 1
        self.cur_state %= FPS // DINO_SPEED * 2

    def level_update(self, up, down, left, right):
        situation = 'stay'
        if left:
            situation = 'run'
            flag = self.cross(POLES)
            self.rect.x -= self.step
            if self.cross(POLES) and not flag:
                self.rect.x += self.step
            self.flip = True
        if right:
            situation = 'run'
            flag = self.cross(POLES)
            self.rect.x += self.step
            if self.cross(POLES) and not flag:
                self.rect.x -= self.step
            self.flip = False
        if up:
            if self.cross(POLES):
                self.vertical_speed = self.jump_step
        if down:
            situation = 'sit'
            if not self.cross(POLES):
                self.vertical_speed += 5
        self.image = pygame.transform.flip(
            self.states[self.situations[situation][self.cur_state // (FPS // DINO_SPEED)]],
            self.flip, False)
        self.mask = pygame.mask.from_surface(self.image)
        if self.vertical_speed < 0:
            for _ in range(abs(self.vertical_speed)):
                self.rect.y -= 1
                if self.cross(POLES):
                    self.vertical_speed = 0
                    self.rect.y += 1
                    break
        else:
            for _ in range(abs(self.vertical_speed)):
                self.rect.y += 1
                if self.cross(POLES):
                    self.vertical_speed = 0
                    break
        is_up = False
        while self.cross(POLES):
            is_up = True
            self.rect.y -= 1
        if is_up:
            self.rect.y += 1
        if not self.cross(POLES):
            self.vertical_speed += self.gravity
        self.rect.x %= WIDTH
        self.cur_state += 1
        self.cur_state %= FPS // DINO_SPEED * 2

    def update(self, up=False, down=False, left=False, right=False):
        keys = pygame.key.get_pressed()
        up |= keys[pygame.K_UP]
        down |= keys[pygame.K_DOWN]
        left |= keys[pygame.K_LEFT]
        right |= keys[pygame.K_RIGHT]
        if self.is_start:
            self.start_update(up, down, left, right)
        else:
            self.level_update(up, down, left, right)

    def cross(self, group):
        """метод проверяет пересечение спрайта Dino с любым из спрайтов группы group"""

        for sprite in group:
            if pygame.sprite.collide_mask(self, sprite):
                return True
        return False
