# Author: Timothy Jan
# Last Modified: 06/17/2021
# Description: Focus/Domination board game: two-player game where the objective is to capture opposing player's pieces.
#              The first player to capture six of the opponent's pieces wins the game.


class Player:
    """Represents game players."""

    def __init__(self, player):
        self._player = {"name": player[0], "color": player[1]}
        self._reserve = []
        self._capture = []

    def get_player_name(self):
        """Returns player name."""
        return self._player["name"]

    def get_player_color(self):
        """Returns player color."""
        return self._player["color"]

    def add_reserve(self, piece):
        """Adds piece to player's reserve."""
        self._reserve.append(piece)

    def add_capture(self, piece):
        """Adds piece to player's capture."""
        self._capture.append(piece)

    def get_len_reserve(self):
        """Returns number of pieces in player's reserve."""
        return len(self._reserve)

    def get_len_capture(self):
        """Returns number of pieces in player's capture."""
        return len(self._capture)


class Piece:
    """Represents game pieces."""

    def __init__(self, player):
        self._piece = {"name": player[0], "color": player[1]}

    def get_player(self):
        """Returns piece's player name."""
        return self._piece["name"]

    def get_color(self):
        """Returns piece's player color."""
        return self._piece["color"]


class Stack:
    """Represents stack of game pieces."""

    def __init__(self, piece):
        self._stack = [piece]

    def get_stack(self):
        """Returns stack."""
        return self._stack

    def get_bottom_piece(self):
        """Returns bottom piece."""
        return self._stack[0]

    def get_slice(self, num):
        """Returns a number of pieces from the top of the stack down."""
        return self._stack[-num:]

    def del_slice(self, num):
        """Deletes a number of pieces off the top of the stack."""
        del self._stack[-num:]

    def add_slice(self, pieces):
        """Adds pieces to the top of the stack."""
        self._stack += pieces

    def get_len_stack(self):
        """Returns number of pieces in the stack."""
        return len(self._stack)

    def get_stack_color(self):
        """Returns color based on the piece on top of the stack."""
        if not self.get_stack():
            return ""
        return self._stack[-1].get_color()

    def get_stack_name(self):
        """Returns name based on the piece on top of the stack."""
        if not self.get_stack():
            return ""
        return self._stack[-1].get_name()


class FocusGame:
    """Represents the board game Focus/Domination"""

    def __init__(self, player_a, player_b):
        self._player_a = Player(player_a)
        self._player_b = Player(player_b)
        self._board = [[Stack(None), Stack(None), Stack(None), Stack(None)],  # row 1 (4)
                       [Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a))],  # row 2 (6)
                       [Stack(None), Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(None)],  # row 3 (8)
                       [Stack(None), Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(None)],  # row 4 (8)
                       [Stack(None), Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(None)],  # row 5 (8)
                       [Stack(None), Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(None)],  # row 6 (8)
                       [Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b))],  # row 7 (6)
                       [Stack(None), Stack(None), Stack(None), Stack(None)]  # row 8 (4)
                       ]
