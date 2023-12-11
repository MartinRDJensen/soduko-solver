def solve(board):
    find = get_empty(board)

    # Basecase
    # if there are no empty squares
    # return True and finish recursion
    if not find:
        return True

    row, col = find

    # loop through all of the numbers
    for number in range(1, 10):
        if valid(board, number, (row, col)):
            board[row][col] = number

            # Recursively run the solve with the new values put
            if solve(board):
                return True

            # if solve(board) returns false
            # reset the last element placed
            # the for loop is increment next time
            # and we try another number for the position
            board[row][col] = 0
    return False


def valid(board, number, pos):
    # check the row
    for col in range(len(board[0])):
        # go through column and check if a number
        # is equal to the one placed. But ignore the insertion place
        if board[pos[0]][col] == number and pos[1] != col:
            return False

    # check the columns
    for row in range(len(board)):
        if board[row][pos[1]] == number and pos[0] != row:
            return False

    # Determine which sqaure we are in
    square_x = pos[1] // 3
    square_y = pos[0] // 3

    # Loop through the square
    for i in range(square_y * 3, square_y * 3 + 3):
        for j in range(square_x * 3, square_x * 3 + 3):
            if board[i][j] == number and (i, j) != pos:
                return False
    return True


def get_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # Returns (row, column)
    return None
