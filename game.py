import abc
from board import *

S_LETTER = 1
O_LETTER = 2
EMPTY = 0


class Agent(object):
    """
    an abstract class of an AI agent
    """

    def __init__(self):
        super(Agent, self).__init__()

    @abc.abstractmethod
    def get_action(self, game_state):
        return

    def stop_running(self):
        pass


class Game:
    """
    a class for a game of sos
    """

    def __init__(self, table_size):
        self.player = 0
        self.score = [0, 0]
        self.board = Board(table_size)

    def choose_tile(self, letter, row, col):
        """
        puts a letter in the board if possible
        :param letter:
        :param row:
        :param col:
        :return:
        """
        if self.board.get_letter(row, col) != 0:
            return -1
        return self.board.put_letter(letter, row, col)

    def done(self):
        """
        checks if the game is finished
        :return:
        """
        return self.board.is_full()

    def switch_turn(self, old_score):
        """
        switches player turn when needed
        :param old_score:
        :return:
        """
        if old_score == self.score:
            self.player = 1 - self.player

    def sos_in_row(self, i, j):
        """
        check how many sos's in row
        :param i:
        :param j:
        :return:
        """
        locations = []
        if self.board.get_letter(i, j) == S_LETTER and self.board.get_letter(i,
                                                                             j + 1) == O_LETTER \
                and self.board.get_letter(i, j + 2) == S_LETTER:
            locations.append([i, j])
        if self.board.get_letter(i, j - 1) == S_LETTER and self.board.get_letter(i,
                                                                                 j) == O_LETTER \
                and self.board.get_letter(i, j + 1) == S_LETTER:
            locations.append([i, j - 1])
        if self.board.get_letter(i, j - 2) == S_LETTER and self.board.get_letter(i,
                                                                                 j - 1) == O_LETTER \
                and self.board.get_letter(i, j) == S_LETTER:
            locations.append([i, j - 2])
        return locations

    def sos_in_col(self, i, j):
        """
        check how many sos's in column
        :param i:
        :param j:
        :return:
        """
        locations = []
        if self.board.get_letter(i, j) == S_LETTER and self.board.get_letter(i + 1,
                                                                             j) == O_LETTER \
                and self.board.get_letter(i + 2, j) == S_LETTER:
            locations.append([i, j])
        if self.board.get_letter(i - 1, j) == S_LETTER and self.board.get_letter(i,
                                                                                 j) == O_LETTER \
                and self.board.get_letter(i + 1, j) == S_LETTER:
            locations.append([i - 1, j])
        if self.board.get_letter(i - 2, j) == S_LETTER and self.board.get_letter(i - 1,
                                                                                 j) == O_LETTER \
                and self.board.get_letter(i, j) == S_LETTER:
            locations.append([i - 2, j])
        return locations

    def sos_in_diag(self, i, j):
        """
        check how many sos's in diagonal
        :param i:
        :param j:
        :return:
        """
        locations = []
        if self.board.get_letter(i, j) == S_LETTER and self.board.get_letter(i + 1,
                                                                             j + 1) == O_LETTER \
                and self.board.get_letter(i + 2, j + 2) == S_LETTER:
            locations.append([i, j])
        if self.board.get_letter(i - 1, j - 1) == S_LETTER and self.board.get_letter(i,
                                                                                     j) == O_LETTER \
                and self.board.get_letter(i + 1, j + 1) == S_LETTER:
            locations.append([i - 1, j - 1])
        if self.board.get_letter(i - 2, j - 2) == S_LETTER and self.board.get_letter(
                i - 1, j - 1) == O_LETTER \
                and self.board.get_letter(i, j) == S_LETTER:
            locations.append([i - 2, j - 2])
        return locations

    def sos_in_diag2(self, i, j):
        """
       check how many sos's in other diagonal
       :param i:
       :param j:
       :return:
       """
        locations = []
        if self.board.get_letter(i, j) == S_LETTER and self.board.get_letter(i + 1,
                                                                             j - 1) == O_LETTER \
                and self.board.get_letter(i + 2, j - 2) == S_LETTER:
            locations.append([i, j])
        if self.board.get_letter(i - 1, j + 1) == S_LETTER and self.board.get_letter(i,
                                                                                     j) == O_LETTER \
                and self.board.get_letter(i + 1, j - 1) == S_LETTER:
            locations.append([i - 1, j + 1])
        if self.board.get_letter(i - 2, j + 2) == S_LETTER and self.board.get_letter(
                i - 1, j + 1) == O_LETTER \
                and self.board.get_letter(i, j) == S_LETTER:
            locations.append([i - 2, j + 2])
        return locations

    def update_scores(self, i, j):
        """
        updates the score of the given move
        :param i:
        :param j:
        :return:
        """
        # i is for column , j is for row
        score = 0
        rows = self.sos_in_row(i, j)
        if rows:
            score += len(rows)
        cols = self.sos_in_col(i, j)
        if cols:
            score += len(cols)
        diag1 = self.sos_in_diag(i, j)
        if diag1:
            score += len(diag1)
        diag2 = self.sos_in_diag2(i, j)
        if diag2:
            score += len(diag2)
        self.score[self.player] += score

    def get_winner(self):
        """
        returns the player with the highest score
        :return:
        """
        if self.score[0] == self.score[1]:
            return -1
        return np.argmax(np.array(self.score))

    def get_player(self):
        """
        returns current player
        :return:
        """
        return self.player

    def get_state(self):
        """
        returns the state of the board of the game
        :return:
        """
        return self.board

    def make_turn(self, action):
        """
        runs one full turn with all that is required
        :param action: [letter, row ,col]
        :return:
        """
        self.choose_tile(action[0], action[1], action[2])
        old_score = self.score[:]
        self.update_scores(action[1], action[2])
        self.switch_turn(old_score)
