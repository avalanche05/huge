import pygame
from pygame.sprite import Group

import CustomGroup

SIZE = WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode(SIZE)
bgd = pygame.display.set_mode(SIZE)
GAME_TITLE = 'the huge.'
ENEMY_SPEED = 5
DINO_SPEED = 10
FPS = 60
CLOCK = pygame.time.Clock()
PLACE_IN_IMAGE = {'Enemy': [[2, 1, 260, 0, 444, 100, 80, 80]],
                  'Cloud': [[1, 1, 170, 0, 260, 60, 110, 80]],
                  'Dino': [[6, 1, 1678, 0, 2208, 100, 88, 100],
                           [2, 1, 2209, 0, 2445, 100, 118, 100]],
                  'Pole': [[1, 1, 2, 100, 2402, 130, 2400, 30]],
                  'Tree': [[6, 1, 446, 0, 650, 73, 40, 70]],
                  'Portal': [[1, 1, 1, 1, 255, 255, 254, 254]]}
# в словаре находятся шансы генерации в соответсвии с уровнем сложности
# последовательность: barrier_chance, enemy_chance, max_enemy_count
GENERATE_CHANCE = {'<Easy>': (1 / 300, 1 / 300, 1 / 5, 2),
                   '<Medium>': (1 / 225, 1 / 225, 1 / 4, 3),
                   '<Hard>': (1 / 150, 1 / 150, 1 / 3, 4)}
CLOUD_CHANCE = 1 / 100
SETTINGS = pygame.sprite.Group()
START_SPRITES = pygame.sprite.Group()
SETTINGS_SPRITES: Group = pygame.sprite.Group()
POLES = pygame.sprite.Group()
TREES = pygame.sprite.Group()
ENEMIES = pygame.sprite.Group()
DINO = CustomGroup.CustomGroup()
BARRIERS = pygame.sprite.Group()
CLOUDS = pygame.sprite.Group()
PORTAL = pygame.sprite.Group()
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
BACKGROUND = pygame.Color(247, 247, 247)
LEVEL_COUNT = 6
LEVEL_HEIGHT = 180
MAX_POLE_LENGTH = 360
MIN_POLE_LENGTH = 108
MAX_SPACE_LENGTH = 360
MIN_SPACE_LENGTH = 140
SPEED_BOOST = 0.1
MAX_GAP = 10
PLATFORM_SPRITE_LENGTH = 2400
