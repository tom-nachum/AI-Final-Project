import tkinter as tk
from sos import *

# sizes
DISTANCE = 70

# colors
BLUE = "#2593cf"
RED = "#b8311a"
BG_COLOR = "#9ad91c"
BUTTON_COLOR = "#d49f1c"


class Graphics:
    """a class running the graphics for the game using tkinter"""

    def __init__(self, sos):
        self.sos = sos
        self.window = tk.Tk()
        self.window.geometry("1200x800")
        self.window.configure(bg=BG_COLOR)
        self.game = None

    def update_game_size(self, size):
        """sets a board to the given size"""
        self.sos.board_size = size
        size_label = tk.Label(self.window, text="board size: " + str(self.sos.board_size),
                              font=("ariel", 12, "bold"), bg=BG_COLOR)
        size_label.place(x=450, y=80)

    def menu_screen(self):
        """the main menu screen of the game"""
        self.clear_window()
        title = tk.Label(self.window, text="S-O-S", font=("ariel", 40, "bold"),
                         bg=BG_COLOR)
        title.pack()
        self.update_game_size(6)
        start_button = tk.Button(self.window, text="PvP", font=("ariel", 24),
                                 relief=tk.GROOVE,
                                 command=self.sos.game_loop, bg=BUTTON_COLOR)
        start_button.place(x=400, y=200)
        start_button = tk.Button(self.window, text="AIvAI", font=("ariel", 24),
                                 relief=tk.GROOVE,
                                 command=self.sos.ai_loop, bg=BUTTON_COLOR)
        start_button.place(x=650, y=200)
        self.player_ai_menu("blue")
        self.player_ai_menu("red")
        self.sizes_menu_button()
        self.window.mainloop()

    def player_ai_menu(self, color):
        """the ai menu for both the main agent and the opponent agent"""
        ai = tk.Menubutton(self.window, text=color + " player \u2193", bg=BUTTON_COLOR, highlightcolor=BUTTON_COLOR)
        ai.menu = tk.Menu(ai, tearoff=0)
        ai["menu"] = ai.menu
        opponent = color == "red"
        if not opponent:
            ai.menu.add_command(label="score heuristic",
                                command=lambda: self.set_gui_agent(MinmaxAgent(score_evaluation_function, 1),
                                                                   "score heuristic player", opponent))
            ai.menu.add_command(label="block heuristic",
                                command=lambda: self.set_gui_agent(MinmaxAgent(min_score_evaluation_function, 1),
                                                                   "block heuristic player", opponent))
            ai.menu.add_command(label="alpha beta with score heuristic",
                                command=lambda: self.set_gui_agent(
                                    AlphaBetaAgent(score_evaluation_function, 1, score_evaluation_function),
                                    "alpha beta player           ", opponent))
            ai.menu.add_command(label="my score minus opponent score heuristic",
                                command=lambda: self.set_gui_agent(
                                    MinmaxAgent(good_minus_bad_evaluation_function, 1),
                                    "my score minus opponent score heuristic", opponent))
            ai.menu.add_command(label="combined heuristic",
                                command=lambda: self.set_gui_agent(
                                    MinmaxAgent(combined_heuristic, 1),
                                    "combined heuristic           ", opponent))
            ai.menu.add_command(label="expectimax score heuristic",
                                command=lambda: self.set_gui_agent(
                                    ExpectimaxAgent(good_minus_bad_evaluation_function, 1),
                                    "Expectimax score heuristic            ", opponent))
        else:
            ai.menu.add_command(label="random", command=lambda: self.set_gui_agent(RandomAgent(),
                                                                                   "random player", opponent))
            ai.menu.add_command(label="greedy",
                                command=lambda: self.set_gui_agent(MinmaxAgent(score_evaluation_function, 0.5),
                                                                   "greedy player", opponent))
        y_loc = 200 if color == "blue" else 240
        ai.place(x=570, y=y_loc)

    def set_gui_agent(self, agent, name, opponent):
        """sets an ai strategy for agent"""
        self.sos.set_opponent(agent) if opponent else self.sos.set_agent(agent)
        agent_label = tk.Label(self.window, text=name,
                               font=("ariel", 8, "bold"), bg=BG_COLOR)
        y_loc = 265 if opponent else 180
        agent_label.place(x=570, y=y_loc)

    def sizes_menu_button(self):
        """menu for different board sizes"""
        sizes = tk.Menubutton(self.window, text="board size \u2193", bg=BUTTON_COLOR, highlightcolor=BUTTON_COLOR)
        sizes.menu = tk.Menu(sizes, tearoff=0)
        sizes["menu"] = sizes.menu
        sizes.menu.add_command(label="3 x 3", command=lambda: self.update_game_size(3))
        sizes.menu.add_command(label="4 x 4", command=lambda: self.update_game_size(4))
        sizes.menu.add_command(label="5 x 5", command=lambda: self.update_game_size(5))
        sizes.menu.add_command(label="6 x 6", command=lambda: self.update_game_size(6))
        sizes.menu.add_command(label="7 x 7", command=lambda: self.update_game_size(7))
        sizes.menu.add_command(label="8 x 8", command=lambda: self.update_game_size(8))
        sizes.menu.add_command(label="9 x 9", command=lambda: self.update_game_size(9))
        sizes.place(x=600, y=80)

    def game_screen(self, game, is_ai):
        """runs a game of sos, we leave the main menu"""
        self.game = game
        self.clear_window()
        self.menu_buttons()
        title = tk.Label(self.window, text="S-O-S", font=("ariel", 40, "bold"),
                         bg=BG_COLOR)
        title.pack()
        self.turn_label()
        self.score_label()
        canvas = tk.Canvas(self.window, width=DISTANCE * self.sos.board_size + 10,
                           height=DISTANCE * self.sos.board_size, bg=BG_COLOR)
        canvas.place(x=DISTANCE - 10, y=DISTANCE - 10)
        # creating all buttons on the game board
        for i in range(self.sos.board_size):
            for j in range(self.sos.board_size):
                button_s = tk.Button(self.window, text="S", font=("ariel", 16),
                                     relief=tk.GROOVE,
                                     command=lambda row=i, col=j,
                                                    letter=1: self.choose_tile(letter,
                                                                               row, col),
                                     bg=BG_COLOR)
                button_o = tk.Button(self.window, text="O", font=("ariel", 16),
                                     relief=tk.GROOVE,
                                     command=lambda row=i, col=j,
                                                    letter=2: self.choose_tile(letter,
                                                                               row, col),
                                     bg=BG_COLOR)
                button_s.place(x=(i + 1) * DISTANCE, y=(j + 1) * DISTANCE)
                button_o.place(x=(i + 1) * DISTANCE + 30, y=(j + 1) * DISTANCE)
        if not is_ai:
            self.window.mainloop()
        else:
            self.window.update()

    def menu_buttons(self):
        """Main menu and restart buttons for in game screen"""
        menu_button = tk.Button(self.window, text="Main Menu", font=("ariel", 20, "bold"),
                                relief=tk.GROOVE,
                                command=self.sos.menu, bg=BUTTON_COLOR)
        menu_button.place(x=DISTANCE * self.sos.board_size + 300, y=100)
        command = self.sos.game_loop if self.sos.game_type == 1 else self.sos.ai_loop
        restart_button = tk.Button(self.window, text="Restart",
                                   font=("ariel", 20, "bold"), relief=tk.GROOVE,
                                   command=command, bg=BUTTON_COLOR)
        restart_button.place(x=DISTANCE * self.sos.board_size + 300, y=200)

    def choose_tile(self, letter, i, j):
        """what happens when a tile is chosen in the ui. plays a move in the game"""
        is_ok = self.game.choose_tile(letter, i, j)
        text = "S" if letter == 1 else "O"
        if is_ok != -1:
            color = BLUE if self.game.get_player() == 0 else RED
            letter_label = tk.Label(self.window, text=text, font=("ariel", 25, "bold"),
                                    fg=color, bg=BG_COLOR, width=3)
            letter_label.place(x=(i + 1) * DISTANCE, y=(j + 1) * DISTANCE)
            old_score = self.game.score[:]
            self.gui_update_score(i, j)
            self.gui_switch_turn(old_score)
            self.window.update()
        if self.game.done():
            self.show_winner()

    def gui_switch_turn(self, old_score):
        """switch the turn both in game and in gui"""
        self.game.switch_turn(old_score)
        self.turn_label()

    def gui_update_score(self, i, j):
        """updates the score and crosses the relevant sos's"""
        row_lines = self.game.sos_in_row(i, j)
        color = BLUE if self.game.get_player() == 0 else RED
        for line in row_lines:
            frame = tk.Frame(width=3, height=2 * DISTANCE, bg=color)
            row_loc = (line[0] + 1) * DISTANCE + 30
            col_loc = (line[1] + 1) * DISTANCE + 20
            frame.place(x=row_loc, y=col_loc)
        col_lines = self.game.sos_in_col(i, j)
        for line in col_lines:
            frame = tk.Frame(width=2 * DISTANCE, height=3, bg=color)
            row_loc = (line[0] + 1) * DISTANCE + 40
            col_loc = (line[1] + 1) * DISTANCE + 20
            frame.place(x=row_loc, y=col_loc)
        diag_lines = self.game.sos_in_diag(i, j)
        for line in diag_lines:
            self.draw_diag(color, line, False)
        diag_lines2 = self.game.sos_in_diag2(i, j)
        for line in diag_lines2:
            self.draw_diag(color, line, True)
        self.game.update_scores(i, j)
        self.score_label()

    def draw_diag(self, color, line, is_reversed):
        """draws a diagonal line"""
        small = 3
        for k in range(50):
            frame = tk.Frame(width=small + 2, height=small, bg=color)
            row_loc = (line[0] + 1) * DISTANCE + 25 + k * small
            col_loc = (line[1] + 1) * DISTANCE + 20 - k * small if is_reversed \
                else (line[1] + 1) * DISTANCE + 20 + k * small
            frame.place(x=row_loc, y=col_loc)

    def score_label(self):
        """a label for score with matching colors"""
        score_label = tk.Label(self.window, text="score", font=("ariel", 14, "bold"),
                               bg=BG_COLOR)
        score_label.place(x=self.sos.board_size * DISTANCE + 100, y=180)
        player_1 = tk.Label(self.window, text="player1: " + str(self.game.score[0]),
                            font=("ariel", 14, "bold"),
                            fg=BLUE, bg=BG_COLOR)
        player_1.place(x=self.sos.board_size * DISTANCE + 100, y=220)
        player_2 = tk.Label(self.window, text="player2: " + str(self.game.score[1]),
                            font=("ariel", 14, "bold"),
                            fg=RED, bg=BG_COLOR)
        player_2.place(x=self.sos.board_size * DISTANCE + 100, y=260)

    def turn_label(self):
        """a label to mark who's turn it is"""
        turn_color = BLUE if self.game.get_player() == 0 else RED
        trun_label = tk.Label(self.window,
                              text="player " + str(self.game.get_player() + 1) + " turn",
                              font=("ariel", 14, "bold"), fg=turn_color, bg=BG_COLOR)
        trun_label.place(x=self.sos.board_size * DISTANCE + 100, y=80)

    def show_winner(self):
        """ a winner label for the end of the game"""
        winner = self.game.get_winner()
        win_text = "Draw"
        win_color = "gray"
        if winner != -1:
            win_text = "Winner is player: " + str(winner + 1)
            win_color = BLUE if winner == 0 else RED
        letter_label = tk.Label(self.window, text=win_text, font=("ariel", 30, "bold"),
                                fg=win_color, bg=BG_COLOR)
        letter_label.place(x=100, y=0)

    def clear_window(self):
        """ clears the screen"""
        for widget in self.window.winfo_children():
            widget.destroy()

    def close_screen(self):
        """closes the gui screen"""
        self.window.destroy()
