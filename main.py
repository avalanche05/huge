import pygame

WIDTH, HEIGHT = 1920, 1080


def draw(screen):
    screen.fill('#c0e6d7')
    font = pygame.font.Font(None, 50)
    text = font.render("the huge.", True, 'black')
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))


def main():
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)

    draw(screen)
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()


if __name__ == '__main__':
    main()
