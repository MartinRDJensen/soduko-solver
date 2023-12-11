import pygame
from soduku import *
import time
from square import Square

pygame.font.init()


class Game:
    board = [
        [8, 9, 0, 0, 0, 0, 0, 4, 3],
        [0, 0, 1, 2, 8, 0, 0, 6, 0],
        [0, 0, 5, 0, 0, 3, 1, 0, 8],
        [0, 4, 0, 0, 0, 0, 0, 3, 0],
        [0, 0, 0, 9, 0, 5, 0, 7, 0],
        [0, 0, 6, 0, 1, 0, 0, 2, 0],
        [3, 8, 0, 6, 0, 0, 9, 0, 0],
        [0, 7, 0, 1, 0, 4, 0, 0, 0],
        [6, 0, 2, 0, 0, 7, 0, 5, 0],
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.model = None
        self.clicked = None
        self.squares = [
            [Square(self.board[i][j], i, j, width, height) for j in range(cols)]
            for i in range(rows)
        ]
        self.testsquares = [
            [self.board[i][j] for j in range(cols)] for i in range(rows)
        ]

    def update_model(self):
        self.model = [
            [self.squares[i][j].number for j in range(self.cols)]
            for i in range(self.rows)
        ]

    def place(self, number):
        row, col = self.clicked

        if self.squares[row][col].number == 0:
            self.squares[row][col].set(number)
            self.update_model()
            if valid(self.model, number, (row, col)) and solve(self.model):
                return True
            else:
                self.squares[row][col].set(0)
                self.squares[row][col].set_tmp(0)
                self.update_model()
                return False

    def sketch(self, number):
        row, col = self.clicked
        self.squares[row][col].set_tmp(number)

    def draw(self, window):
        # create lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 3
            pygame.draw.line(
                window, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick
            )
            pygame.draw.line(
                window, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick
            )
        for row in range(self.rows):
            for col in range(self.cols):
                self.squares[row][col].draw(window)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].clicked = False
        self.squares[row][col].clicked = True
        self.clicked = (row, col)

    def clear(self):
        row, col = self.clicked
        if self.squares[row][col].number == 0:
            self.squares[row][col].set_tmp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.squares[row][col].number == 0:
                    return False
        return True


def redraw(window, board, time, strikes):
    window.fill((255, 255, 255))
    board.draw(window)
    # font = pygame.font.SysFont("comicsans", 1, (0, 0, 0))
    font = pygame.font.SysFont("comicsans", 20)
    text = font.render("Time: " + str(time)[:5], 1, (0, 0, 0))
    window.blit(text, (540 - 160, 560))
    text = font.render(f"Attempts: {strikes}", 1, (255, 0, 0))  # (255, 0, 0))
    window.blit(text, (0, 560))


def solve_display(window, board, play_time, strikes):
    # Current issue is that it doesn't return the
    # most deeply nested strikes
    # but the strikes before first recursive call
    find = get_empty(board.board)
    if not find:
        return (True, strikes)

    row, col = find

    for number in range(1, 10):
        strikes += 1
        if valid(board.board, number, (row, col)):
            board.squares[row][col].set(number)
            board.board[row][col] = number
            board.update_model()
            redraw(window, board, play_time, strikes)
            board.squares[row][col].draw(window)
            pygame.display.update()
            if solve_display(window, board, play_time, strikes + 1)[0]:
                return (True, strikes)
            board.squares[row][col].set(0)
            board.board[row][col] = 0
    return (False, strikes + 1)


def main():
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Soduku")
    board = Game(9, 9, 540, 540)
    key = True
    run = True
    start = time.time()
    strikes = 0
    while run:
        play_time = str(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_s:
                    strikes = solve_display(window, board, play_time, strikes)[1]
                if event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.clicked
                    if board.squares[i][j].tmp != 0:
                        if board.place(board.squares[i][j].tmp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None
            if board.is_finished():
                print("Game over")
                print("Sleeping for 5 seconds and then exiting")
                time.sleep(5)
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.clicked and key is not None:
            board.sketch(key)

        redraw(window, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
