from sos import *

DEFAULT_SIZE = 6


class GameState(object):
    """
    a class for a game state, hold a board and scores
    """

    def __init__(self, table_size=DEFAULT_SIZE, board=None, score1=0, score2=0, done=False):
        super(GameState, self).__init__()
        self._done = done
        self._score = score1
        self._op_score = score2
        self._table_size = table_size
        if board is None:
            board = np.zeros((self._table_size, self._table_size))
        self._board = board

    @property
    def done(self):
        return self._done

    @property
    def score(self):
        return self._score

    @property
    def opponent_score(self):
        return self._op_score

    @property
    def board(self):
        return self._board

    def is_done(self):
        return np.count_nonzero(self._board) == self._table_size ** 2

    def isInRange(self, loc: tuple):
        return 0 <= loc[0] < self._table_size and 0 <= loc[1] < self._table_size

    def get_legal_actions(self):
        """
        makes a list of legal actions and returns it
        :return:
        """
        locations = np.array(np.where(self._board == 0)).T
        s_letter = np.ones(len(locations))
        o_letter = np.ones(len(locations)) + 1
        good_s = np.array([s_letter, locations.T[0], locations.T[1]], dtype=np.int).T
        good_o = np.array([o_letter, locations.T[0], locations.T[1]], dtype=np.int).T
        return np.concatenate((good_s, good_o))

    def generate_successor(self, action, player):
        """
        generates a new state given an action and a player
        :param action:
        :param player:
        :return:
        """
        successor = GameState(self._table_size, self._board.copy(),
                              self._score, self._op_score, self._done)
        successor.apply_action(action, player)
        return successor

    def apply_action(self, action, player):
        """
        applies action to the state
        :param action:
        :param player:
        :return:
        """
        self._board[action[1], action[2]] = action[0]
        self.score_update(action[1], action[2], player)

    def _sos_in_row(self, i, j):
        """check if sos in row"""
        locations = []
        if self.isInRange((i, j + 2)):
            if self._board[i, j] == S_LETTER and self._board[i, j + 1] == O_LETTER \
                    and self._board[i, j + 2] == S_LETTER:
                locations.append([i, j])
        if self.isInRange((j - 1, j + 1)):
            if self._board[i, j - 1] == S_LETTER and self._board[i, j] == O_LETTER \
                    and self._board[i, j + 1] == S_LETTER:
                locations.append([i, j - 1])
        if self.isInRange((i, j - 1)):
            if self._board[i, j - 2] == S_LETTER and self._board[i, j - 1] == O_LETTER \
                    and self._board[i, j] == S_LETTER:
                locations.append([i, j - 2])
        return locations

    def _sos_in_col(self, i, j):
        """checks if sos in column"""
        locations = []
        if self.isInRange((j, i + 2)):
            if self._board[i, j] == S_LETTER and self._board[i + 1, j] == O_LETTER \
                    and self._board[i + 2, j] == S_LETTER:
                locations.append([i, j])
        if self.isInRange((i + 1, i - 1)):
            if self._board[i - 1, j] == S_LETTER and self._board[i, j] == O_LETTER \
                    and self._board[i + 1, j] == S_LETTER:
                locations.append([i - 1, j])
        if self.isInRange((i - 2, j)):
            if self._board[i - 2, j] == S_LETTER and self._board[i - 1, j] == O_LETTER \
                    and self._board[i, j] == S_LETTER:
                locations.append([i - 2, j])
        return locations

    def _sos_in_diag(self, i, j):
        """checks if sos in diagonal"""
        locations = []
        if self.isInRange((i + 2, j + 2)):
            if self._board[i, j] == S_LETTER and self._board[i + 1, j + 1] == O_LETTER \
                    and self._board[i + 2, j + 2] == S_LETTER:
                locations.append([i, j])
        if self.isInRange((i + 1, j + 1)) and self.isInRange((i - 1, j - 1)):
            if self._board[i - 1, j - 1] == S_LETTER and self._board[i, j] == O_LETTER \
                    and self._board[i + 1, j + 1] == S_LETTER:
                locations.append([i - 1, j - 1])
        if self.isInRange((i - 2, j - 2)):
            if self._board[i - 2, j - 2] == S_LETTER and self._board[
                i - 1, j - 1] == O_LETTER \
                    and self._board[i, j] == S_LETTER:
                locations.append([i - 2, j - 2])
            return locations

    def _sos_in_diag2(self, i, j):
        """check if sos in other diagonal"""
        locations = []
        if self.isInRange((i + 2, j - 2)):
            if self._board[i, j] == S_LETTER and self._board[i + 1, j - 1] == O_LETTER \
                    and self._board[i + 2, j - 2] == S_LETTER:
                locations.append([i, j])
        if self.isInRange((i - 1, j + 1)) and self.isInRange((i + 1, j - 1)):
            if self._board[i - 1, j + 1] == S_LETTER and self._board[i, j] == O_LETTER \
                    and self._board[i + 1, j - 1] == S_LETTER:
                locations.append([i - 1, j + 1])
        if self.isInRange((i - 2, j + 2)):
            if self._board[i - 2, j + 2] == S_LETTER and self._board[
                i - 1, j + 1] == O_LETTER \
                    and self._board[i, j] == S_LETTER:
                locations.append([i - 2, j + 2])
        return locations

    def score_update(self, i, j, player):
        """updates the score according to the player"""
        score = 0
        rows = self._sos_in_row(i, j)
        if rows:
            score += len(rows)
        cols = self._sos_in_col(i, j)
        if cols:
            score += len(cols)
        diag1 = self._sos_in_diag(i, j)
        if diag1:
            score += len(diag1)
        diag2 = self._sos_in_diag2(i, j)
        if diag2:
            score += len(diag2)
        if player == 0:
            self._score += score
        else:
            self._op_score += score
