from random import randint

from classes.Barrier import Barrier
from classes.Dino import Dino
from classes.Enemy import Enemy
from classes.Pole import Pole
from constant import LEVEL_COUNT, MIN_SPACE_LENGTH, MAX_SPACE_LENGTH, MAX_POLE_LENGTH, \
    MIN_POLE_LENGTH, WIDTH, MAX_GAP, LEVEL_HEIGHT, POLES, BARRIERS, ENEMIES, \
    POLES_GAP, \
    DINO


def generate_barriers(start_x, stop_x, chance, y):
    current_x = start_x + POLES_GAP
    while current_x < stop_x - POLES_GAP:
        if not randint(0, 1 // chance):
            current_x += Barrier((current_x, y), BARRIERS).rect.width
        else:
            current_x += randint(40, 70)


def generate_enemy(level):
    for _ in range(randint(0, 3)):
        Enemy((randint(0, WIDTH - 80), level * LEVEL_HEIGHT - LEVEL_HEIGHT + randint(10, 40)),
              randint(2, 10), ENEMIES)


def clear_groups():
    for group in (DINO, BARRIERS, ENEMIES, POLES):
        for sprite in group:
            sprite.kill()


def generate_level():
    clear_groups()

    for level in range(1, LEVEL_COUNT):
        if level != LEVEL_COUNT - 1:
            generate_enemy(level)
        current_x = 0
        is_pole = bool(randint(0, 1))
        d = {False: (MIN_SPACE_LENGTH, MAX_SPACE_LENGTH),
             True: (MIN_POLE_LENGTH, MAX_POLE_LENGTH)}
        while d[is_pole][0] <= WIDTH - current_x:
            length = randint(d[is_pole][0], min(d[is_pole][1], WIDTH - current_x))
            gap = randint(-MAX_GAP, MAX_GAP)
            if is_pole:
                y = level * LEVEL_HEIGHT - MAX_GAP + gap
                Pole((current_x, y), length, POLES)
                generate_barriers(current_x, current_x + length - 40, 1 / 4, y - 123)
            current_x += length
            is_pole = not is_pole
        else:
            gap = randint(-MAX_GAP, MAX_GAP)
            if is_pole:
                Pole((current_x, level * LEVEL_HEIGHT - MAX_GAP + gap), WIDTH - current_x, POLES)
        if level == LEVEL_COUNT - 1:
            while True:
                dino = Dino((randint(0, WIDTH), LEVEL_HEIGHT * (LEVEL_COUNT - 1) - 80), DINO)
                if dino.cross(POLES) and not dino.cross(BARRIERS):
                    break
                else:
                    dino.kill()
