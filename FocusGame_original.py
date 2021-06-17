# Author: Timothy Jan
# Date: 11/26/2020
# Description: Focus/Domination board game! Two-player game to move and capture your opponent's pieces. The first
#              player to capture six of the opponent's pieces wins the game.


class Player:
    """Represents game players."""

    def __init__(self, player_tuple):
        self._player = {"name": player_tuple[0], "color": player_tuple[1]}
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

    def get_reserve(self):
        """Returns the bottommost piece in reserves."""
        return self._reserve[0]

    def get_len_reserve(self):
        """Returns the number of pieces in the player's reserve."""
        return len(self._reserve)

    def get_len_capture(self):
        """Returns the number of pieces in the player's capture."""
        return len(self._capture)

    def del_one_reserve(self):
        """Deletes the bottommost piece from reserves."""
        del self._reserve[0]


class Stack:
    """Represents stack of game pieces."""

    def __init__(self, piece):
        self._stack = [piece]  # initializes the stack to game setup's default piece

    def get_stack(self):
        """Returns stack *object*."""
        return self._stack

    def get_bottom_stack_piece(self):
        """Returns bottom piece *object* in stack."""
        return self._stack[0]

    def get_piece_at_index(self, index):
        """Returns piece in stack at index."""
        return self._stack[index]

    def get_slice_of_stack(self, index):
        """Returns pieces from index + 1 to end (top) of stack. Useful when player moves part of a stack."""
        if index == 1:
            return self._stack[0]
        return self._stack[index:]

    def get_stack_pieces(self):
        """Returns number of pieces in stack."""
        return len(self._stack)

    def get_stack_color(self):
        """Returns color based on the piece on the top of the stack."""
        if not self.get_stack():
            return ""
        return self._stack[-1].get_color()

    def get_stack_ownership(self):
        """Returns player name based on the piece on top of the stack."""
        return self._stack[-1].get_player()

    def add_to_stack(self, from_stack, number):
        """Copies a specified number of pieces from one stack to another."""
        self._stack.extend(from_stack.get_stack()[len(from_stack.get_stack()) - number:])

    def remove_from_stack(self, number):
        """Removes pieces(s) from top of stack."""
        for piece in range(number):
            del self._stack[-1]

    def transfer_stack(self, from_stack, number):
        """Transfers piece(s) from one stack to another."""
        for piece in range(number):
            self._stack.append(from_stack.get_bottom_stack_piece())
            del self._stack[0]


class Piece:
    """Represents game pieces."""

    def __init__(self, player_tuple):
        self._piece = {"name": player_tuple[0], "color": player_tuple[1]}

    def get_player(self):
        """Returns piece's player."""
        return self._piece["name"]

    def get_color(self):
        """Returns piece's color."""
        return self._piece["color"]


