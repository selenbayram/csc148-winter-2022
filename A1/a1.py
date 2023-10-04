"""A1: Raccoon Raiders game objects (all tasks)

CSC148, Winter 2022

This code is provided solely for the personal and private use of students
taking the CSC148 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of this
code, whether as given or with any changes, are expressly prohibited.

Authors: Diane Horton, Sadia Sharmin, Dina Sabie, Jonathan Calver, and
Sophia Huynh.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Diane Horton, Sadia Sharmin, Dina Sabie, Jonathan Calver,
and Sophia Huynh.

=== Module Description ===
This module contains all of the classes necessary for a1_game.py to run.
"""

from __future__ import annotations

import random
from random import shuffle
from typing import List, Tuple, Optional, Union

# Each raccoon moves every this many turns
RACCOON_TURN_FREQUENCY = 20

# Directions dx, dy
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [LEFT, UP, RIGHT, DOWN]


def get_shuffled_directions() -> List[Tuple[int, int]]:
    """
    Provided helper that returns a shuffled copy of DIRECTIONS.
    You should use this where appropriate
    >>> k = get_shuffled_directions()
    >>> UP in k
    True
    """
    to_return = DIRECTIONS[:]
    shuffle(to_return)
    return to_return


class GameBoard:
    """A game board on which the game is played.

    === Public Attributes ===
    ended:
        whether this game has ended or not
    turns:
        how many turns have passed in the game
    width:
        the number of squares wide this board is
    height:
        the number of squares high this board is

    === Representation Invariants ===
    turns >= 0
    width > 0
    height > 0
    No tile in the game contains more than 1 character, except that a tile
    may contain both a Raccoon and an open GarbageCan.

    === Sample Usage ===
    See examples in individual method docstrings.
    """
    # === Private Attributes ===
    # _player:
    #   the player of the game
    # _master:
    #   the dict containing all character data
    # _raccoons:
    #   the list of all raccoons
    # _bins:
    #   the list of all bins
    # _considered:
    #   the list of considered recycling bins
    # _considered_coords:
    #   the list of considered coordinates
    # _bin_c:
    #   the list of recycling bin coordinates
    # Something to store all tiles used up

    ended: bool
    turns: int
    width: int
    height: int
    _player: Optional[Player]
    _master: dict
    _raccoons: list
    _bins: list
    _considered: list
    _considered_coords: list
    _bin_c: list

    def __init__(self, w: int, h: int) -> None:
        """Initialize this Board to be of the given width <w> and height <h> in
        squares. A board is initially empty (no characters) and no turns have
        been taken.

        >>> b = GameBoard(3, 3)
        >>> b.width == 3
        True
        >>> b.height == 3
        True
        >>> b.turns == 0
        True
        >>> b.ended
        False
        """

        self._bin_c = []
        self.ended = False
        self.turns = 0

        self.width = w
        self.height = h

        self._considered = []
        self._considered_coords = []

        self._player = None
        self._master = {}
        self._raccoons = []
        self._bins = []

    def add_to_dict(self, r: Union[Character, str], x: int, y: int) -> None:
        """
        This helper function is used to track where each character is.
        Also used to check if the tile is available by creating a temporary
        list with all coordinates. This list is used to check all values NOT
        used up and placing character within these bounds and on_board.

        r is self
        x is self.x
        y is self.y

        THIS MUST BE CALLED EVERYTIME A CHARACTER MOVES!!!!!
        WE CAN USE KEYS TO SEE ALL CHARS ON BOARD
        WE CAN USE VALUES TO SEE ALL SPACES USED

        >>> b = GameBoard(2, 2)
        >>> r_ = 'B'
        >>> x_ = 1
        >>> y_ = 1
        >>> b.add_to_dict(r_, x_, y_)
        >>> print(b._master)
        {'B': [1, 1]}
        """

        self._master[r] = [x, y]
        return None

    def place_character(self, c: Character) -> None:
        """Record that character <c> is on this board.

        This method should only be called from Character.__init__.

        The decisions you made about new private attributes for class GameBoard
        will determine what you do here.

        Preconditions:
        - c.board == self
        - Character <c> has not already been placed on this board.
        - The tile (c.x, c.y) does not already contain a character, with the
        exception being that a Raccoon can be placed on the same tile where
        an unlocked GarbageCan is already present.

        Note: The testing will depend on this method to set up the board,
        as the Character.__init__ method calls this method.

        >>> b = GameBoard(3, 2)
        >>> r = Raccoon(b, 1, 1)  # when a Raccoon is created, it is placed on b
        >>> b.at(1, 1)[0] == r  # requires GameBoard.at be implemented to work
        True
        """
        self.add_to_dict(c, c.x, c.y)

        if isinstance(c, Player):  # if it is a player make it (0, 0)
            # c.x = 0
            # c.y = 0
            self._player = c

        else:  # c.get_char() == 'R' or 'G':  # add characters here!!!

            if c.get_char() == 'R':
                self._raccoons.append(c)
            if c.get_char() == 'S':
                self._raccoons.append(c)
            if c.get_char() == 'B':
                self._bins.append(c)
                self._bin_c.append([c.x, c.y])

    def at(self, x: int, y: int) -> List[Character]:
        """Return the characters at tile (x, y).

        If there are no characters or if the (x, y) coordinates are not
        on the board, return an empty list.
        There may be as many as two characters at one tile,
        since a raccoon can climb into a garbage can.

        Note: The testing will depend on this method to allow us to
        access the Characters on your board, since we don't know how
        you have chosen to store them in your private attributes,
        so make sure it is working properly!

        >>> b = GameBoard(3, 2)
        >>> r = Raccoon(b, 1, 1)
        >>> b.at(1, 1)[0] == r
        True
        >>> p = Player(b, 0, 1)
        >>> b.at(0, 1)[0] == p
        True
        >>> g = RecyclingBin(b, 1, 0)
        >>> b.at(1, 0)[0] == g
        True
        >>> r2 = Raccoon(b, 1, 0)
        >>> b.at(1, 0)[1] == r2
        True
        >>> b_ = GameBoard(10, 10)
        >>> b_.setup_from_grid("-------BBB\\nO------PBS\\\
        \\nBB-BB----B\\nB-----B@--\\n--B--B----\\nB-B-------\\\
        \\n---BBB--@-\\nBB--------\\n-B---B---B\\nB-@-----B-")
        >>> print(b_)
        -------BBB
        O------PBS
        BB-BB----B
        B-----B@--
        --B--B----
        B-B-------
        ---BBB--@-
        BB--------
        -B---B---B
        B-@-----B-
        >>> len(b_.at(2, 9)) == 2
        True
        """
        temp = []
        for key in self._master:
            if self._master[key] == [x, y]:
                temp.append(key)
        return temp

        # if value is in self.master
        # return the key and use get_char on the key

        # USE HELPER Gameboard.on_board to make sure it is a proper input
        # Create a masterlist/dict of all spaces taken up Private Attribute
        # Loop through it and see if it is taken up

    def to_grid(self) -> List[List[chr]]:
        """
        Return the game state as a list of lists of chrs (letters) where:

        'R' = Raccoon
        'S' = SmartRaccoon
        'P' = Player
        'C' = closed GarbageCan
        'O' = open GarbageCan
        'B' = RecyclingBin
        '@' = Raccoon in GarbageCan
        '-' = Empty tile

        Each inner list represents one row of the game board.

        >>> b = GameBoard(3, 2)
        >>> _ = Player(b, 0, 0)
        >>> _ = SmartRaccoon(b, 0, 1)
        >>> _ = Raccoon(b, 2, 0)
        >>> _ = GarbageCan(b, 2, 1, False)
        >>> _ = SmartRaccoon(b, 2, 1)
        >>> _ = GarbageCan(b, 1, 1, False)
        >>> b.to_grid()
        [['P', '-', 'R'], ['S', 'O', '@']]
        """
        result = []

        for y in range(self.height):
            row = []

            for x in range(self.width):

                if len(self.at(x, y)) == 0:
                    row.append('-')
                elif len(self.at(x, y)) == 2:
                    row.append('@')
                elif isinstance(self.at(x, y)[0], SmartRaccoon):
                    row.append('S')
                elif isinstance(self.at(x, y)[0], Raccoon):
                    row.append('R')
                elif isinstance(self.at(x, y)[0], GarbageCan):
                    row.append(self.at(x, y)[0].get_char())
                elif isinstance(self.at(x, y)[0], Player):
                    row.append('P')
                elif isinstance(self.at(x, y)[0], RecyclingBin):
                    row.append('B')
            result.append(row)

        return result

    def __str__(self) -> str:
        """
        Return a string representation of this board.

        The format is the same as expected by the setup_from_grid method.

        >>> b = GameBoard(3, 2)
        >>> _ = Raccoon(b, 1, 1)
        >>> print(b)
        ---
        -R-
        >>> _ = Player(b, 0, 0)
        >>> _ = GarbageCan(b, 2, 1, False)
        >>> _ = Raccoon(b, 2, 1)
        >>> print(b)
        P--
        -R@
        >>> str(b)
        'P--\\n-R@'
        >>> _b = GameBoard(5, 5)
        >>> s = SmartRaccoon(_b, 4, 4)
        >>> _ = GarbageCan(_b, 2, 4, False)
        >>> _ = GarbageCan(_b, 4, 3, False)
        >>> _ = GarbageCan(_b, 2, 0, False)
        >>> print(_b)
        --O--
        -----
        -----
        ----O
        --O-S
        """
        rows = self.to_grid()
        result = ''

        for r in rows:
            row = ''
            for c in r:
                row = row + c
            result = result + row + '\n'

        return result.strip()

    def setup_from_grid(self, grid: str) -> None:
        """
        Set the state of this GameBoard to correspond to the string <grid>,
        which represents a game board using the following chars:

        'R' = Raccoon not in a GarbageCan
        'P' = Player
        'C' = closed GarbageCan
        'O' = open GarbageCan
        'B' = RecyclingBin
        '@' = Raccoon in GarbageCan
        '-' = Empty tile

        There is a newline character between each board row.

        >>> b = GameBoard(4, 4)
        >>> b.setup_from_grid('P-B-\\n-BRB\\n--BB\\n-C--')
        >>> str(b)
        'P-B-\\n-BRB\\n--BB\\n-C--'
        """
        lines = grid.split("\n")
        width = len(lines[0])
        height = len(lines)
        self.__init__(width, height)  # reset the board to an empty board
        y = 0
        for line in lines:
            x = 0
            for char in line:
                if char == 'R':
                    Raccoon(self, x, y)
                elif char == 'S':
                    SmartRaccoon(self, x, y)
                elif char == 'P':
                    Player(self, x, y)
                elif char == 'O':
                    GarbageCan(self, x, y, False)
                elif char == 'C':
                    GarbageCan(self, x, y, True)
                elif char == 'B':
                    RecyclingBin(self, x, y)
                elif char == '@':
                    GarbageCan(self, x, y, False)
                    Raccoon(self, x, y)  # always makes it a Raccoon
                    # Note: the order mattered above, as we have to place the
                    # Raccoon BEFORE the GarbageCan (see the place_character
                    # method precondition)
                x += 1
            y += 1

    # a helper method you may find useful in places
    def on_board(self, x: int, y: int) -> bool:
        """Return True iff the position x, y is within the boundaries of this
        board (based on its width and height), and False otherwise.
        >>> b = GameBoard(8, 8)
        >>> b.on_board(9, 9)
        False
        """
        return 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1

    def give_turns(self) -> None:
        """Give every turn-taking character one turn in the game.

        The Player should take their turn first and the number of turns
        should be incremented by one. Then each other TurnTaker
        should be given a turn if RACCOON_TURN_FREQUENCY turns have occurred
        since the last time the TurnTakers were given their turn.

        After all turns are taken, check_game_end should be called to
        determine if the game is over.

        Precondition:
        self._player is not None

        >>> b = GameBoard(4, 3)
        >>> p = Player(b, 0, 0)
        >>> r = Raccoon(b, 1, 1)
        >>> b.turns
        0
        >>> for _ in range(RACCOON_TURN_FREQUENCY - 1):
        ...     b.give_turns()
        >>> b.turns == RACCOON_TURN_FREQUENCY - 1
        True
        >>> (r.x, r.y) == (1, 1)  # Raccoon hasn't had a turn yet
        True
        >>> (p.x, p.y) == (0, 0)  # Player hasn't had any inputs
        True
        >>> p.record_event(RIGHT)
        >>> b.give_turns()
        >>> (r.x, r.y) != (1, 1)  # Raccoon has had a turn!
        True
        >>> (p.x, p.y) == (1, 0)  # Player moved right!
        True
        """

        self._player.take_turn()
        # if player.move == True
        self.turns += 1  # PROVIDED, DO NOT CHANGE

        if self.turns % RACCOON_TURN_FREQUENCY == 0:  # PROVIDED, DO NOT CHANGE
            for key in self._master:
                if key.get_char() == 'R':
                    key.take_turn()
                if key.get_char() == 'S':
                    key.take_turn()
        self.check_game_end()  # PROVIDED, DO NOT CHANGE

    def handle_event(self, event: Tuple[int, int]) -> None:
        """Handle a user-input event.

        The board's Player records the event that happened, so that when the
        Player gets a turn, it can make the move that the user input indicated.
        """
        self._player.record_event(event)

    def check_game_end(self) -> Optional[int]:
        """Check if this game has ended. A game ends when all the raccoons on
        this game board are either inside a can or trapped.

        If the game has ended:
        - update the ended attribute to be True
        - Return the score, where the score is given by:
            (number of raccoons trapped) * 10 + the adjacent_bin_score
        If the game has not ended:
        - update the ended attribute to be False
        - return None

        >>> b = GameBoard(3, 2)
        >>> _ = SmartRaccoon(b, 1, 0)
        >>> _ = Player(b, 0, 0)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> b.check_game_end() is None
        True
        >>> b.ended
        False
        >>> _ = RecyclingBin(b, 2, 0)
        >>> b.check_game_end()
        11
        >>> b.ended
        True
        >>> b_ = GameBoard(10, 10)
        >>> b_.setup_from_grid('-------BBB\\nO------PBS\\nBB-BB----B\\\
        \\nB-----B@--\\n--B--B----\\nB-B-------\\n---BBB--@-\\nBB--------\\\
        \\n-B---B---B\\nB-@-----B-')
        >>> b_.check_game_end()
        14
        >>> b = GameBoard(10, 10)
        >>> b.setup_from_grid("---B-----B\\n-------@--\\nB-----B-B-\\\
        \\nBBBBB-O---\\nSBB------B\\nBSP------B\\nBB----BBO-\\n------B--B\\\
        \\n---@-B----\\n-B----B--B")
        >>> b.check_game_end()
        28
        >>> b = GameBoard(10, 10)
        >>> b.setup_from_grid("SP-BB--B--\\nBB-BB---B-\\nB--B-B@B--\\\
        \\nB-------BB\\n--------B-\\n--@-------\\n----------\\n-O---B--B-\\\
        \\n-B---@---B\\n--B-BB-B-B")
        >>> b.check_game_end()
        15
        """
        total_raccoons = len(self._raccoons)
        trapped = 0
        canned = 0

        for raccoon in self._raccoons:
            if len(self.at(raccoon.x, raccoon.y)) == 2:
                canned += 1
            elif raccoon.check_trapped():
                trapped += 1

        if total_raccoons == (trapped + canned):
            self.ended = True
            temp = (trapped * 10)
            temp2 = self.adjacent_bin_score()
            temp3 = temp + temp2
            return temp3
        else:
            return None

    def adjacent_bin_score(self) -> int:
        """
        >>> b = GameBoard(3, 3)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 0, 0)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> print(b)
        B--
        -B-
        --B
        >>> b.adjacent_bin_score()
        1
        >>> _ = RecyclingBin(b, 2, 1)
        >>> print(b)
        B--
        -BB
        --B
        >>> b.adjacent_bin_score()
        3
        >>> _ = RecyclingBin(b, 0, 1)
        >>> print(b)
        B--
        BBB
        --B
        >>> b.adjacent_bin_score()
        5
        >>> b_ = GameBoard(10, 10)
        >>> b_.setup_from_grid("-------BBB\\nO------PBS\\nBB-BB----B\\\
        \\nB-----B@--\\n--B--B----\\nB-B-------\\n---BBB--@-\\nBB--------\\\
        \\n-B---B---B\\nB-@-----B-")
        >>> b_.adjacent_bin_score()
        4
        """
        self._considered = []
        self._considered_coords = []
        count = 0
        highest = 0
        s = []

        # BASE CASE
        if len(self._considered) == len(self._bins):
            return count

            # loop through recycling bins
        for rec in self._bins:
            self._considered.append(rec)  # add bin it to considered
            coordinate = [rec.x, rec.y]  # current coordinate of bin
            self._considered_coords.append(coordinate)
            le = [(coordinate[0] - 1), coordinate[1]]  # left tile
            r = [(coordinate[0] + 1), coordinate[1]]  # right tile
            u = [coordinate[0], (coordinate[1] - 1)]  # up tile
            d = [coordinate[0], (coordinate[1] + 1)]  # down tile
            count = 0
            s.clear()

            # is there any bin adjacent to this bin?????
            # if there are adjacent bins, add it to the stack and count it
            for rec2 in self._bins:
                if u == [rec2.x, rec2.y] and u not in self._considered_coords:
                    self._considered.append(u)  # add counted bins to considered
                    self._considered_coords.append([rec2.x, rec2.y])
                    s.append(u)  # and stack
                    count += 1
                if d == [rec2.x, rec2.y] and d not in self._considered_coords:
                    self._considered.append(d)
                    self._considered_coords.append([rec2.x, rec2.y])
                    s.append(d)
                    count += 1
                if le == [rec2.x, rec2.y] and le not in self._considered_coords:
                    self._considered.append(le)
                    self._considered_coords.append([rec2.x, rec2.y])
                    s.append(le)
                    count += 1
                if r == [rec2.x, rec2.y] and r not in self._considered_coords:
                    self._considered.append(r)
                    self._considered_coords.append([rec2.x, rec2.y])
                    s.append(r)
                    count += 1

            count += 1  # count the current bin

            # NOW I HAVE A STACK OF DIRECTLY ADJACENT BINS
            # CHECK HOW MANY THESE ARE ADJACENT TO
            if count > 1:
                check = self.helper_adjacent(s)
                count += check

            if count >= highest:  # return the highest number of adjacent bins
                highest = count

        return highest

    def helper_adjacent(self, direct: list) -> int:
        """A helper function for the method adjacent_bin_score with the
        parameter <direct>.
        >>> b = GameBoard(3, 3)
        >>> _ = RecyclingBin(b, 0, 0)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> _ = RecyclingBin(b, 2, 1)
        >>> _ = RecyclingBin(b, 0, 1)
        >>> print(b)
        B--
        BBB
        --B
        >>> s = [[0, 1]]
        >>> b.helper_adjacent(s)
        4
        """
        count = 0
        for rec in direct:
            coordinate = rec  # current coordinate of bin
            self._considered_coords.append(rec)
            le = [(coordinate[0] - 1), coordinate[1]]  # left tile
            r = [(coordinate[0] + 1), coordinate[1]]  # right tile
            u = [coordinate[0], (coordinate[1] - 1)]  # up tile
            d = [coordinate[0], (coordinate[1] + 1)]  # down tile

            # check around this bin
            if (u in self._bin_c) and (u not in self._considered_coords):
                self._considered_coords.append(u)
                # add counted bins to considered
                direct.append(u)  # and stack
                count += 1
            if (d in self._bin_c) and (d not in self._considered_coords):
                self._considered_coords.append(d)
                direct.append(d)
                count += 1
            if (le in self._bin_c) and (le not in self._considered_coords):
                self._considered_coords.append(le)
                direct.append(le)
                count += 1
            if (r in self._bin_c) and (r not in self._considered_coords):
                self._considered_coords.append(r)
                direct.append(r)
                count += 1
        return count


