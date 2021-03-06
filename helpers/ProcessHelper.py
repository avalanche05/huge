import os
import sys
from random import randint, randrange

import pygame

from classes.Barrier import Barrier
from classes.ChooseButton import ChooseButton
from classes.Cloud import Cloud
from classes.Dino import Dino
from classes.Enemy import Enemy
from classes.FunctionalButton import FunctionalButton
from classes.Pole import Pole
from classes.Settings import Settings
from classes.TextButton import TextButton
from constant import BACKGROUND, FPS, HEIGHT, PLATFORM_SPRITE_LENGTH, SPEED_BOOST, WIDTH, \
    GENERATE_CHANCE, CLOUD_CHANCE, TEXT_COLOR, STARTED_TEXT, PRESS_UP_TEXT, PRESS_DOWN_TEXT, UUID, \
    DEFAULT_NAME, BLACK, FINAL_WINDOW_COLOR, FINAL_TEXT, SCORE_COUNT
from globals import barriers, enemies, settings, clouds, settings_sprites, poles, dino, screen, \
    portal, trees, clock, transformation_surface, user, table, score
from helpers.DataBaseHelper import is_mac_contain, get_username, update_user_in_db, add_user_in_db
from helpers.GenerationHelper import generate_level, clear_groups


def terminate():
    """Выход из игры"""
    pygame.quit()
    sys.exit()


