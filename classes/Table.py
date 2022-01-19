import os

import pygame

from constant import BLACK, TEXT_COLOR, UUID
from helpers.DataBaseHelper import get_best_score_top


class Table:
    def __init__(self, x=0, y=0, width=0, height=0, screen=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.cur_index = 0
        self.cur_user = ''
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
        self.cur_index = raw.index([elem for elem in raw if elem['mac'] == UUID][0])
        self.cur_user = [raw[self.cur_index]['username'], raw[self.cur_index]['best_score'], raw[self.cur_index]['mac']]
        self.top = list(filter(lambda x: x[1] != 0, map(lambda x: (x['username'], x['best_score'], x['mac']), raw[:5])))

    def render(self):
        flag = False
        is_you = ''
        for i in range(min(5, len(self.top))):
            if self.top[i][2] == UUID:
                flag = True
                is_you = '(you)'

            font = pygame.font.Font(os.path.abspath('data/font.ttf'), 32)
            pygame.draw.rect(self.screen, BLACK,
                             (self.x + sum(self.ratio[:0]) * self.width, self.y + i * self.height,
                              self.ratio[0] * self.width, self.height), 1)
            text = font.render(str(i + 1), True, TEXT_COLOR)
            self.screen.blit(text, (
                self.x + sum(self.ratio[:0]) * self.width + (self.ratio[0] * self.width - text.get_width()) // 2,
                self.y + i * self.height))
            pygame.draw.rect(self.screen, BLACK,
                             (self.x + sum(self.ratio[:1]) * self.width, self.y + i * self.height,
                              self.ratio[1] * self.width, self.height), 1)
            text = font.render(self.top[i][0] + is_you, True, TEXT_COLOR)
            self.screen.blit(text, (
                self.x + sum(self.ratio[:1]) * self.width + (self.ratio[1] * self.width - text.get_width()) // 2,
                self.y + i * self.height))
            pygame.draw.rect(self.screen, BLACK,
                             (self.x + sum(self.ratio[:2]) * self.width, self.y + i * self.height,
                              self.ratio[2] * self.width, self.height), 1)
            text = font.render(str(self.top[i][1]), True, TEXT_COLOR)
            self.screen.blit(text, (
                self.x + sum(self.ratio[:2]) * self.width + (self.ratio[2] * self.width - text.get_width()) // 2,
                self.y + i * self.height))
            is_you = ''
        if not flag:
            i = min(5, len(self.top))
            self.top.append(self.cur_user)
            font = pygame.font.Font(os.path.abspath('data/font.ttf'), 32)
            pygame.draw.rect(self.screen, BLACK,
                             (self.x + sum(self.ratio[:0]) * self.width, self.y + i * self.height,
                              self.ratio[0] * self.width, self.height), 1)
            text = font.render(str(self.cur_index + 1), True, TEXT_COLOR)
            self.screen.blit(text, (
                self.x + sum(self.ratio[:0]) * self.width + (self.ratio[0] * self.width - text.get_width()) // 2,
                self.y + i * self.height))
            pygame.draw.rect(self.screen, BLACK,
                             (self.x + sum(self.ratio[:1]) * self.width, self.y + i * self.height,
                              self.ratio[1] * self.width, self.height), 1)
            text = font.render(self.top[i][0] + '(you)', True, TEXT_COLOR)
            self.screen.blit(text, (
                self.x + sum(self.ratio[:1]) * self.width + (self.ratio[1] * self.width - text.get_width()) // 2,
                self.y + i * self.height))
            pygame.draw.rect(self.screen, BLACK,
                             (self.x + sum(self.ratio[:2]) * self.width, self.y + i * self.height,
                              self.ratio[2] * self.width, self.height), 1)
            text = font.render(str(self.top[i][1]), True, TEXT_COLOR)
            self.screen.blit(text, (
                self.x + sum(self.ratio[:2]) * self.width + (self.ratio[2] * self.width - text.get_width()) // 2,
                self.y + i * self.height))
