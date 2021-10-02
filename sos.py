import time

from game import *
from graphics import *
from multi_agents import *

DEFAULT_SIZE = 6


class Sos:
    """
    a class that represents the entire running of the application sos
    """

    def __init__(self, agent, opponent, is_graphic=True, board_size=DEFAULT_SIZE):
        self.is_graphic = is_graphic
        self.board_size = board_size
        self.graphics = Graphics(self)
        self.agent = agent
        self.opponent = opponent
        self.state = None
        self.game_type = -1
        if is_graphic:
            self.menu()

    def set_agent(self, agent):
        """
        sets agent strategy
        :param agent:
        :return:
        """
        self.agent = agent

    def set_opponent(self, opponent):
        """
        sets opponent strategy
        :param opponent:
        :return:
        """
        self.opponent = opponent

    def menu(self):
        """
        runs a main menu in the ui
        :return:
        """
        self.graphics.menu_screen()

    def game_loop(self):
        """
        runs a single game ui loop
        :return:
        """
        game = Game(self.board_size)
        self.game_type = 1
        self.graphics.game_screen(game, False)

    def ai_loop(self):
        """
        runs a full game either with a full ui or without ui
        :return:
        """
        sleep_sec = 0.5
        game = Game(self.board_size)
        self.game_type = 2
        self.state = GameState(self.board_size)
        if self.is_graphic:
            self.graphics.game_screen(game, True)
        while not game.done():
            agent = self.agent if game.player == MAX_AGENT else self.opponent
            action = agent.get_action(self.state)
            self.state = self.state.generate_successor(action, game.player)
            if self.is_graphic:
                self.graphics.choose_tile(action[0], action[1], action[2])
                time.sleep(sleep_sec)
            else:
                game.make_turn(action)
            if game.done():
                break
        return game.score


def test_agents(heuristic, num_of_runs=30, depth=2, board_size=6):
    """
    runs several games without ui and prints some statistics about them
    :param heuristic:
    :param num_of_runs:
    :param depth:
    :param board_size:
    :return:
    """
    ai_wins, ai_average, opponent_average, avg_time = 0, 0, 0, 0
    ai_ties = 0
    for i in range(1, num_of_runs + 1):
        start = time.time()
        agent = ExpectimaxAgent(heuristic, depth)
        opponent = MinmaxAgent(opponent_score_function, 0.5)
        sos = Sos(agent, opponent, False, board_size)
        scores = sos.ai_loop()
        ai_score, opponent_score = scores[0], scores[1]
        ai_average += ai_score
        opponent_average += opponent_score
        if ai_score > opponent_score:
            ai_wins += 1
        if ai_score == opponent_score:
            ai_ties += 1
        end = time.time()
        total = end - start
        avg_time += total
        print(f"Game {i}: AI: {ai_score}, Opponent: {opponent_score} | time: {total}")
    print(f"AI Victories: {ai_wins}")
    print(f"AI ties: {ai_ties}")
    print(f"Average of SOS: {ai_average / num_of_runs}")
    print(f"Opponent average of SOS: {opponent_average / num_of_runs}")
    print(f"Average Time: {avg_time / num_of_runs}")


def run_ui():
    """
    runs the ui version of the game
    :return:
    """
    agent = MinmaxAgent(block_evaluation_function, 1)
    opponent = RandomAgent()
    Sos(agent, opponent, True)


if __name__ == '__main__':
    # test_agents(score_evaluation_function, 30, 1, 6)
    run_ui()
