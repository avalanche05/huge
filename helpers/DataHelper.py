import os
import sys

import pygame


def load_image(name: str, colorkey=None):
    """Скачивание изображения"""
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def cut_sheet(sheet, value):
    states = []
    for columns, rows, start_x, start_y, stop_x, stop_y, width, height in value:
        rect = pygame.Rect(0, 0, (stop_x - start_x) // columns,
                           (stop_y - start_y) // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (start_x + rect.w * i, start_y + rect.h * j)
                states.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)), (width, height)))
    return states
