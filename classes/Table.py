import os

import pygame

from constant import BLACK, TEXT_COLOR
from helpers.DataBaseHelper import get_best_score_top


class Table:
    def __init__(self, x=0, y=0, width=0, height=0, screen=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.top = []
        self.ratio = (1, 8, 3)

    def resize(self, width, height):
        self.width = width
        self.height = height

    def move(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        raw = sorted(get_best_score_top(), key=lambda x: x['best_score'], reverse=True)
        self.top = list(filter(lambda x: x[1] != 0, map(lambda x: (x['username'], x['best_score']), raw[:5])))

    def render(self):
        font = pygame.font.Font(os.path.abspath('data/font.ttf'), 32)
        for i in range(min(5, len(self.top))):
            pygame.draw.rect(self.screen, BLACK,
                             (self.x + sum(self.ratio[:0]) * self.width, self.y + i * self.height,
                              self.ratio[0] * self.width, self.height), 1)
            text = font.render(str(i + 1), True, TEXT_COLOR)
            self.screen.blit(text, (self.x + sum(self.ratio[:0]) * self.width + (self.ratio[0] * self.width - text.get_width()) // 2, self.y + i * self.height))
            pygame.draw.rect(self.screen, BLACK,
                             (self.x + sum(self.ratio[:1]) * self.width, self.y + i * self.height,
                              self.ratio[1] * self.width, self.height), 1)
            text = font.render(self.top[i][0], True, TEXT_COLOR)
            self.screen.blit(text, (self.x + sum(self.ratio[:1]) * self.width + (self.ratio[1] * self.width - text.get_width()) // 2, self.y + i * self.height))
            pygame.draw.rect(self.screen, BLACK,
                             (self.x + sum(self.ratio[:2]) * self.width, self.y + i * self.height,
                              self.ratio[2] * self.width, self.height), 1)
            text = font.render(str(self.top[i][1]).rjust(5, '0'), True, TEXT_COLOR)
            self.screen.blit(text, (self.x + sum(self.ratio[:2]) * self.width + (self.ratio[2] * self.width - text.get_width()) // 2, self.y + i * self.height))