class Character:
    """A character that has (x,y) coordinates and is associated with a given
    board.

    This class is abstract and should not be directly instantiated.

    NOTE: To reduce the amount of documentation in subclasses, we have chosen
    not to repeat information about the public attributes in each subclass.
    Remember that the attributes are not inherited, but only exist once we call
    the __init__ of the parent class.

    === Public Attributes ===
    board:
        the game board that this Character is on
    x, y:
        the coordinates of this Character on the board

    === Representation Invariants ===
    x, y are valid coordinates in board (i.e. board.on_board(x, y) is True)
    """

    board: GameBoard
    x: int
    y: int

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Character with board <b>, and
        at tile (<x>, <y>).

        When a Character is initialized, it is placed on board <b>
        by calling the board's place_character method. Refer to the
        preconditions of place_character, which must be satisfied.
        """
        self.board = b
        self.x, self.y = x, y
        self.board.place_character(self)  # this associates self with the board!

    def move(self, direction: Tuple[int, int]) -> bool:
        """
        Move this character to the tile

        (self.x + direction[0], self.y + direction[1]) if possible. Each child
        class defines its own version of what is possible.

        Return True if the move was successful and False otherwise.

        """
        raise NotImplementedError

    def get_char(self) -> chr:
        """
        Return a single character (letter) representing this Character.
        """
        raise NotImplementedError


# Note: You can safely ignore PyCharm's warning about this class
# not implementing abstract method(s) from its parent class.
class TurnTaker(Character):
    """
    A Character that can take a turn in the game.

    This class is abstract and should not be directly instantiated.
    """

    def take_turn(self) -> None:
        """
        Take a turn in the game. This method must be implemented in any subclass
        """
        raise NotImplementedError


class RecyclingBin(Character):
    """A recycling bin in the game.

    === Sample Usage ===
    >>> rb = RecyclingBin(GameBoard(4, 4), 2, 1)
    >>> rb.x, rb.y
    (2, 1)
    """

    def move(self, direction: Tuple[int, int]) -> bool:
        """Move this recycling bin to tile:
                (self.x + direction[0], self.y + direction[1])
        if possible and return whether or not this move was successful.

        If the new tile is occupied by another RecyclingBin, push
        that RecyclingBin one tile away in the same direction and take
        its tile (as described in the Assignment 1 handout).

        If the new tile is occupied by any other Character or if it
        is beyond the boundaries of the board, do nothing and return False.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> rb = RecyclingBin(b, 0, 0)
        >>> rb.move(UP)
        False
        >>> rb.move(DOWN)
        True
        >>> b.at(0, 1) == [rb]
        True
        """
        check = self.x + direction[0], self.y + direction[1]  # future direction

        if self.board.on_board(check[0], check[1]):
            # tile within the boundaries of game board
            if len(self.board.at(check[0], check[1])) == 0:
                # tile is empty
                self.x = check[0]
                self.y = check[1]
                self.board.add_to_dict(self, self.x, self.y)
                self.board.at(check[0], check[1]).append(self)
                return True
            elif isinstance(self.board.at(check[0], check[1])[0], RecyclingBin):
                # there is another recycling bin on the tile
                next_bin = self.board.at(check[0], check[1])[0]
                if next_bin.move(direction):
                    # the other recycling bin moves the same way
                    self.x = check[0]
                    self.y = check[1]
                    self.board.add_to_dict(self, self.x, self.y)
                    self.board.at(check[0], check[1]).append(self)
                    return True
            else:
                return False

        return False

    def get_char(self) -> chr:
        """
        Return the character 'B' representing a RecyclingBin.
        """
        return 'B'


class Player(TurnTaker):
    """The Player of this game.

    === Sample Usage ===
    >>> b = GameBoard(3, 1)
    >>> p = Player(b, 0, 0)
    >>> p.record_event(RIGHT)
    >>> p.take_turn()
    >>> (p.x, p.y) == (1, 0)
    True
    >>> g = GarbageCan(b, 0, 0, False)
    >>> p.move(LEFT)
    True
    >>> g.locked
    True
    """
    # === Private Attributes ===
    # _last_event:
    #   The direction corresponding to the last keypress event that the user
    #   made, or None if there is currently no keypress event left to process
    _last_event: Optional[Tuple[int, int]]

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Player with board <b>,
        and at tile (<x>, <y>)."""

        TurnTaker.__init__(self, b, x, y)
        self._last_event = None

    def record_event(self, direction: Tuple[int, int]) -> None:
        """Record that <direction> is the last direction that the user
        has specified for this Player to move. Next time take_turn is called,
        this direction will be used.
        Precondition:
        direction is in DIRECTIONS
        """
        self._last_event = direction

    def take_turn(self) -> None:
        """Take a turn in the game.

        For a Player, this means responding to the last user input recorded
        by a call to record_event.
        """
        if self._last_event is not None:
            self.move(self._last_event)
            self._last_event = None

    def move(self, direction: Tuple[int, int]) -> bool:
        """Attempt to move this Player to the tile:
                (self.x + direction[0], self.y + direction[1])
        if possible and return True if the move is successful.

        If the new tile is occupied by a Racooon, a locked GarbageCan, or if it
        is beyond the boundaries of the board, do nothing and return False.

        If the new tile is occupied by a movable RecyclingBin, the player moves
        the RecyclingBin and moves to the new tile.

        If the new tile is unoccupied, the player moves to that tile.

        If a Player attempts to move towards an empty, unlocked GarbageCan, the
        GarbageCan becomes locked. The player's position remains unchanged in
        this case. Also return True in this case, as the Player has performed
        the action of locking the GarbageCan.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> p = Player(b, 0, 0)
        >>> p.move(UP)
        False
        >>> p.move(DOWN)
        True
        >>> b.at(0, 1) == [p]
        True
        >>> _ = RecyclingBin(b, 1, 1)
        >>> p.move(RIGHT)
        True
        >>> b.at(1, 1) == [p]
        True
        """
        check = self.x + direction[0], self.y + direction[1]

        if (self.board.on_board(check[0], check[1])) and \
                (not isinstance(self.board.at(check[0], check[1]), Raccoon)):
            # the tile is within the boundaries of the game board and
            # there isn't a raccoon there
            if len(self.board.at(check[0], check[1])) == 0:
                # the tile is empty
                self.x = check[0]
                self.y = check[1]
                self.board.add_to_dict(self, self.x, self.y)
                self.board.at(check[0], check[1]).append(self)
                return True
            elif isinstance(self.board.at(check[0], check[1])[0], GarbageCan):
                # there is a garbage can on the tile
                garbage_can = self.board.at(check[0], check[1])[0]
                if garbage_can.get_char() == 'C':
                    # the garbage can is locked
                    return False
                elif len(self.board.at(check[0], check[1])) != 2:
                    # the garbage can is unlocked and empty
                    garbage_can.locked = True
                    return True
            elif isinstance(self.board.at(check[0], check[1])[0], RecyclingBin):
                # there is a recycling bin on tile
                recycling_bin = self.board.at(check[0], check[1])[0]
                if recycling_bin.move(direction):
                    # recycling bin is moved according to its method
                    self.x = check[0]
                    self.y = check[1]
                    self.board.add_to_dict(self, self.x, self.y)
                    self.board.at(check[0], check[1]).append(self)
                    return True
            else:
                return False

        return False

    def get_char(self) -> chr:
        """
        Return the character 'P' representing this Player.
        """
        return 'P'


