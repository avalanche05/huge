import os
import sys
import pygame

pygame.init()
SIZE = WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode(SIZE)
SETTINGS = pygame.sprite.Group()
START_SPRITES = pygame.sprite.Group()
SETTINGS_SPRITES = pygame.sprite.Group()
BLACK = (0, 0, 0)


def load_image(name, colorkey=None):
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


def draw(screen):
    screen.fill('#c0e6d7')
    # font = pygame.font.Font(None, 50)
    # text = font.render("the huge.", True, 'black')
    # text_x = WIDTH // 2 - text.get_width() // 2
    # text_y = HEIGHT // 2 - text.get_height() // 2
    # screen.blit(text, (text_x, text_y))


class Settings(pygame.sprite.Sprite):
    settings = load_image("gear.png")
    close = load_image("close.png")

    def __init__(self, pos, *groups):
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
    def __init__(self, text, pos, *groups):
        super().__init__(*groups)
        self.text = text
        self.x, self.y = pos

    def update_text(self, text, bg):
        # текст
        font = pygame.font.Font(None, 60)
        self.render_text = font.render(text, True, 'black')
        # размеры
        self.size = self.render_text.get_size()
        self.size = self.size[0] + 16, self.size[1] + 4
        self.rect = pygame.Rect(self.x - self.size[0] // 2, self.y - self.size[1] // 2, *self.size)
        # итоговая картинка
        self.image = pygame.Surface(self.size)
        self.image.fill(bg)
        self.image.fill('#c0e6d7', rect=(2, 2, self.size[0] - 4, self.size[1] - 4))
        self.image.blit(self.render_text, (8, 2))

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            pass


class TextButton(Button):
    def __init__(self, text, pos, *groups, start_text):
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
    def __init__(self, text, pos, *groups, args):
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
    def __init__(self, text, pos, *groups, function):
        super().__init__(text, pos, *groups)
        self.function = function
        self.update_text(self.text, BLACK)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.function()


def terminate():
    pygame.quit()
    sys.exit()


def started_window():
    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            settings.position().update(event)
            SETTINGS.update(event)
        draw(SCREEN)
        SETTINGS.draw(SCREEN)
        settings.position().draw(SCREEN)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


settings = Settings((WIDTH - 64, 0), SETTINGS)
FunctionalButton('Play', (WIDTH // 2, HEIGHT // 2), START_SPRITES, function=terminate)
TextButton('Name', (WIDTH // 2, HEIGHT // 2 - 100), SETTINGS_SPRITES, start_text='user')
ChooseButton('Difficult', (WIDTH // 2, HEIGHT // 2), SETTINGS_SPRITES, args=['<Easy>', '<Hard>'])
FunctionalButton('Quit', (WIDTH // 2, HEIGHT // 2 + 100), SETTINGS_SPRITES, function=terminate)


def main():
    started_window()


if __name__ == '__main__':
    main()
