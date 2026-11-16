Basic Strategy
1. implement Gomoku: to play Gomoku based on the subject
2. implement Gomoku AI
- heuristic function: a function to evaluate how favorable a board position is for each player
- minimax: an algorithim that search possible future moves and determine the best next move in a time
3. optimaize
- alpha-beta pruning: a way that skip the cadinate branching that cannnot affect final decision
- Move Ordring: a way that prioritize the next moves based on heuristic function
- caching: Reuse the evaluated board position
- etc
4. GUI
- display gomoku, stones and AI thinking time
- allow user interact to play against AI
5. bonus: change the rules to be able to play fairly the game

---
class player (abstract)
-> get_move()
- HumanPlayer
- AIPlayer

Class Game Rule (static class)

class Gomoku:
- Game Rule:  static class
- two player: tuple(Player Class)
[Black, Whilte]
- 19 * 19 board: tuple
-> Black: 1
-> White: -1
-> Empty: 0

Gomoku
Start
1. if current user has is_five=true or 10 of the opposite's stone
-> print the report about Win
2. First player(Black) chooses a position on the board
-> need to get the selected position from the player
3. Check if the position is valid (not already occupied)
  Condition (if it's true, it can arise exception error)
   - Check whether this position is already occupied
   - Check whether this position is within the board range
  if the position is valid, update the board.
4. Game Rule(static class) 
- is_five(flag): Check if the current user has won (5 or more aligned stones) 
   True: is_five in Current User Class is true
- is_capture(flag): Check if any player can capture the pair
  True: Gomoku Class update the board, current user get the the opposite's stone, the oppsite's is_five get false
5. Change the player again from 1

Question
- 