class Raccoon(TurnTaker):
    """A raccoon in the game.

    === Public Attributes ===
    inside_can:
        whether or not this Raccoon is inside a garbage can

    === Representation Invariants ===
    inside_can is True iff this Raccoon is on the same tile as an open
    GarbageCan.

    === Sample Usage ===
    >>> r = Raccoon(GameBoard(5, 5), 5, 10)
    >>> r.x, r.y
    (5, 10)
    >>> r.inside_can
    False
    """
    inside_can: bool

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Raccoon with board <b>, and
        at tile (<x>, <y>). Initially a Raccoon is not inside
        of a GarbageCan, unless it is placed directly inside an open GarbageCan.

        >>> r = Raccoon(GameBoard(11, 11), 5, 10)
        """
        self.inside_can = False
        # since this raccoon may be placed inside an open garbage can,
        # we need to initially set the inside_can attribute
        # BEFORE calling the parent init, which is where the raccoon is actually
        # placed on the board.
        TurnTaker.__init__(self, b, x, y)

    def check_trapped(self) -> bool:
        """Return True iff this raccoon is trapped. A trapped raccoon is
        surrounded on 4 sides (diagonals don't matter) by recycling bins, other
        raccoons (including ones in garbage cans), the player, and/or board
        edges. Essentially, a raccoon is trapped when it has nowhere it could
        move.

        Reminder: A racooon cannot move diagonally.

        >>> b = GameBoard(3, 3)
        >>> r = Raccoon(b, 2, 1)
        >>> _ = Raccoon(b, 2, 2)
        >>> _ = Player(b, 2, 0)
        >>> r.check_trapped()
        False
        >>> _ = RecyclingBin(b, 1, 1)
        >>> r.check_trapped()
        True
        """

        for direction in DIRECTIONS:
            check = self.x + direction[0], self.y + direction[1]
            symbol = self.board.at(check[0], check[1])

            if not symbol:
                if self.board.on_board(check[0], check[1]):
                    return False

            elif symbol[0].get_char() == 'O':
                return False

        return True

    def move(self, direction: Tuple[int, int]) -> bool:
        """Attempt to move this Raccoon in <direction> and return whether
        or not this was successful.

        If the tile one tile over in that direction is occupied by the Player,
        a RecyclingBin, or another Raccoon, OR if the tile is not within the
        boundaries of the board, do nothing and return False.

        If the tile is occupied by an unlocked GarbageCan that has no Raccoon
        in it, this Raccoon moves there and we have two characters on one tile
        (the GarbageCan and the Raccoon). If the GarbageCan is locked, this
        Raccoon uses this turn to unlock it and return True.

        If a Raccoon is inside of a GarbageCan, it will not move. Do nothing and
        return False.

        Return True if the Raccoon unlocks a GarbageCan or moves from its
        current tile.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> r = Raccoon(b, 0, 0)
        >>> r.move(UP)
        False
        >>> r.move(DOWN)
        True
        >>> b.at(0, 1) == [r]
        True
        >>> g = GarbageCan(b, 1, 1, True)
        >>> r.move(RIGHT)
        True
        >>> r.x, r.y  # Raccoon didn't change its position
        (0, 1)
        >>> not g.locked  # Raccoon unlocked the garbage can!
        True
        >>> r.move(RIGHT)
        True
        >>> r.inside_can
        True
        >>> len(b.at(1, 1)) == 2  # Raccoon and GarbageCan are both at (1, 1)!
        True
        """
        check = (self.x + direction[0], self.y + direction[1])

        if self.board.on_board(check[0], check[1]) and \
                (not isinstance(self.board.at(check[0], check[1]),
                                (Player, Raccoon, RecyclingBin))):
            # the tile is within boundaries of the game board and is not
            # occupied by either the player, a recycling bin, or another raccoon
            if self.get_char() == '@':
                # the raccoon is in a garbage can
                return False
            elif len(self.board.at(check[0], check[1])) == 0:
                # the raccoon is not in a garbage can and there is no other
                # characters on the tile
                self.x = check[0]
                self.y = check[1]
                self.board.add_to_dict(self, self.x, self.y)
                self.board.at(check[0], check[1]).append(self)
                return True
            elif isinstance(self.board.at(check[0], check[1])[0], GarbageCan):
                # the tile is occupied by a garbage can
                garbage_can = self.board.at(check[0], check[1])[0]
                if (garbage_can.get_char() == 'O') and \
                        (len(self.board.at(check[0], check[1])) != 2):
                    # the garbage can is open and there isn't a raccoon in it
                    self.x = check[0]
                    self.y = check[1]
                    self.inside_can = True
                    self.board.add_to_dict(self, self.x, self.y)
                    self.board.at(check[0], check[1]).append(self)
                    return True
                elif garbage_can.get_char() == 'O':
                    # the garbage can is open but has a raccoon in it
                    return False
                else:
                    # the garbage can is locked
                    garbage_can.locked = False
                    return True

        return False

    def take_turn(self) -> None:
        """Take a turn in the game.

        If a Raccoon is in a GarbageCan, it stays where it is.

        Otherwise, it randomly attempts (if it is not blocked) to move in
        one of the four directions, with equal probability.

        >>> b = GameBoard(3, 4)
        >>> r1 = Raccoon(b, 0, 0)
        >>> r1.take_turn()
        >>> (r1.x, r1.y) in [(0, 1), (1, 0)]
        True
        >>> r2 = Raccoon(b, 2, 1)
        >>> _ = RecyclingBin(b, 2, 0)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> r2.take_turn()  # Raccoon is trapped
        >>> r2.x, r2.y
        (2, 1)
        """
        possible_directions = []
        grid_board = self.board.to_grid()
        for d in DIRECTIONS:
            if (self.board.on_board(self.x + d[0], self.y + d[1])) and \
                    (grid_board[self.y + d[1]][self.x + d[0]] == 'O'
                     or grid_board[self.y + d[1]][self.x + d[0]] == '-'):
                possible_directions.append(d)

        if (not self.inside_can) and (possible_directions != []):
            self.move(random.choice(possible_directions))

    def get_char(self) -> chr:
        """
        Return '@' to represent that this Raccoon is inside a garbage can
        or 'R' otherwise.
        """
        if self.inside_can:
            return '@'
        return 'R'


class SmartRaccoon(Raccoon):
    """A smart raccoon in the game.

    Behaves like a Raccoon, but when it takes a turn, it will move towards
    a GarbageCan if it can see that GarbageCan in its line of sight.
    See the take_turn method for details.

    SmartRaccoons move in the same way as Raccoons.

    === Sample Usage ===
    >>> b = GameBoard(8, 1)
    >>> s = SmartRaccoon(b, 4, 0)
    >>> s.x, s.y
    (4, 0)
    >>> s.inside_can
    False
    """

    def take_turn(self) -> None:
        """Take a turn in the game.

        If a SmartRaccoon is in a GarbageCan, it stays where it is.

        A SmartRaccoon checks along the four directions for
        the closest non-occupied GarbageCan that has nothing blocking
        it from reaching that GarbageCan (except possibly the Player).

        If there is a tie for the closest GarbageCan, a SmartRaccoon
        will prioritize the directions in the order indicated in DIRECTIONS.

        If there are no GarbageCans in its line of sight along one of the four
        directions, it moves exactly like a Raccoon. A GarbageCan is in its
        line of sight if there are no other Raccoons, RecyclingBins, or other
        GarbageCans between this SmartRaccoon and the GarbageCan. The Player
        may be between this SmartRaccoon and the GarbageCan though.

        >>> b = GameBoard(8, 2)
        >>> s = SmartRaccoon(b, 4, 0)
        >>> _ = GarbageCan(b, 3, 1, False)
        >>> _ = GarbageCan(b, 0, 0, False)
        >>> _ = GarbageCan(b, 7, 0, False)
        >>> s.take_turn()
        >>> s.x == 5
        True
        >>> s.take_turn()
        >>> s.x == 6
        True
        >>> b = GameBoard(8, 6)
        >>> s = SmartRaccoon(b, 7, 5)
        >>> _ = GarbageCan(b, 2, 5, False)
        >>> _ = GarbageCan(b, 6, 3, False)
        >>> _ = GarbageCan(b, 2, 0, False)
        >>> print(b)
        --O-----
        --------
        --------
        ------O-
        --------
        --O----S
        >>> l = []
        >>> s.take_turn()
        >>> l.append((s.x, s.y))
        >>> l
        [(6, 5)]
        >>> print(b)
        --O-----
        --------
        --------
        ------O-
        --------
        --O---S-
        >>> s.take_turn()
        >>> l.append((s.x, s.y))
        >>> l
        [(6, 5), (6, 4)]
        >>> print(b)
        --O-----
        --------
        --------
        ------O-
        ------S-
        --O-----
        >>> b_ = GameBoard(8, 6)
        >>> s_ = SmartRaccoon(b_, 7, 5)
        >>> _ = GarbageCan(b_, 5, 5, False)
        >>> _ = GarbageCan(b_, 7, 3, False)
        >>> _ = GarbageCan(b_, 2, 0, False)
        >>> print(b_)
        --O-----
        --------
        --------
        -------O
        --------
        -----O-S
        >>> s_.take_turn()
        >>> print(b_)
        --O-----
        --------
        --------
        -------O
        --------
        -----OS-
         >>> s_.take_turn()
        >>> print(b_)
        --O-----
        --------
        --------
        -------O
        --------
        -----@--
        """
        can_coordinate = []
        obs_coordinate = []

        if self.inside_can:
            return None

        # top to bottom
        for i in range(self.board.height):
            check = [self.x, i]
            symbol = self.board.at(check[0], check[1])
            if symbol != [] and ((symbol[0].get_char() == 'O'
                                 or symbol[0].get_char() == 'C')):
                can_coordinate.append([check[0], check[1]])
            elif symbol:
                obs_coordinate.append([check[0], check[1]])

        # left to right
        for i in range(self.board.width):
            check = [i, self.y]
            symbol = self.board.at(check[0], check[1])
            if symbol != [] and ((symbol[0].get_char() == 'O'
                                 or symbol[0].get_char() == 'C')):
                can_coordinate.append([check[0], check[1]])
            elif symbol:
                obs_coordinate.append([check[0], check[1]])
        # now I have a list of all garbage cans available

        if len(can_coordinate) == 0:  # if no cans in LOS
            Raccoon.take_turn(self)
            return None

        # remove self from obs_coordinate
        self._helper_five(obs_coordinate)

        # check if garbage is obstructed and remove it if it is
        len1 = len(can_coordinate)
        len2 = len(obs_coordinate)
        i1 = 0
        i2 = 0
        while i1 < len1:
            for can in can_coordinate:
                self._helper_six([i2, len2], can_coordinate, obs_coordinate,
                                 can)
            i1 += 1
        # now I have a list of unobstructed cans
        # if all cans are obstructed
        if len(can_coordinate) == 0:
            Raccoon.take_turn(self)
            return None

        # reduce list to only the closest cans
        closest = []

        self._helper_two(can_coordinate, closest)

        # now closest should have list of only open closest cans
        # even if there is a tie, based on the order it will follow directions
        self._helper_one(closest)

        return None

    def _helper_one(self, closest: list) -> None:
        """A helper function for SmartRaccoon take_turn method with the
        parameter <closest>.
        >>> s = SmartRaccoon(GameBoard(8, 8), 3, 5)
        >>> c = [[2, 5]]
        >>> s._helper_one(c) is None
        True
        """
        for can in closest:
            if can[1] == self.y and can[0] < self.x:
                self.move(LEFT)
                return None
        for can in closest:
            if can[0] == self.x and can[1] < self.y:
                self.move(UP)
                return None
        for can in closest:
            if can[1] == self.y and can[0] > self.x:
                self.move(RIGHT)
                return None
        for can in closest:
            if can[0] == self.x and can[1] > self.y:
                self.move(DOWN)
                return None

        return None

    def _helper_two(self, can_coordinate: list,
                    closest: list) -> None:
        """A helper function for SmartRaccoon take_turn method with parameters
         <can_coordinate> and <closest>.
         >>> s = SmartRaccoon(GameBoard(8, 8), 3, 5)
         >>> can_co = [[1, 2]]
         >>> c = []
         >>> s._helper_two(can_co, c) is None
         True
         """
        first_can = can_coordinate[0]
        highest = abs((self.x + self.y) - (first_can[0] + first_can[1]))

        if len(can_coordinate) != 1:
            for can in can_coordinate[1:]:
                distance = abs((self.x + self.y) - (can[0] + can[1]))
                if distance <= highest:
                    highest = distance

        for can in can_coordinate:
            distance = abs((self.x + self.y) - (can[0] + can[1]))
            if distance == highest:
                closest.append(can)

    def _helper_three(self, can_coordinate: list, can: list, obs: list) -> None:
        """A helper function for SmartRaccoon take_turn method with parameters
         <can_coordinate>, <can>, and <obs>.
         >>> s = SmartRaccoon(GameBoard(8, 8), 3, 5)
         >>> can_co = [[7, 5], [3, 6], [2, 5], [6, 5]]
         >>> can_ = [7, 5]
         >>> obs_ = [4, 5]
         >>> s._helper_three(can_co, can_, obs_)
         >>> can_co
         [[3, 6], [2, 5], [6, 5]]
         """
        y = self.y
        x = self.x

        if (y == obs[1] == can[1]) and not (obs[0] < x < can[0])\
                and not (obs[0] > x > can[0]) \
                and (abs(x - obs[0]) < abs(x - can[0])):
            if can in can_coordinate:
                can_coordinate.remove(can)

    def _helper_four(self, can_coordinate: list, can: list, obs: list) -> None:
        """A helper function for SmartRaccoon take_turn method with parameters
         <can_coordinate>, <can>, and <obs>.
         >>> s = SmartRaccoon(GameBoard(8, 8), 3, 5)
         >>> can_co = [[3, 6], [2, 5], [7, 5], [6, 5]]
         >>> can_ = [3, 6]
         >>> obs_ = [3, 3]
         >>> s._helper_four(can_co, can_, obs_)
         >>> can_co
         [[3, 6], [2, 5], [7, 5], [6, 5]]
         """
        y = self.y
        x = self.x

        if (x == obs[0] == can[0]) and not (obs[1] < y < can[1])\
                and not (obs[1] > y > can[1]) \
                and (abs(y - obs[1]) < abs(y - can[1])):
            if can in can_coordinate:
                can_coordinate.remove(can)

    def _helper_five(self, obs_coordinate: list) -> None:
        """A helper function for SmartRaccoon take_turn method with the
        parameter <obs_coordinate>.
        >>> s = SmartRaccoon(GameBoard(8, 8), 3, 5)
        >>> o = []
        >>> s._helper_five(o) is None
        True
        """
        to_be_removed = []
        for obs in obs_coordinate:
            if obs == [self.x, self.y]:
                to_be_removed.append(obs)
        for item in to_be_removed:
            obs_coordinate.remove(item)

    def _helper_six(self, i2_len2: list, can_coordinate: list,
                    obs_coordinate: list, can: list) -> None:
        """A helper function for SmartRaccoon take_turn method with the
        parameters <i2_len2>, <can_coordinate>, <obs_coordinate>, and
        <can>.
        >>> s = SmartRaccoon(GameBoard(8, 8), 3, 5)
        >>> i_l = [1, 2]
        >>> can_co = []
        >>> obs_co = []
        >>> c = [2, 5]
        >>> s._helper_six(i_l, can_co, obs_co, c) is None
        True
        """
        i2 = i2_len2[0]
        len2 = i2_len2[1]
        while i2 < len2:
            for obs in obs_coordinate:
                # left or right
                self._helper_three(can_coordinate, can, obs)

                # top or bottom
                self._helper_four(can_coordinate, can, obs)
            i2 += 1

    def get_char(self) -> chr:
        """
        Return '@' to represent that this SmartRaccoon is inside a Garbage Can
        and 'S' otherwise.
        """
        if self.inside_can:
            return '@'
        return 'S'


class GarbageCan(Character):
    """A garbage can in the game.

    === Public Attributes ===
    locked:
        whether or not this GarbageCan is locked.

    === Sample Usage ===
    >>> b = GameBoard(2, 2)
    >>> g = GarbageCan(b, 0, 0, False)
    >>> g.x, g.y
    (0, 0)
    >>> g.locked
    False
    """
    locked: bool

    def __init__(self, b: GameBoard, x: int, y: int, locked: bool) -> None:
        """Initialize this GarbageCan to be at tile (<x>, <y>) and store
        whether it is locked or not based on <locked>.
        """

        self.locked = locked
        Character.__init__(self, b, x, y)

    def get_char(self) -> chr:
        """
        Return 'C' to represent a closed garbage can and 'O' to represent
        an open garbage can.
        """
        if self.locked:
            return 'C'
        return 'O'

    def move(self, direction: Tuple[int, int]) -> bool:
        """
        Garbage cans cannot move, so always return False.
        """
        return False


# A helper function you may find useful for Task #5, depending on how
# you implement it.
def get_neighbours(tile: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Return the coordinates of the four tiles adjacent to <tile>.

    This does NOT check if they are valid coordinates of a board.

    >>> ns = set(get_neighbours((2, 3)))
    >>> {(2, 2), (2, 4), (1, 3), (3, 3)} == ns
    True
    """
    rslt = []
    for direction in DIRECTIONS:
        rslt.append((tile[0] + direction[0], tile[1] + direction[1]))
    return rslt


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-io': [],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', '__future__', 'math'],
        'disable': ['E1136'],
        'max-attributes': 15,
        'max-module-lines': 1600
    })
