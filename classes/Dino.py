import pygame

from constant import WHITE, PLACE_IN_IMAGE, DINO_SPEED, FPS, WIDTH, HEIGHT
from globals import poles, enemies, barriers
from helpers.DataHelper import load_image, cut_sheet


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
        self.is_dead = False

        self.start_y = pos[1]

    def set_dead(self):
        self.image = pygame.transform.flip(self.states[self.situations['dead'][0]], self.flip, False)
        self.vertical_speed = 0

    def set_on_pole(self):
        is_up = self.cross(poles)
        while self.cross(poles):
            self.rect.y -= 1
        if is_up:
            self.rect.y += 1

    def start_update(self, up, down, left, right):
        situation = 'run'

        if down:
            situation = 'sit'
            if not self.cross(poles):
                self.vertical_speed += 5
        if up:
            if self.cross(poles):
                self.vertical_speed = self.jump_step
        self.image = self.states[self.situations[situation][self.cur_state // (FPS // DINO_SPEED)]]
        self.mask = pygame.mask.from_surface(self.image)

        if self.vertical_speed < 0:
            self.rect.y += self.vertical_speed
        else:
            self.rect.y = min(self.rect.y + self.vertical_speed, self.start_y)
        if not self.cross(poles):
            self.vertical_speed += self.gravity
        self.cur_state += 1
        self.cur_state %= FPS // DINO_SPEED * 2
        if self.cross(enemies) or self.cross(barriers):
            self.set_dead()
            return True
        return False

    def level_update(self, up, down, left, right):
        situation = 'stay'
        if left:
            situation = 'run'
            self.rect.x -= self.step
            if self.cross(enemies) or self.cross(barriers):
                self.set_dead()
                return True
            self.flip = True
        if right:
            situation = 'run'
            self.rect.x += self.step
            if self.cross(enemies) or self.cross(barriers):
                self.set_dead()
                return True
            self.flip = False
        if up:
            if self.cross(poles):
                self.vertical_speed = self.jump_step
        if down:
            situation = 'sit'
            if not self.cross(poles):
                self.vertical_speed += 5
        self.image = pygame.transform.flip(
            self.states[self.situations[situation][self.cur_state // (FPS // DINO_SPEED)]],
            self.flip, False)
        self.mask = pygame.mask.from_surface(self.image)
        if self.vertical_speed < 0:
            for _ in range(abs(self.vertical_speed)):

                if self.cross(enemies) or self.cross(barriers):
                    self.set_dead()
                    return True

                self.rect.y -= 1
                if self.cross(poles):
                    self.vertical_speed = 0
                    self.rect.y += 1
                    break
        else:
            for _ in range(self.vertical_speed):

                if self.cross(enemies) or self.cross(barriers):
                    self.set_dead()
                    return True

                self.rect.y += 1
                if self.cross(poles):
                    self.vertical_speed = 0
                    break
        self.set_on_pole()
        if not self.cross(poles):
            self.vertical_speed += self.gravity
        if self.rect.y + self.rect.height > HEIGHT:
            self.set_dead()
            return True
        self.rect.x = sorted([0, self.rect.x, WIDTH - self.rect.width])[1]
        self.cur_state += 1
        self.cur_state %= FPS // DINO_SPEED * 2
        return False

    def update(self, up=False, down=False, left=False, right=False, is_ai_play=False):
        if (self.cross(enemies) or self.cross(barriers)) and not is_ai_play:
            self.set_dead()
            return True
        keys = pygame.key.get_pressed()
        up |= keys[pygame.K_UP]
        down |= keys[pygame.K_DOWN]
        left |= keys[pygame.K_LEFT]
        right |= keys[pygame.K_RIGHT]
        if self.is_start:
            return self.start_update(up, down, left, right)
        else:
            return self.level_update(up, down, left, right)

    def fly_height(self):
        return self.start_y - self.rect.y

    def cross(self, group):
        """метод проверяет пересечение спрайта Dino с любым из спрайтов группы group"""

        for sprite in group:
            if pygame.sprite.collide_mask(self, sprite):
                return True
        return False