def started_window():
    """Работа стартового окна"""
    global score

    def biggest_x():
        ans = -200

        for sprite in barriers:
            ans = max(ans, sprite.rect.x)
        for sprite in enemies:
            ans = max(ans, sprite.rect.x)

        return ans

    def is_generate_correct():
        return biggest_x() < WIDTH - 400

    def is_barrier_near(count):
        """функция проверяет наличие препятсвия на расстоянии count пикселей от игрока"""
        for barrier in barriers:
            if barrier.rect.x - dino_sprite.rect.x <= dino_sprite.rect.width + count \
                    and barrier.rect.x + barrier.rect.width > dino_sprite.rect.x:
                return True

        return False

    def is_enemy_near(count):
        """функция проверяет наличие врага в радиусе count пикселей от игрока"""
        for enemy in enemies:
            if enemy.rect.x <= dino_sprite.rect.width + dino_sprite.rect.x + count and \
                    enemy.rect.x + enemy.rect.width - 10 > dino_sprite.rect.x:
                return True

        return False

    def update_platform():
        """функция двигает платформу на константную скорость"""
        platform_1.rect.x = current_x
        platform_2.rect.x = current_x - PLATFORM_SPRITE_LENGTH

    def generate_enemies():
        # генерация врага происходит случайно
        if not randrange(0, 1 // enemy_chance) and is_generate_correct():
            Enemy((WIDTH, HEIGHT * 0.6 - 110), -(platform_speed + 240) // FPS, enemies,
                  is_start=True)

    def generate_barriers():
        # генерация барьера происходит случайно
        if not randrange(0, 1 // barrier_chance) and is_generate_correct():
            barrier = Barrier((WIDTH, HEIGHT * 0.6 - 100), barriers)
            barrier.move(randint(0, 15))

    def generate_clouds():
        # генерация барьера происходит случайно
        if not randrange(0, int(1 // CLOUD_CHANCE)):
            cloud = Cloud((WIDTH, HEIGHT * 0.6 - 200), -platform_speed // FPS, clouds)
            cloud.move(randint(0, 80))

    def tutorial():
        nonlocal is_dino_dead, current_x
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
            if is_dino_dead:
                key = 'key up' if ai_step()[0] else 'key down'
                is_dino_dead = False
                shift = 600
                for group in (barriers, enemies, clouds):
                    for sprite in group:
                        sprite.rect.x += shift
                for sprite in enemies:
                    sprite.rect.x += 240
                current_x += shift
                current_x %= PLATFORM_SPRITE_LENGTH
                dino_sprite.rect.y = dino_sprite.start_y
                update_platform()
                draw_screen()
                text = font.render(f'You should have pressed {key}', True, TEXT_COLOR)
                screen.blit(text, (
                    WIDTH // 2 - text.get_width() // 2, HEIGHT - 100 + text.get_height() // 2))
                update_screen()
                clock.tick(1 / 2)

            # генерация объектов
            generate_barriers()
            generate_enemies()
            generate_clouds()

            # обновление координат всех объектов
            update_platform()
            clouds.update()
            barriers.update(platform_speed // FPS)
            enemies.update()

            # изменение текущего положение всех объектов
            current_x -= platform_speed // FPS
            current_x %= PLATFORM_SPRITE_LENGTH
            is_dino_dead = dino.update(False, False, False, False)
            draw_screen()
            is_up, is_down = ai_step()
            if is_up:
                text = font.render(PRESS_UP_TEXT, True, TEXT_COLOR)
                screen.blit(text, (
                    WIDTH // 2 - text.get_width() // 2, HEIGHT - 100 + text.get_height() // 2))
            elif is_down:
                text = font.render(PRESS_DOWN_TEXT, True, TEXT_COLOR)
                screen.blit(text, (
                    WIDTH // 2 - text.get_width() // 2, HEIGHT - 100 + text.get_height() // 2))
            update_screen()

    def ai_step():
        is_up = is_barrier_near(150) and not is_enemy_near(400) \
                or is_barrier_near(150) and is_enemy_near(150) \
                or is_barrier_near(30)
        is_down = is_enemy_near(30) and not is_up
        return is_up, is_down

    if not is_mac_contain(UUID):
        add_user_in_db(user)
    # обновление таблицы
    table.update()
    # очистка всех спрайтов
    clear_groups()
    # инициализация спрайтов
    settings_sprite = Settings((WIDTH - 64, 0), settings)

    if is_mac_contain(UUID):
        username = get_username(UUID)
    else:
        username = DEFAULT_NAME
    username_button = TextButton('Name', (WIDTH // 2, HEIGHT // 2 - 140), settings_sprites,
                                 start_text=username)
    difficult_button = ChooseButton('Difficult', (WIDTH // 2, HEIGHT // 2 - 70), settings_sprites,
                                    args=['<Easy>', '<Medium>', '<Hard>'])
    FunctionalButton('Tutorial', (WIDTH // 2, HEIGHT // 2), settings_sprites, function=tutorial)
    top_button = ChooseButton('Top', (WIDTH // 2, HEIGHT // 2 + 70), settings_sprites, args=['<OFF>', '<ON>'])
    FunctionalButton('Quit', (WIDTH // 2, HEIGHT // 2 + 140), settings_sprites, function=terminate)
    dino_sprite = Dino((100, HEIGHT * 0.6 - 70), dino, is_start=True)
    platform_1 = Pole((0, HEIGHT * 0.6), PLATFORM_SPRITE_LENGTH, poles, start_pos=0)
    platform_2 = Pole((0, HEIGHT * 0.6), PLATFORM_SPRITE_LENGTH, poles, start_pos=0)
    # инициализация переменных
    difficult_degree = difficult_button.get_text()
    barrier_chance, enemy_chance = GENERATE_CHANCE[difficult_degree][:2]
    current_x = 0
    platform_speed = 600
    alpha = 0
    addend = 8
    score = 0
    color = [0, 0, 0, 255]
    is_top_show = False
    font = pygame.font.Font(os.path.abspath('data/font.ttf'), 32)
    text = font.render(STARTED_TEXT, True, TEXT_COLOR)
    is_player_game = False
    is_dino_dead = False

    def update_name():

        user.set_username(username_button.get_text())

        if is_mac_contain(UUID):
            update_user_in_db(user)
        else:
            add_user_in_db(user)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_player_game = False
                score = 0
            if is_player_game and event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                set_pause()
            if not is_player_game and event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_UP, pygame.K_DOWN):
                difficult_degree = difficult_button.get_text()
                barrier_chance, enemy_chance = GENERATE_CHANCE[difficult_degree][:2]
                is_player_game = True
                update_name()
            if not is_player_game:
                settings_sprite.position().update(event)
                settings.update(event)
            if is_dino_dead and event.type == pygame.KEYDOWN:
                game_window(difficult_degree)
        if is_dino_dead:
            continue

        # генерация объектов
        generate_barriers()
        generate_enemies()
        generate_clouds()

        # обновление координат всех объектов
        update_platform()
        clouds.update()
        barriers.update(platform_speed // FPS)
        if top_button.get_text() == '<ON>' and not is_top_show:
            table.update()
        is_top_show = True if top_button.get_text() == '<ON>' else False
        if is_player_game:
            is_dino_dead = dino.update(False, False, False, False)
            platform_speed += SPEED_BOOST
            score += 1
        else:
            dino.update(*ai_step(), False, False, True)
        enemies.update()

        # изменение текущего положение всех объектов
        current_x -= platform_speed // FPS
        current_x %= PLATFORM_SPRITE_LENGTH

        draw_screen()
        if not is_player_game:
            settings.draw(screen)
            settings_sprite.position().draw(screen)
            text.set_alpha(alpha)
            alpha += addend
            addend = addend if 0 <= alpha <= 255 else -addend
            screen.blit(text,
                        (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100 + text.get_height() // 2))
            if is_top_show:
                table.render()
        transformation_surface.fill(color)
        screen.blit(transformation_surface, (0, 0))
        color[-1] = max(color[-1] - 5, 0)
        update_screen()


def final_screen(difficult_degree):
    global score
    set_color(FINAL_WINDOW_COLOR)
    alpha = 255
    addend = 5
    font = pygame.font.Font(os.path.abspath('data/font.ttf'), 32)
    text = font.render(FINAL_TEXT, True, TEXT_COLOR)
    font = pygame.font.Font(os.path.abspath('data/font.ttf'), 64)
    score = max(0, score)
    score *= GENERATE_CHANCE[difficult_degree][-1]
    user.set_best_score(score)
    update_user_in_db(user)
    score_text = font.render(f'{SCORE_COUNT} {score}', True, TEXT_COLOR)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                started_window()
        text.set_alpha(alpha)
        alpha += addend
        addend = addend if 0 <= alpha <= 255 else -addend
        alpha += 0 if 0 <= alpha <= 255 else addend
        screen.fill(FINAL_WINDOW_COLOR)
        screen.blit(text,
                    (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100 - text.get_height() // 2))
        screen.blit(score_text,
                    (WIDTH // 2 - score_text.get_width() // 2,
                     HEIGHT * 0.5 - score_text.get_height() // 2))
        update_screen()


def set_color(color: pygame.Color):
    for i in range(0, 256, 15):
        color.a = i
        transformation_surface.fill(color)
        screen.blit(transformation_surface, (0, 0))
        update_screen()


def set_pause():
    transformation_surface.fill((0, 0, 0, 75))
    screen.blit(transformation_surface, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                return


def update_screen():
    clock.tick(FPS)
    pygame.display.flip()


def game_window(difficult_degree):
    global score
    barrier_chance, max_enemy_count = GENERATE_CHANCE[difficult_degree][2:-1]
    generate_level(barrier_chance, max_enemy_count)
    is_dino_dead = False
    color = [0, 0, 0, 255]
    set_color(BLACK)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                set_color(BLACK)
                started_window()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p and not is_dino_dead:
                set_pause()
            if is_dino_dead and event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE,):
                set_color(BLACK)
                generate_level(barrier_chance, max_enemy_count)
                is_dino_dead = False
                color[-1] = 255
                score -= 500
        if is_dino_dead:
            continue
        is_dino_dead = dino.update()
        if is_dino_dead == -1:
            final_screen(difficult_degree)
        score -= 1
        clouds.update()
        enemies.update()
        portal.update()
        clouds.update()
        draw_screen()
        transformation_surface.fill(color)
        screen.blit(transformation_surface, (0, 0))
        color[-1] = max(color[-1] - 3, 0)
        update_screen()


def draw_screen():
    screen.fill(BACKGROUND)
    portal.draw(screen)
    clouds.draw(screen)
    barriers.draw(screen)
    poles.draw(screen)
    trees.draw(screen)
    dino.draw(screen)
    enemies.draw(screen)
