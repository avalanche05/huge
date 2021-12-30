import pygame
from pygame.sprite import Group

SIZE = WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode(SIZE)
GAME_TITLE = 'the huge.'
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
SETTINGS_SPRITES: Group = pygame.sprite.Group()
POLES = pygame.sprite.Group()
TREES = pygame.sprite.Group()
BIRDS = pygame.sprite.Group()
DINO = pygame.sprite.Group()
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
BACKGROUND = pygame.Color(247, 247, 247)
LEVEL_COUNT = 6
LEVEL_HEIGHT = 180
MAX_POLE_LENGTH = 360
MIN_POLE_LENGTH = 108
MAX_SPACE_LENGTH = 360
MIN_SPACE_LENGTH = 140
MAX_GAP = 10
