import pygame

pygame.font.init()


class Square:
    rows = 9
    cols = 9

    def __init__(self, number, row, col, width, height):
        self.number = number
        self.tmp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.clicked = False

    def draw(self, window):
        font = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        y = self.row * gap
        x = self.col * gap

        if self.tmp != 0 and self.number == 0:
            text = font.render(str(self.tmp), 1, (128, 128, 128))
            window.blit(text, (x + 5, y + 5))
        elif not self.number == 0:
            text = font.render(str(self.number), 1, (0, 0, 0))
            window.blit(
                text,
                (
                    x + (gap / 2 - text.get_width() / 2),
                    y + (gap / 2 - text.get_height() / 2),
                ),
            )
        if self.clicked:
            pygame.draw.rect(window, (200, 200, 0), (x, y, gap, gap), 3)

    def set(self, number):
        self.number = number

    def set_tmp(self, number):
        self.tmp = number
