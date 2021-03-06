import uuid
from math import ceil

import pygame

UUID = uuid.getnode()
pygame.init()
SIZE = WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
GAME_TITLE = 'the huge.'
ENEMY_SPEED = 5
DINO_SPEED = 10
FPS = 60
PLACE_IN_IMAGE = {'Enemy': [[2, 1, 260, 0, 444, 100, 80, 80]],
                  'Cloud': [[1, 1, 170, 0, 260, 60, 110, 80]],
                  'Dino': [[6, 1, 1678, 0, 2208, 100, 88, 100],
                           [2, 1, 2209, 0, 2445, 100, 118, 100]],
                  'Pole': [[1, 1, 2, 100, 2402, 130, 2400, 30]],
                  'Tree': [[6, 1, 446, 0, 650, 73, 40, 70]],
                  'Portal': [[1, 1, 1, 1, 255, 255, 254, 254]]}
# в словаре находятся шансы генерации в соответсвии с уровнем сложности
# последовательность: barrier_chance, enemy_chance, max_enemy_count
GENERATE_CHANCE = {'<Easy>': (1 / 300, 1 / 300, 1 / 5, 2, 1),
                   '<Medium>': (1 / 225, 1 / 225, 1 / 4, 3, 2),
                   '<Hard>': (1 / 150, 1 / 150, 1 / 3, 4, 3)}
CLOUD_CHANCE = 1 / 100
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
BACKGROUND = pygame.Color(247, 247, 247)
FINAL_WINDOW_COLOR = pygame.Color(30, 30, 30)
TEXT_COLOR = pygame.Color(83, 83, 83)
SETTINGS_TEXT_COLOR = BLACK
LEVEL_HEIGHT = 180
LEVEL_COUNT = ceil(HEIGHT / LEVEL_HEIGHT)
MAX_POLE_LENGTH = 360
MIN_POLE_LENGTH = 108
MAX_SPACE_LENGTH = 360
MIN_SPACE_LENGTH = 140
SPEED_BOOST = 0.1
MAX_GAP = 10
PLATFORM_SPRITE_LENGTH = 2400
STARTED_TEXT = 'PRESS ARROW KEY TO START'
FINAL_TEXT = 'PRESS ANY KEY TO CONTINUE'
SCORE_COUNT = 'You score:'
PRESS_UP_TEXT = 'press key up'
PRESS_DOWN_TEXT = 'press key down'
MONGO_DB_CONNECTION = "mongodb+srv://Admin:hugebestproject@maincluster.jjykr.mongodb.net" \
                      "/huge?retryWrites=true&w=majority"
DEFAULT_NAME = 'unidentified otter'