class FocusGame:
    """Represents the board game Focus/Domination."""

    def __init__(self, player_a, player_b):
        self._player_a = Player(player_a)
        self._player_b = Player(player_b)
        self._board = ((Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a))),  # row 1
                       (Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b))),  # row 2
                       (Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a))),  # row 3
                       (Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b))),  # row 4
                       (Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a))),  # row 5
                       (Stack(Piece(player_b)), Stack(Piece(player_b)), Stack(Piece(player_a)), Stack(Piece(player_a)), Stack(Piece(player_b)), Stack(Piece(player_b))),  # row 6
                       )
        self._turn_counter = 1
        self._first_player = None
        self._second_player = None
        self._current_turn = None
        self._message = None

    def pre_move_check(self, player, start, end, number):
        """Performs pre-move checks."""
        # check if a player exists
        if player != self._player_a.get_player_name() and player != self._player_b.get_player_name():
            self._message = False
            return self._message

        # check if it's the first turn
        if self._turn_counter == 1:
            self.setup_first_turn_players(player)

        # check if it's the player's turn
        if player != self._current_turn.get_player_name():
            self._message = False
            return self._message

        # check valid move locations
        if start[0] < 0 or start[0] > 5:
            self._message = False
            return self._message
        elif start[1] < 0 or start[1] > 5:
            self._message = False
            return self._message
        elif end[0] < 0 or end[0] > 5:
            self._message = False
            return self._message
        elif end[1] < 0 or end[1] > 5:
            self._message = False
            return self._message

        # check diagonal move
        if end[0] - start[0] != 0 and end[1] - start[1] != 0:
            self._message = False
            return self._message

        # starting and ending location are the same
        elif start[0] == end[0] and start[1] == end[1]:
            self._message = False
            return self._message

        # stack exists in starting location
        elif self._board[start[0]][start[1]].get_stack_pieces == 0:
            self._message = False
            return self._message

        # enough pieces exist in the stack for the player to move
        elif number > self._board[start[0]][start[1]].get_stack_pieces():
            self._message = False
            return self._message

        # player is trying to move the wrong number of spaces (e.g. if moving 3 pieces, must move 3 spaces)
        elif end[0] - start[0] != number and end[1] - start[1] != number:
            self._message = False
            return self._message

        # player is attempting to move a stack that doesn't belong to them
        elif self._board[start[0]][start[1]].get_stack_ownership() != self._current_turn.get_player_name():
            self._message = False
            return self._message

        else:
            self._message = "successfully moved"

        return self._message

    def assign_pieces(self, start, end, number):
        """Moves pieces from one stack to another."""

        # add pieces to destination
        self._board[end[0]][end[1]].add_to_stack(self._board[start[0]][start[1]], number)

        # remove pieces from start location
        self._board[start[0]][start[1]].remove_from_stack(number)

        return

    def reserve_capture(self, location):
        """Checks end space after a move to determine whether to capture or reserve any pieces."""
        if self._board[location[0]][location[1]].get_stack_pieces() < 5:
            return
        else:
            for piece in range(self._board[location[0]][location[1]].get_stack_pieces() - 5):
                # if the piece belongs to the current player
                if self._current_turn.get_player_name() == self._board[location[0]][location[1]].get_bottom_stack_piece().get_player():
                    # add to player reserve
                    self._current_turn.add_reserve(self._board[location[0]][location[1]].get_bottom_stack_piece())
                    # remove from stack
                    self._board[location[0]][location[1]].remove_from_stack(1)
                # otherwise, the piece belongs to the other player
                else:
                    # add to player capture
                    self._current_turn.add_capture(self._board[location[0]][location[1]].get_bottom_stack_piece())
                    # remove from stack
                    self._board[location[0]][location[1]].remove_from_stack(1)
            # check win condition
            if self._current_turn.get_len_capture() > 5:
                self._message = self._current_turn.get_player_name() + " Wins"
                return self._message
            else:
                self._message = "successfully moved"
                return

    def move_piece(self, player, start, end, number):  # string, tuple, tuple, integer
        """Allows players to move game stacks."""
        # pre move checks
        self.pre_move_check(player, start, end, number)

        # return invalid move message and exit
        if self._message != "successfully moved":
            return self._message

        # move pieces
        self.assign_pieces(start, end, number)

        # check reserve, capture, win condition
        self.reserve_capture(end)

        # update turn
        self.update_turn()

        # return final message
        return self._message

    def reserved_move(self, player, location):
        """Allows player to place a piece from their reserve on a given location."""
        # check to see if the player has reserves
        if player == self._player_a.get_player_name():
            if self._player_a.get_len_reserve() < 1:
                return "No pieces in reserve"
        if player == self._player_b.get_player_name():
            if self._player_b.get_len_reserve() < 1:
                return "No pieces in reserve"

        # check that it's the player's turn
        if player != self._current_turn.get_player_name():
            return False

        # check to see if the player is putting the piece on the board
        if location[0] < 0 or location[0] > 5:
            self._message = False
            return self._message
        if location[1] < 0 or location[1] > 5:
            self._message = False
            return self._message

        # add the piece to that space on TOP
        self._board[location[0]][location[1]].get_stack().append(self._current_turn.get_reserve())

        # take the piece away from reserves
        self._current_turn.del_one_reserve()

        # check for reserve or capture
        self.reserve_capture(location)

        # update turn
        self.update_turn()

        # return final message
        return self._message

    def get_first_player(self):
        """Returns first player."""
        return self._first_player

    def get_second_player(self):
        """Returns second player."""
        return self._second_player

    def get_stack_on_board(self, location_tuple):
        """Returns stack object at location_tuple."""
        return self._board[location_tuple[0]][location_tuple[1]]

    def setup_first_turn_players(self, player):
        """Sets up game players."""
        # first player is player A
        if player == self._player_a.get_player_name():
            self._first_player = self._player_a
            self._current_turn = self._player_a
            self._second_player = self._player_b
            return
        # first player is player B
        else:
            self._first_player = self._player_b
            self._current_turn = self._player_b
            self._second_player = self._player_a
            return

    def update_turn(self):
        """Updates turn counter by incrementing turn counter and flipping current turn to the other player's name."""
        self._turn_counter += 1
        if self._turn_counter % 2 == 0:
            self._current_turn = self.get_second_player()
            return
        else:
            self._current_turn = self.get_first_player()
            return

    def show_pieces(self, location):
        """Shows a list of the pieces that are present at a given location from bottom (left) to top (right)."""
        temp_list = []
        for pieces in range(len(self._board[location[0]][location[1]].get_stack())):
            temp_list.append(self._board[location[0]][location[1]].get_piece_at_index(pieces).get_color())
        return temp_list

    def show_reserve(self, player):
        """Returns the number of pieces in a player's reserve."""
        if player == self._player_a.get_player_name():
            return self._player_a.get_len_reserve()
        if player == self._player_b.get_player_name():
            return self._player_b.get_len_reserve()

    def show_captured(self, player):
        """Returns the number of pieces captured by a player."""
        if player == self._player_a.get_player_name():
            return self._player_a.get_len_capture()
        if player == self._player_b.get_player_name():
            return self._player_b.get_len_capture()

    def print_board(self):
        """Prints game board [top piece (stack) ownership][size of stack in space]."""
        for row in self._board:
            print()
            for index in row:
                print("[" + Stack.get_stack_color(index), str(Stack.get_stack_pieces(index)) + "]", end=" ")


