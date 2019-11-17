from solving.utils.framework import Puzzle
from copy import deepcopy
import random
Board = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    ]
Size = 4


class TwentyFortyEight(Puzzle):

    def __init__(self, board=Board, largest=2, second_largest=2):
        self.largest = largest
        self.board = board
        self.second_largest = second_largest

    # Return whether this puzzle is equivalent to the other
    def __eq__(self, other):
        return self.board == other.board

    # Return a hash code for this puzzle
    def __hash__(self):
        return hash(str(self.board))

    # Return whether this puzzle comes before the other in a sort
    def __lt__(self, other):
        return self.largest > other.largest

    # Returns the puzzle heuristic
    def heuristic(self):
        four = 0
        eight = 0
        sixteen = 0
        thirtytwo = 0
        sixtyfour = 0
        onetwentyeight = 0
        twofiftysix = 0
        fivetweleve = 0
        tentwentyfour = 0
        twentyfortyeight = 0
        sum_heur = 0

        for x in range(Size):
            for y in range(Size):
                if self.board[x][y] == 4:           # counts the number of each value in the board and then each count
                    four += 1                       # has a different multiplier the higher the tile value the bigger
                if self.board[x][y] == 8:           # the multiplier
                    eight += 1
                if self.board[x][y] == 16:
                    sixteen += 1
                if self.board[x][y] == 32:
                    thirtytwo += 1
                if self.board[x][y] == 64:
                    sixtyfour += 1
                if self.board[x][y] == 128:
                    onetwentyeight += 1
                if self.board[x][y] == 256:
                    twofiftysix += 1
                if self.board[x][y] == 512:
                    fivetweleve += 1
                if self.board[x][y] == 1024:
                    tentwentyfour += 1
                if self.board[x][y] == 2048:
                    twentyfortyeight += 1

        sum_heur += 1 * four
        sum_heur += 4 * eight
        sum_heur += 16 * sixteen
        sum_heur += 64 * thirtytwo
        sum_heur += 256 * sixtyfour
        sum_heur += 1024 * onetwentyeight
        sum_heur += 4096 * twofiftysix
        sum_heur += 16384 * fivetweleve
        sum_heur += 65536 * tentwentyfour
        sum_heur += 10000000000000 * twentyfortyeight
        return sum_heur

    # returns the the count of all possible moves multiplied by the heuristic value of the board
    # if stuck should return zero
    def heuristic_stuck(self):
        count = 0   # total moves overall
        count2 = 0  # total moves combinations
        for x in range(Size):  # if there is a zero then there is a move count = count + 1
            for y in range(Size):
                if self.board[x][y] == 0:
                    count += 1

        for x in range(Size):  # all possible combinations if and see how many can happen move count = count + 1
            for y in range(Size):
                if x == 0:
                    if self.board[x][y] == self.board[x + 1][y]:
                        count2 += 1
                if y == 0:
                    if self.board[x][y] == self.board[x][y + 1]:
                        count2 += 1
                if x == Size - 1:
                    if self.board[x][y] == self.board[x - 1][y]:
                        count += 1
                if y == Size - 1:
                    if self.board[x][y] == self.board[x][y - 1]:
                        count2 += 1
                if 1 < x < Size - 2:
                    if self.board[x][y] == self.board[x - 1][y] or self.board[x][y] == self.board[x + 1][y]:
                        count2 += 1
                if 1 < y < Size - 2:
                    if self.board[x][y] == self.board[x][y - 1] or self.board[x][y] == self.board[x][y + 1]:
                        count2 += 1

        if self.solved() and not self.stuck():     # if the puzzle becomes solved set the count really high
            count = 10000000

        count = count + count2/2    # divided combinations by 2 to account for double counting

        return count * self.heuristic()

    # Return whether this puzzle is solved
    def solved(self):
        if self.largest == 2048:
            # print("The Puzzle was Solved in ")
            return True
        if self.stuck():    # will say the puzzle was Solved even if stuck so it breaks out of the program
            # print("The Puzzle became Stuck in ")
            return True
        else:
            return False

    # Return a list of legal moves
    def moves(self):
        move = list()       # add all possible moves to the list only 5
        move.append("up")
        move.append("down")
        move.append("right")
        move.append("left")
        move.append("Start")
        return move

    def neighbor(self, move):

        board_copy = deepcopy(self.board)       # set a deep copy of the board for all the methods
        largest = self.largest                  # record the current Largest and second largest
        largest_2 = 0

        if move == "up":
            board_copy = self.combined_shift(move, board_copy, 1, 0, 0)        # run the two shift methods with the
            board_copy = self.shift(move, board_copy, 1, 0, 0)                 # correct move given and set copy

        if move == "down":
            board_copy = self.combined_shift(move, board_copy, -1, 0, Size - 1)
            board_copy = self.shift(move, board_copy, -1, 0, Size - 1)

        if move == "left":
            board_copy = self.combined_shift(move, board_copy, 0, 1, 0)
            board_copy = self.shift(move, board_copy, 0, 1, 0)

        if move == "right":
            board_copy = self.combined_shift(move, board_copy, 0, -1, Size - 1)
            board_copy = self.shift(move, board_copy, 0, -1, Size - 1)

        board_copy = self.spawn(move, board_copy)    # spawn values and set the copy

        for x in range(Size):                     # find the new largest and second largest values
            for y in range(Size):
                if board_copy[x][y] > largest:
                    largest = board_copy[x][y]
        count = 0
        for x in range(Size):
            for y in range(Size):

                if board_copy[x][y] == largest:
                    count += 1

                elif board_copy[x][y] > largest_2:
                    largest_2 = board_copy[x][y]

                if board_copy[x][y] == largest and count == 2:
                    largest_2 = largest
                    break

        return TwentyFortyEight(board_copy, largest, largest_2)       # return the new board with largest and 2nd

    # Print this puzzle to the console
    def display(self):
        for row in self.board:
            print("{: >20} {: >20} {: >20} {: >20}".format(*row))

    # stuck: tells the player if there are no more moves left to be made in the game
    # returns: Boolean value true if stuck false all other cases
    def stuck(self):
        for x in range(Size):           # if there is a zero then there is a move returns false
            for y in range(Size):
                if self.board[x][y] == 0:
                    return False

        for x in range(Size):          # all possible combinations if ant can happen returns false
            for y in range(Size):
                if x == 0:
                    if self.board[x][y] == self.board[x + 1][y]:
                        return False
                if y == 0:
                    if self.board[x][y] == self.board[x][y + 1]:
                        return False
                if x == Size - 1:
                    if self.board[x][y] == self.board[x - 1][y]:
                            return False
                if y == Size - 1:
                    if self.board[x][y] == self.board[x][y - 1]:
                            return False
                if 0 < x < Size - 1:
                    if self.board[x][y] == self.board[x - 1][y] or self.board[x][y] == self.board[x + 1][y]:
                            return False
                if 0 < y < Size - 1:
                    if self.board[x][y] == self.board[x][y - 1] or self.board[x][y] == self.board[x][y + 1]:
                        return False

        return True

    # combined_shift: makes sure when a move is made it combined all the correct pieces in the right way
    # move: the move given to match with the shift
    # board: the current board being looked at
    # x1: up and down move multiplier
    # y1: right and left move multiplier
    # w: flips the board so you can start at the bottom corner if "down or right"
    # return: the board after all combinations
    def combined_shift(self, move, board, x1, y1, w):
        count = 0
        for x in range(Size):
            if move == "right" or move == "left":
                count = 0                           # counter used when zero pairs combined to make sure no other
            for y in range(Size):                   # moves can happen after that
                if move == "up" or move == "down":
                    count = 0
                if (y == 0 and (move == "left" or move == "right")) or (x == 0 and (move == "up" or move == "down")):

                    # Start and Middle Pair w/ zero in the Middle (use absolute value so you are in the correct spot)
                    if board[abs(w - x)][abs(w - y)] == board[abs(w - x) + (2 * x1)][abs(w - y) + (2 * y1)] and\
                                    board[abs(w - x) + (1 * x1)][abs(w - y) + (1 * y1)] == 0\
                                    and board[abs(w - x)][abs(w - y)] != 0 and board[abs(w - x)][abs(w - y)] != -1:

                        board[abs(w - x)][abs(w - y)] = board[abs(w - x)][abs(w - y)] * 2
                        board[abs(w - x) + (2 * x1)][abs(w - y) + (2 * y1)] = -1
                        board[abs(w - x) + (1 * x1)][abs(w - y) + (1 * y1)] = -1
                        count += 1

                    # Start and End Pair w/ 2 zero's between them
                    elif board[abs(w - x)][abs(w - y)] == board[abs(w - x) + (3 * x1)][abs(w - y) + (3 * y1)] and\
                                    board[abs(w - x) + x1][abs(w - y) + y1] == 0 and\
                                    board[abs(w - x) + (2 * x1)][abs(w - y) + (2 * y1)] == 0 and\
                                    board[abs(w - x)][abs(w - y)] != 0 and board[abs(w - x)][abs(w - y)] != -1:

                        board[abs(w - x)][abs(w - y)] = board[abs(w - x)][abs(w - y)] * 2
                        board[abs(w - x) + (3 * x1)][abs(w - y) + (3 * y1)] = - 1
                        board[abs(w - x) + x1][abs(w - y) + y1] = -1
                        board[abs(w - x) + (2 * x1)][abs(w - y) + (2 * y1)] = - 1
                        count += 1

                # All pairs that are next to each other as long as a move hasn't been made yet
                if ((move == "left" or move == "right") and count == 0 and y != Size - 1) or\
                        ((move == "up" or move == "down")and count == 0 and x != Size - 1):

                    if board[abs(w - x)][abs(w - y)] == board[abs(w - x) + x1][abs(w - y) + y1] and \
                            board[abs(w - x)][abs(w - y)] != 0 and board[abs(w - x)][abs(w - y)] != -1:

                        board[abs(w - x)][abs(w - y)] = board[abs(w - x)][abs(w - y)] * 2
                        board[abs(w - x) + x1][abs(w - y) + y1] = -1

                # Second tile and third Tile pair with a zero in between
                elif ((move == "left" or move == "right") and count == 0 and y == 1) or\
                        ((move == "up" or move == "down") and count == 0 and x == 1):

                    if board[abs(w - x)][abs(w - y)] == board[abs(w - x) + (2 * x1)][abs(w - y) + (2 * y1)] and\
                         board[abs(w - x) + x1][abs(w - y) + y1] == 0 and\
                         board[abs(w - x)][abs(w - y)] != 0 and board[abs(w - x)][abs(w - y)] != -1:

                        board[abs(w - x)][abs(w - y)] = board[abs(w - x)][abs(w - y)] * 2
                        board[abs(w - x) + (2 * x1)][abs(w - y) + (2 * y1)] = - 1

        return board

    # Shift: Moves all tiles to their correct spots after they have been incremented correctly
    # move: The move the player made for the shift
    # board: The state of the board before the shift occurs
    # x1: multiplier for the up and down moves
    # y1: multiplier for left and right moves
    # w: used to flip the board start spot when reading in nested for loops
    # return: the board after all shifts
    def shift(self, move, board, x1, y1, w):

        for x in range(Size):               # Look for negative placeholders and remove them with 0's
            for y in range(Size):
                if board[x][y] <= -1:
                    board[x][y] = 0

        for t in range(Size - 1):          # shift evey tile over in the correct direction by 3 if 0's are in it's path
            for x in range(Size):
                for y in range(Size):
                    if ((move == "left" or move == "right") and y != Size - 1) or\
                            ((move == "up" or move == "down") and x != Size - 1):

                        if board[abs(w - x)][abs(w - y)] == 0:
                            board[abs(w - x)][abs(w - y)] = board[abs(w - x) + x1][abs(w - y) + y1]
                            board[abs(w - x) + x1][abs(w - y) + y1] = 0
        return board

    # This is A spawn method that is used after every move or the Start
    # move: the move the was used to check if it was a valid move and if its start " for the human player option"
    # board: the current board that the move was just done on
    # returns the board after the spawns have been made
    def spawn(self, move, board):
        open_spots = []                         # List of open spots for a spawn
        count = 0
        for x in range(Size):             # Check for zeros which are open spawn locations keep a count
            for y in range(Size):
                if board[x][y] == 0:
                    open_spots.append((x, y))
                    count += 1

        if move != "Start" and count != 0 and not move not in self.moves():
            location = random.randrange(count)
            prob = random.uniform(0, 1)                   # if a valid move and not start it spawns a 2 or a 10% of a 4
            (x, y) = open_spots[location]                       # at a random location that is open on the board

            if prob < .1:
                board[x][y] = 4
            else:
                board[x][y] = 2

        if move == "Start":
            location = random.randrange(count)          # if it is the start of the game spawn 2 twos randomly on the
            location2 = random.randrange(count)         # board only twos this time

            while location == location2:
                location2 = random.randrange(count)

            (x, y) = open_spots[location]
            board[x][y] = 2
            (x, y) = open_spots[location2]
            board[x][y] = 2

        return board
