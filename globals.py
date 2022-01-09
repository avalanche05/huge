import pygame

from CustomGroup import CustomGroup

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