# tests
# game = FocusGame(('PlayerA', 'R'), ('PlayerB', 'G'))
# game.print_board()
# print()
# print(game.move_piece("bob", (0, 0), (0, 1), 1))  # player doesn't exist
# print(game.move_piece("PlayerA", (0, 0), (0, 1), 1))  # valid move
# game.print_board()
# print()
# print(game.move_piece("PlayerA", (0, 2), (0, 1), 1))  # not your turn
# print(game.move_piece("PlayerB", (0, 10), (0, 1), 1))  # off the board
# print(game.move_piece("PlayerB", (0, 1), (0, 2), 18))  # too many pieces
# print(game.move_piece("PlayerB", (0, 1), (0, 1), 1))  # start and end in same location
# print(game.move_piece("PlayerB", (0, 1), (0, 5), 1))  # trying to move too far
# print(game.move_piece("PlayerB", (1, 0), (1, 1), 1))  # valid move
# game.print_board()
# print()
# print(game.move_piece("PlayerA", (1, 1), (0, 1), 1))  # move another player's stack
# game.print_board()
# print()
# print(game.move_piece("PlayerA", (0, 1), (0, 2), 2))  # valid move
# game.print_board()
# print()
# print(game.move_piece("PlayerB", (1, 1), (1, 2), 2))  # valid move
# game.print_board()
# print()
# print(game.move_piece("PlayerA", (0, 2), (0, 3), 3))  # valid move
# game.print_board()
# print()
# print(game.move_piece("PlayerB", (1, 2), (1, 3), 3))  # valid move
# game.print_board()
# print()
# print(game.move_piece("PlayerA", (0, 3), (0, 4), 4))  # valid move
# game.print_board()
# print()
# print(game.move_piece("PlayerB", (1, 3), (1, 4), 4))  # valid move
# game.print_board()
# print()
# print(game.move_piece("PlayerA", (0, 4), (0, 5), 5))  # valid move
# game.print_board()
# print()
# print(game.move_piece("PlayerB", (1, 4), (1, 5), 5))  # valid move
# game.print_board()
# print()
# print(game.reserve_move("PlayerA", (0, 5)))
# print(game.move_piece("PlayerB", (1, 5), (0, 5), 5))
# game.print_board()
# print()
# print(game.move_piece("PlayerA", (2, 0), (3, 0), 1))
# game.print_board()
# print()
# # print(game.move_piece("PlayerB", (0, 5), (1, 5), 3))
# # game.print_board()
# # print()
#
#
# # print()
# # print(game.move_piece("PlayerB", (1, 0), (0, 0), 1))
# # game.print_board()
# # print()
# # print(game.move_piece("PlayerA", (0, 1), (1, 1), 2))
# # game.print_board()
# # print()

# def main():
#     game = FocusGame(('PlayerA', 'R'), ('PlayerB', 'G'))
#     game.move_piece('PlayerA', (0, 0), (0, 1), 1)  # Returns message "successfully moved"
#     game.show_pieces((0, 1))  # Returns ['R','R']
#     game.show_captured('PlayerA')  # Returns 0
#     game.reserved_move('PlayerA', (0, 0))  # Returns message "No pieces in reserve"
#     game.show_reserve('PlayerA')  # Returns 0
#
#
# if __name__ == '__main__':
#     main()
