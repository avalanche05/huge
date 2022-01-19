import pygame

from CustomGroup import CustomGroup
from classes.User import User
from constant import UUID, DEFAULT_NAME
from helpers.DataBaseHelper import is_mac_contain, get_username

screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
transformation_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
clock = pygame.time.Clock()
settings = pygame.sprite.Group()
start_sprites = pygame.sprite.Group()
settings_sprites = pygame.sprite.Group()
poles = pygame.sprite.Group()
trees = pygame.sprite.Group()
enemies = pygame.sprite.Group()
dino = CustomGroup()
barriers = pygame.sprite.Group()
clouds = pygame.sprite.Group()
portal = pygame.sprite.Group()
score = 0
user = User(get_username(UUID) if is_mac_contain(UUID) else DEFAULT_NAME, UUID, 0)
