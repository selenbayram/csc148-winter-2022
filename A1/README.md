# Raccoon Raiders!

## Assignment 1 for CSC148H1 at the University of Toronto.  

![raccoon_raiders](https://github.com/selenbayram/csc148-winter-2022/assets/113145976/11a369f6-a631-42fd-b733-3559d7265a84)


### Game Description

Raccoons try to climb into one of the available garbage cans. 
The main player aims to prevent the raccoons from reaching the garbage cans by trapping them using recycling bins. 
The game is similar to [Rodent's Revenge](https://en.wikipedia.org/wiki/Rodent%27s_Revenge) in terms of rules and design. 

_NOTE: The starter code is provided by the instructors and the copyright statement can be found at the beginning of each file._

### Classes (in a1.py)
_NOTE: The class descriptions are obtained from the assignment handout provided by the instructors._

**Character:** An abstract class that represents any character in the game. All characters must define move and get_char methods.

**TurnTaker:** An abstract class that inherits from Character that represents any character in the game that can take a turn. All turn-takers must define a take_turn method in addition to the Character abstract methods.

**Raccoon:** A class representing a raccoon that moves around randomly.

**SmartRaccoon:** A class representing a raccoon that moves in a less random way. This is drawn as a raccoon with glasses.

**GarbageCan:** A class representing a garbage can that a raccoon can climb into. A garbage can cannot be moved around. It is either locked or unlocked; a player can lock it, but a raccoon can open it.

**RecyclingBin:** A class representing a recycling bin that a raccoon cannot climb into, but a player can move around to trap the raccoons.

**Player:** The player that the user can move around via the arrow keys on their keyboard.

**GameBoard:** The game board that keeps track of the game objects. In this board, there is at most one item on each tile, with this exception: A raccoon can climb into an unlocked garbage can.
