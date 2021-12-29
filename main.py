import os
import sys

import pygame

pygame.init()
SIZE = WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode(SIZE)
SPEED = 5
FPS = 60
CLOCK = pygame.time.Clock()
PLACE_IN_IMAGE = {'Enemy': [[2, 1, 260, 0, 444, 100]]}
SETTINGS = pygame.sprite.Group()
START_SPRITES = pygame.sprite.Group()
SETTINGS_SPRITES = pygame.sprite.Group()
BIRDS = pygame.sprite.Group()
BLACK = pygame.Color(0, 0, 0)
BACKGROUND = pygame.Color(247, 247, 247)


def load_image(name: str, colorkey: int = None):
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


def cut_sheet(sheet, value, width, height):
    states = []
    for columns, rows, start_x, start_y, stop_x, stop_y in value:
        rect = pygame.Rect(0, 0, (stop_x - start_x) // columns,
                           (stop_y - start_y) // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (start_x + rect.w * i, start_y + rect.h * j)
                states.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)), (width, height)))
    return states


class Enemy(pygame.sprite.Sprite):
    """Враг(птичка)"""
    image = load_image('all_dino_sprites.png')

    def __init__(self, pos: tuple, direction: int, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.states = cut_sheet(Enemy.image, PLACE_IN_IMAGE['Enemy'], 50, 50)
        self.cur_state = 0
        self.image = self.states[self.cur_state]
        self.rect = self.image.get_rect()
        self.direction = direction
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        self.rect.x += self.direction
        if self.rect.x <= 0 or self.rect.x >= WIDTH - 50:
            self.rect.x -= self.direction
            self.direction *= -1
            for i in range(len(self.states)):
                self.states[i] = pygame.transform.flip(self.states[i], True, False)
        self.cur_state += 1
        self.cur_state %= FPS // SPEED * 2
        self.image = self.states[self.cur_state // (FPS // SPEED)]


class Settings(pygame.sprite.Sprite):
    """Настроки"""
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
        BIRDS.update()
        BIRDS.draw(SCREEN)
        CLOCK.tick(FPS)
        pygame.display.flip()


settings = Settings((WIDTH - 64, 0), SETTINGS)
FunctionalButton('Play', (WIDTH // 2, HEIGHT // 2), START_SPRITES, function=game_window)
TextButton('Name', (WIDTH // 2, HEIGHT // 2 - 100), SETTINGS_SPRITES, start_text='user')
ChooseButton('Difficult', (WIDTH // 2, HEIGHT // 2), SETTINGS_SPRITES, args=['<Easy>', '<Hard>'])
FunctionalButton('Quit', (WIDTH // 2, HEIGHT // 2 + 100), SETTINGS_SPRITES, function=terminate)


def main():
    started_window()


if __name__ == '__main__':
    main()
