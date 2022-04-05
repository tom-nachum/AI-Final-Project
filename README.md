# SOS-Solver

https://user-images.githubusercontent.com/69695824/135716972-2603511a-b8ec-497d-8a0f-fcb74201fc33.mp4

## Description
This is the final project in AI course. In this project, we built AI agents for the paper and pencil game 'SOS'.
We used search algorithms as: Alpha-Beta Pruning, Minimax and Expectimax
with different heuristics, and compared their performances to find the 
optimal agent (furthor details in AI final project subnittion.pdf).

## SOS Gameplay
This game is similar to tic-tac-toe, but has greater complexity.
There are two players against each other, which can place "S" or "O"
on the board. The winner is the player who has the greater number 
of "SOS" sequences either diagonally, horizontally, or vertically.
If a player succeeds to create SOS sequence, he gets another turn.
In case both players has the same number of "SOS" sequences, it's a draw.
The board size is nXn, of any n>=3. 

## Search Algorithms
We chose to solve this problem with search algorithms, as we can describe 
the game as a search tree, in which each node is a state of the game (representation of the board). 
For each state we can generate all the possible moves of the opponent, 
and recursivley create every possible gameplay scenarios.
The problem is that this search space is very large, and we can't just run throw 
all the options of possible games in advance. Thats why we use heuristics as 
evaluation functions for game states. Basically we give some score to a state based
on our understanding of the game rules, and which states are considered as "good" 
or "bad". A search agent will choose the action which maximize the score of the reached state.

## Our Implementation
We implemented a very intuitive UI of the SOS game in python, using tkinter library.
Then we implemented our agents: Minimax agent, Alpha-Beta Pruning agent and Expectimax agent.
As mentioned, we implemented heuristics in order to improve running time:
#### Score Heuristic
This heuristic rates a state according to the number of SOS sequences the agent completed. 
Using this heuristic with Minimax for example, will make the agent choose actions that
maximize it's number of SOS sequences.
#### Block Heuristic
This heuristics gives low score for states that allows to the opponent to complete a SOS sequence.
For example, if some action of the agent leeds to a state in which the board includes S_S or SO_
this action will get a low score, because it gives the opponent the opportunity to complete SOS 
sequence in the next turn.

## Results
After some data analysis we found out that the Alpha-Beta agent with the score heuristic, 
is the fastest agent, which was 33% faster than the Minimax agent. 
We expected for this result because as we learned in class,
the order heuristic of the nodes and the pruning of the search tree in Alpha-Beta algorithm 
causing significant improvement in running time.
