import os
import sys
from random import randint, choice

import pygame

pygame.init()
SIZE = WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode(SIZE)
ENEMY_SPEED = 5
DINO_SPEED = 10
FPS = 60
CLOCK = pygame.time.Clock()
PLACE_IN_IMAGE = {'Enemy': [[2, 1, 260, 0, 444, 100, 50, 50]],
                  'Dino': [[6, 1, 1678, 0, 2208, 100, 88, 100],
                           [2, 1, 2209, 0, 2445, 100, 118, 100]],
                  'Pole': [[1, 1, 0, 100, 2446, 130, 2446, 30]],
                  'Tree': [[6, 1, 446, 0, 650, 73, 40, 70]]}
SETTINGS = pygame.sprite.Group()
START_SPRITES = pygame.sprite.Group()
SETTINGS_SPRITES = pygame.sprite.Group()
POLES = pygame.sprite.Group()
TREES = pygame.sprite.Group()
BIRDS = pygame.sprite.Group()
DINO = pygame.sprite.Group()
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
BACKGROUND = pygame.Color(247, 247, 247)


def load_image(name: str, colorkey=None):
    """Скачивание изображения"""
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    """Выход из игры"""
    pygame.quit()
    sys.exit()


def cut_sheet(sheet, value):
    states = []
    for columns, rows, start_x, start_y, stop_x, stop_y, width, height in value:
        rect = pygame.Rect(0, 0, (stop_x - start_x) // columns,
                           (stop_y - start_y) // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (start_x + rect.w * i, start_y + rect.h * j)
                states.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)), (width, height)))
    return states


