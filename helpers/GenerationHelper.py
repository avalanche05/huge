from random import randint, randrange, choice

from classes.Barrier import Barrier
from classes.Cloud import Cloud
from classes.Dino import Dino
from classes.Enemy import Enemy
from classes.Pole import Pole
from classes.Portal import Portal
from constant import LEVEL_COUNT, MIN_SPACE_LENGTH, MAX_SPACE_LENGTH, MAX_POLE_LENGTH, \
    MIN_POLE_LENGTH, WIDTH, MAX_GAP, LEVEL_HEIGHT, POLES, BARRIERS, ENEMIES, DINO, CLOUDS, PORTAL


def generate_barriers(start_x, stop_x, chance, y):
    current_x = start_x
    while current_x < stop_x:
        if not randrange(0, 1 // chance):
            current_x += Barrier((current_x, y), BARRIERS).get_width()
        else:
            current_x += randint(40, 70)


def generate_enemy(level, max_enemy_count):
    for _ in range(randint(0, max_enemy_count)):
        Enemy((randint(0, WIDTH - 80), level * LEVEL_HEIGHT - LEVEL_HEIGHT + randint(10, 40)),
              randint(2, 10), ENEMIES)


def generate_clouds(level, count):
    for _ in range(randint(0, count)):
        Cloud((randint(0, WIDTH - 80), (level - 1) * LEVEL_HEIGHT + randint(10, 40)), 0, CLOUDS)


def clear_groups():
    for group in (DINO, BARRIERS, ENEMIES, POLES, CLOUDS, PORTAL):
        for sprite in group:
            sprite.kill()


def generate_level(barrier_chance, max_enemy_count):
    """генерирует сигнатуру уровня(положение всех объектов)"""

    # перед началом генерации уровня, очистим весь экран
    clear_groups()

    # перебираем все уровни
    # уровнем считается определённая высота
    for level in range(1, LEVEL_COUNT):
        current_x = 0
        # случайно выбираем с чего начать: платформы или пустоты
        is_pole = bool(randint(0, 1))
        # словарь содержит диапазон длин
        length_range = {False: (MIN_SPACE_LENGTH, MAX_SPACE_LENGTH),
                        True: (MIN_POLE_LENGTH, MAX_POLE_LENGTH)}

        # список будет содержать все платформы на данном уровне
        poles = []

        # в цикле происходит генерация объектов
        while length_range[is_pole][0] <= WIDTH - current_x:
            # случайно выбираем длину
            length = randint(length_range[is_pole][0],
                             min(length_range[is_pole][1], WIDTH - current_x))
            # выбираем небольшой люфт платформ на уровне
            gap = randint(-MAX_GAP, MAX_GAP)

            if is_pole:
                # выбираем высоту платформы
                y = level * LEVEL_HEIGHT - MAX_GAP + gap
                pole = Pole((current_x, y), length, POLES)
                # сохраняем текущую платформу
                poles.append(pole)
            current_x += length
            # генерация происходит последовательно
            # после пустого пространства идёт платформа и наоборот
            is_pole = not is_pole

        # после полной генерации может остаться большое пустое пространство
        if is_pole:
            gap = randint(-MAX_GAP, MAX_GAP)
            y = level * LEVEL_HEIGHT - MAX_GAP + gap
            Pole((current_x, y), WIDTH - current_x, POLES)

        # на данном уровне должен генерироваться игрок
        if level == LEVEL_COUNT - 1:
            # выбираем случайную платформу на текущем уровне
            pole = choice(poles)
            # удаляем платформу из списка, т.к. мы НЕ генерируем препятствия на платформе игрока
            poles.remove(pole)

            x_pole = pole.rect.x
            y_pole = pole.rect.y
            pole_length = pole.rect.width

            # выбираем случайный x для игрока
            x_dino = randint(x_pole, x_pole + pole_length - 40)
            Dino((x_dino, y_pole - 100), DINO)
        else:
            # мы генрируем врагов на всех уровнях кроме нижнего, т.к. там изначально находится игрок
            generate_enemy(level, max_enemy_count)

        # генерируем облака на каждом уровне
        generate_clouds(level, 5)

        # на данном уровне должен генерироваться портал
        if level == 1:
            # выбираем случайную платформу на текущем уровне
            pole = choice(poles)
            # удаляем портал из списка, т.к. мы НЕ генерируем препятствия на платформе портала
            poles.remove(pole)

            x_pole = pole.rect.x
            y_pole = pole.rect.y
            pole_length = pole.rect.width

            # выбираем случайный x для портала
            x_platform = randint(x_pole, max(x_pole, x_pole + pole_length - 160))
            Portal((x_platform, y_pole - 145), PORTAL)

        # расставляем препятствия на платформах
        for pole in poles:
            x_pole = pole.rect.x
            y_pole = pole.rect.y
            pole_length = pole.rect.width
            generate_barriers(x_pole, x_pole + pole_length - 40, barrier_chance, y_pole - 123)
