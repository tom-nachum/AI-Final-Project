import random
import numpy as np
import abc
import game
from game import Agent
from game_state import GameState

MIN_AGENT = 1
MAX_AGENT = 0


def good_minus_bad_evaluation_function(current_game_state: GameState):
    return current_game_state.score - current_game_state.opponent_score


def score_evaluation_function(current_game_state: GameState):
    return current_game_state.score


def opponent_score_function(current_game_state: GameState):
    return current_game_state.opponent_score


def min_score_evaluation_function(current_game_state: GameState):
    if current_game_state.opponent_score == 0:
        return 2
    return 1 / current_game_state.opponent_score


def is_almost_sos(row, col, current_game_state):
    """
    checks if exists a situation where the opponent can complete sos next turn
    :param row:
    :param col:
    :param current_game_state:
    :return:
    """
    board = current_game_state.board
    for i in range(-1, 2):
        for j in range(-1, 2):
            o_pos = (row + i, col + j)
            s_pos = (row + 2 * i, col + 2 * j)
            if current_game_state.isInRange(s_pos):
                is_soe = board[o_pos] == game.O_LETTER and board[s_pos] == game.EMPTY
                is_ses = board[o_pos] == game.EMPTY and board[s_pos] == game.S_LETTER
                if is_soe or is_ses:
                    return True
    return False


def block_evaluation_function(current_game_state: GameState):
    """
    counts how many near sos's can be made and returns 1/#nearsos's
    :param current_game_state:
    :return:
    """
    board = current_game_state.board
    locations = np.array(np.where(board == game.S_LETTER))
    score = 1
    for row, col in locations.T:
        if is_almost_sos(row, col, current_game_state):
            score += 1
    return 1 / score


def combined_heuristic(current_game_state: GameState):
    """
    runs a score evaluation and if we can't get any score runs block evaluation
    :param current_game_state:
    :return:
    """
    value = 3 * score_evaluation_function(current_game_state)
    if value == 0:
        return block_evaluation_function(current_game_state)
    return value


