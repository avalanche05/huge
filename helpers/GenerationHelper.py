from random import randint

from classes.Pole import Pole
from constant import LEVEL_COUNT, MIN_SPACE_LENGTH, MAX_SPACE_LENGTH, MAX_POLE_LENGTH, \
    MIN_POLE_LENGTH, WIDTH, MAX_GAP, LEVEL_HEIGHT, POLES


def generate_level():
    for level in range(1, LEVEL_COUNT):
        current_x = 0
        is_pole = bool(randint(0, 1))
        d = {False: (MIN_SPACE_LENGTH, MAX_SPACE_LENGTH),
             True: (MIN_POLE_LENGTH, MAX_POLE_LENGTH)}
        while d[is_pole][0] <= WIDTH - current_x:
            length = randint(d[is_pole][0], min(d[is_pole][1], WIDTH - current_x))
            gap = randint(-MAX_GAP, MAX_GAP)
            if is_pole:
                Pole((current_x, level * LEVEL_HEIGHT - MAX_GAP + gap), length, POLES)
            current_x += length
            is_pole = not is_pole
        else:
            gap = randint(-MAX_GAP, MAX_GAP)
            if is_pole:
                Pole((current_x, level * LEVEL_HEIGHT - MAX_GAP + gap), WIDTH - current_x, POLES)
