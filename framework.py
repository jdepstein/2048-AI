from time import sleep, time


# Superclass for puzzles
class Puzzle(object):

    # Return whether this puzzle is equivalent to the other
    def __eq__(self, other):
        raise NotImplementedError

    # Return a hash code for this puzzle
    def __hash__(self):
        raise NotImplementedError

    # Return whether this puzzle comes before the other in a sort
    def __lt__(self, other):
        raise NotImplementedError

    # Return whether this puzzle is solved
    def solved(self):
        raise NotImplementedError

    # Return an estimate of how far this puzzle is from being solved
    def heuristic(self):
        raise NotImplementedError

    # Return a list of legal moves
    def moves(self):
        raise NotImplementedError

    # Return a new puzzle created by a move
    def neighbor(self, move):
        raise NotImplementedError

    # Print this puzzle to the console
    def display(self):
        raise NotImplementedError


# Superclass for a puzzle solver
class Agent(object):

    # Return the move this agent wants to make
    def move(self, puzzle):
        raise NotImplementedError

    # Watch this agent solve a puzzle
    def solve(self, puzzle, interval=0.25):
        print("Solving puzzle:")
        puzzle.display()
        moves = 0

        while not puzzle.solved():

            start = time()
            move = self.move(puzzle)
            seconds = time() - start

            print("After", seconds, "seconds:")
            puzzle = puzzle.neighbor(move)
            puzzle.display()
            moves += 1

            sleep(interval)

        print(moves, "moves where used to either make the puzzle Stuck or Solved")