def smart_random_play(game_state: GameState):
    """
    a random play that does not create a near sos , not always possible therefore might return None
    :param game_state:
    :return:
    """
    actions = game_state.get_legal_actions()
    best_actions = []
    for action in actions:
        val = block_evaluation_function(game_state.generate_successor(action, MAX_AGENT))
        if val == 1:
            best_actions.append(action)
    if len(best_actions) == 0:
        return None
    r = random.randint(0, len(best_actions) - 1)
    return best_actions[r]


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function=None, depth=2):
        self.evaluation_function = evaluation_function
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class RandomAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        actions = game_state.get_legal_actions()
        if list(actions):
            r = random.randint(0, len(actions) - 1)
            return actions[r]
        return np.array([])


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        max_val = float("-inf")
        best_action = np.array([])
        actions = game_state.get_legal_actions()
        scores = []
        for action in actions:
            next_state = game_state.generate_successor(action, MAX_AGENT)
            diff = game_state.score - next_state.score
            agent = MIN_AGENT if diff == 0 else MAX_AGENT
            cur_val = self._minmax_helper(next_state, agent, self.depth - 0.5)
            scores.append(cur_val)
            if cur_val > max_val:
                max_val = cur_val
                best_action = action
        if max_val == min(scores):
            new_action = smart_random_play(game_state)
            if new_action is not None:
                best_action = new_action
        return best_action

    def _minmax_helper(self, cur_state, agent, depth):
        if depth == 0 or cur_state.is_done():
            evaluation = self.evaluation_function(cur_state)
            return evaluation
        max_val = float("-inf")
        min_val = np.inf
        for action in cur_state.get_legal_actions():
            next_state = cur_state.generate_successor(action, agent)
            diff = cur_state.score - next_state.score
            if agent == MIN_AGENT:
                diff = cur_state.opponent_score - next_state.opponent_score
            next_agent = 1 - agent if diff == 0 else agent
            evaluation = self._minmax_helper(next_state, next_agent, depth - 0.5)
            if evaluation > max_val and agent == MAX_AGENT:
                max_val = evaluation
            if evaluation < min_val and agent == MIN_AGENT:
                min_val = evaluation
        if agent == MAX_AGENT:
            return max_val
        else:
            return min_val


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def __init__(self, evaluation_function=None, depth=2, ordering_function=lambda x: 0):
        super().__init__(evaluation_function, depth)
        self.order = ordering_function

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        best_action = np.array([])
        max_score = float("-inf")
        actions = game_state.get_legal_actions()
        states = [(game_state.generate_successor(action, MAX_AGENT), action) for action in
                  actions]
        states.sort(key=lambda x: self.order(x[0]), reverse=True)
        scores = []
        for state, action in states:
            cur_score = self._find_score(state, self.depth - 0.5, MIN_AGENT, max_score)
            scores.append(cur_score)
            if cur_score > max_score:
                max_score = cur_score
                best_action = action
        if max_score == min(scores):
            new_action = smart_random_play(game_state)
            if new_action is not None:
                best_action = new_action
        return best_action

    def _find_score(self, state, depth, agent, parent_val):
        if depth == 0 or state.is_done():
            evaluation = self.evaluation_function(state)
            return evaluation
        if agent == MAX_AGENT:
            max_val = float("-inf")
            actions = state.get_legal_actions()
            states = [state.generate_successor(action, agent) for action in actions]
            states.sort(key=self.order, reverse=True)
            for next_state in states:
                diff = state.score - next_state.score
                if agent == MIN_AGENT:
                    diff = state.opponent_score - next_state.opponent_score
                next_agent = 1 - agent if diff == 0 else agent
                cur_val = self._find_score(next_state, depth - 0.5, next_agent, max_val)
                if cur_val > max_val:
                    max_val = cur_val
                if cur_val > parent_val:
                    break
            return max_val
        else:
            min_val = np.inf
            actions = state.get_legal_actions()
            states = [state.generate_successor(action, agent) for action in actions]
            states.sort(key=self.order)
            for next_state in states:
                diff = state.score - next_state.score
                if agent == MIN_AGENT:
                    diff = state.opponent_score - next_state.opponent_score
                next_agent = 1 - agent if diff == 0 else agent
                cur_val = self._find_score(next_state, depth - 0.5, next_agent, min_val)
                if cur_val < min_val:
                    min_val = cur_val
                if cur_val < parent_val:
                    break
            return min_val


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""
        best_action = np.array([])
        max_score = float("-inf")
        scores=[]
        for action in game_state.get_legal_actions():
            cur_state = game_state.generate_successor(action, MAX_AGENT)
            cur_score = self._expectimax_helper(cur_state, self.depth - 0.5, MIN_AGENT)
            scores.append(cur_score)
            if cur_score >= max_score:
                max_score = cur_score
                best_action = action
        if max_score == min(scores):
            new_action = smart_random_play(game_state)
            if new_action is not None:
                best_action = new_action
        return best_action

    def _expectimax_helper(self, state, depth, agent):
        if depth == 0:
            return self.evaluation_function(state)
        if agent == MAX_AGENT:
            max_val = float("-inf")
            actions = state.get_legal_actions()
            for action in actions:
                new_state = state.generate_successor(action, agent)
                diff = state.score - new_state.score
                if agent == MIN_AGENT:
                    diff = state.opponent_score - new_state.opponent_score
                next_agent = 1 - agent if diff == 0 else agent
                cur_val = self._expectimax_helper(new_state, depth - 0.5, next_agent)
                if cur_val >= max_val:
                    max_val = cur_val
            return max_val
        else:
            avg_val = 0.0
            actions = state.get_legal_actions()
            for action in actions:
                new_state = state.generate_successor(action, agent)
                diff = state.score - new_state.score
                if agent == MIN_AGENT:
                    diff = state.opponent_score - new_state.opponent_score
                next_agent = 1 - agent if diff == 0 else agent
                cur_val = self._expectimax_helper(new_state, depth - 0.5, next_agent)
                avg_val += cur_val
            if len(actions) == 0:
                return 0
            return avg_val / len(actions)