class Dino(pygame.sprite.Sprite):
    """Друг(диинозаврик)"""
    image = load_image('all_dino_sprites.png', WHITE)

    def __init__(self, pos: tuple, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.situations = {'stay': [0, 0], 'run': [2, 3], 'sit': [6, 7], 'dead': [4, 4]}
        self.states = cut_sheet(Dino.image, PLACE_IN_IMAGE['Dino'])
        self.cur_state = 0
        self.step = 10
        self.jump_step = -15
        self.vertical_speed = 0
        self.gravity = 1
        self.flip = False
        self.image = self.states[self.situations['stay'][0]]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        keys = pygame.key.get_pressed()
        situation = 'stay'
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.step
            situation = 'run'
            self.flip = True
        if keys[pygame.K_RIGHT]:
            situation = 'run'
            self.rect.x += self.step
            self.flip = False
        if keys[pygame.K_UP]:
            for sprite in POLES:
                if pygame.sprite.collide_mask(self, sprite):
                    self.vertical_speed = self.jump_step
                    break
        if keys[pygame.K_DOWN]:
            situation = 'sit'
            for sprite in POLES:
                if pygame.sprite.collide_mask(self, sprite):
                    break
            else:
                self.vertical_speed += 5
        self.image = pygame.transform.flip(
            self.states[self.situations[situation][self.cur_state // (FPS // DINO_SPEED)]],
            self.flip, False)
        if self.vertical_speed < 0:
            self.rect.y += self.vertical_speed
        else:
            for _ in range(self.vertical_speed):
                for sprite in POLES:
                    if pygame.sprite.collide_mask(self, sprite):
                        break
                else:
                    self.rect.y += 1
        for sprite in POLES:
            if pygame.sprite.collide_mask(self, sprite):
                self.vertical_speed = 0
                break
        else:
            self.vertical_speed += self.gravity
        self.cur_state += 1
        self.cur_state %= FPS // DINO_SPEED * 2


class Enemy(pygame.sprite.Sprite):
    """Враг(птичка)"""
    image = load_image('all_dino_sprites.png', WHITE)

    def __init__(self, pos: tuple, direction: int, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.states = cut_sheet(Enemy.image, PLACE_IN_IMAGE['Enemy'])
        self.cur_state = 0
        self.image = self.states[self.cur_state]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.direction = direction
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        self.rect.x += self.direction
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            self.rect.x -= self.direction
            self.direction *= -1
            for i in range(len(self.states)):
                self.states[i] = pygame.transform.flip(self.states[i], True, False)
        self.cur_state += 1
        self.cur_state %= FPS // ENEMY_SPEED * 2
        self.image = self.states[self.cur_state // (FPS // ENEMY_SPEED)]


class Pole(pygame.sprite.Sprite):
    """Жёрдочка"""
    image = load_image('all_dino_sprites.png', WHITE)

    def __init__(self, pos: tuple, length: int, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        raw = cut_sheet(Enemy.image, PLACE_IN_IMAGE['Pole'])[0]
        start_pos = randint(0, raw.get_width() - length)
        self.image = raw.subsurface(pygame.Rect(start_pos, 0, length, 30))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Tree(pygame.sprite.Sprite):
    """Дерево"""
    image = load_image('all_dino_sprites.png', WHITE)

    def __init__(self, pos: tuple, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image = choice(cut_sheet(Enemy.image, PLACE_IN_IMAGE['Tree']))
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


class Button(pygame.sprite.Sprite):
    """Базовый класс любой кнопки"""

    def __init__(self, text: str, pos: tuple, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.text = text
        self.x, self.y = pos

    def update_text(self, text, bg):
        # текст
        font = pygame.font.Font(None, 60)
        self.render_text = font.render(text, True, BLACK)
        # размеры
        self.size = self.render_text.get_size()
        self.size = self.size[0] + 16, self.size[1] + 4
        self.rect = pygame.Rect(self.x - self.size[0] // 2, self.y - self.size[1] // 2, *self.size)
        # итоговая картинка
        self.image = pygame.Surface(self.size)
        self.image.fill(bg)
        self.image.fill(BACKGROUND, rect=(2, 2, self.size[0] - 4, self.size[1] - 4))
        self.image.blit(self.render_text, (8, 2))


class TextButton(Button):
    """Кнопка ввода информации"""

    def __init__(self, text: str, pos: tuple, *groups: pygame.sprite.Group, start_text: str):
        super().__init__(text, pos, *groups)
        self.added_text = start_text
        self.activated = False
        self.update_text(self.text + ': ' + self.added_text, BLACK)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.activated = True
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                not self.rect.collidepoint(args[0].pos):
            self.activated = False
        if args and args[0].type == pygame.KEYDOWN and self.activated:
            if args[0].key == pygame.K_RETURN:
                self.activated = False
            elif args[0].key == pygame.K_BACKSPACE:
                self.added_text = self.added_text[:-1]
            else:
                self.added_text += args[0].unicode if args[0].unicode.isalnum() or args[
                    0].unicode == ' ' else ''
        self.update_text(self.text + ': ' + self.added_text, BLACK)


class ChooseButton(Button):
    """Кнопка выбора определённого параметра"""

    def __init__(self, text: str, pos: tuple, *groups: pygame.sprite.Group, args: iter):
        super().__init__(text, pos, *groups)
        self.arguments = args
        self.cur_argument = 0
        self.activated = False
        self.update_text(self.text + ': ' + str(self.arguments[self.cur_argument]), BLACK)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.activated = True
            self.cur_argument += 1
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                not self.rect.collidepoint(args[0].pos):
            self.activated = False
        if args and args[0].type == pygame.KEYDOWN and self.activated:
            if args[0].key == pygame.K_RETURN:
                self.activated = False
            elif args[0].key == pygame.K_LEFT:
                self.cur_argument -= 1
            elif args[0].key == pygame.K_RIGHT:
                self.cur_argument += 1
        self.cur_argument %= len(self.arguments)
        self.update_text(self.text + ': ' + str(self.arguments[self.cur_argument]), BLACK)


class FunctionalButton(Button):
    """Кнопка, выполняющая определённую функцию при нажатии"""

    def __init__(self, text: str, pos: tuple, *groups: pygame.sprite.Group, function):
        super().__init__(text, pos, *groups)
        self.function = function
        self.update_text(self.text, BLACK)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.function()


def started_window():
    """Работа стартового окна"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            settings.position().update(event)
            SETTINGS.update(event)
        SCREEN.fill(BACKGROUND)
        SETTINGS.draw(SCREEN)
        settings.position().draw(SCREEN)
        CLOCK.tick(FPS)
        pygame.display.flip()


def game_window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        SCREEN.fill(BACKGROUND)
        POLES.draw(SCREEN)
        TREES.draw(SCREEN)
        DINO.update()
        DINO.draw(SCREEN)
        BIRDS.update()
        BIRDS.draw(SCREEN)
        CLOCK.tick(FPS)
        pygame.display.flip()


settings = Settings((WIDTH - 64, 0), SETTINGS)
FunctionalButton('Play', (WIDTH // 2, HEIGHT // 2), START_SPRITES, function=game_window)
TextButton('Name', (WIDTH // 2, HEIGHT // 2 - 100), SETTINGS_SPRITES, start_text='user')
ChooseButton('Difficult', (WIDTH // 2, HEIGHT // 2), SETTINGS_SPRITES, args=['<Easy>', '<Hard>'])
FunctionalButton('Quit', (WIDTH // 2, HEIGHT // 2 + 100), SETTINGS_SPRITES, function=terminate)
Enemy((0.15, 0), -10, BIRDS)
Dino((100, 0), DINO)
Pole((0, 300), 1920, POLES)
Pole((200, 1005), 200, POLES)
Tree((10, 230), TREES)


def main():
    started_window()


if __name__ == '__main__':
    main()
