import numpy as np


class Board:
    """
    a class representing a board
    """

    def __init__(self, table_size):
        self.table_size = table_size
        self.board = np.zeros((self.table_size, self.table_size))

    def __repr__(self):
        s = ""
        for row in self.board:
            for letter in row:
                if letter == 0:
                    s += "_|"
                elif letter == 1:
                    s += "S|"
                else:
                    s += "O|"
            s += "\n"
        return s

    def is_full(self):
        return np.count_nonzero(self.board) == self.table_size ** 2

    def put_letter(self, letter, row, col):
        if row < 0 or row > self.table_size - 1 or col < 0 or col > self.table_size - 1:
            return -1
        self.board[row][col] = letter

    def get_letter(self, row, col):
        if row < 0 or row > self.table_size - 1 or col < 0 or col > self.table_size - 1:
            return -1
        return self.board[row][col]

    def get_empty_locations(self):
        return np.array(np.where(self.board == 0)).T
