import pygame

from constant import BACKGROUND, BLACK


class Button(pygame.sprite.Sprite):
    """Базовый класс любой кнопки"""

    def __init__(self, text: str, pos: tuple, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.text = text
        self.current_text = text
        self.x, self.y = pos

    def update_text(self, text, bg):
        self.current_text = text
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
