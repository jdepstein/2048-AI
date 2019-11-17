from solving.utils.framework import Agent
import random


class MonteCarlo(Agent):

    def move(self, puzzle):

        if puzzle.largest != 1024 or puzzle.second_largest < 64:
            sumr = self.run_tests(puzzle, "right", 100, 5)      # have range to use regular tests
            suml = self.run_tests(puzzle, "left", 100, 5)       # run each 100 test with a cut_off of 5 moves ahead
            sumu = self.run_tests(puzzle, "up", 100, 5)
            sumd = self.run_tests(puzzle, "down", 100, 5)

            avr = sumr / 100        # Average each returned heuristic
            avl = suml / 100
            avu = sumu / 100
            avd = sumd / 100

            return self.largest(avr, avl, avu, avd)     # return the best heuristic move

        elif puzzle.second_largest < 256:
            (xr, yr) = self.till_stuck(puzzle, "right", 50, 25)         # use till stuck cut off but now set
            (xl, yl) = self.till_stuck(puzzle, "left", 50, 25)          # 50 test but 25 moves ahead
            (xu, yu) = self.till_stuck(puzzle, "up", 50, 25)
            (xd, yd) = self.till_stuck(puzzle, "down", 50, 25)

            avr = xr / 50
            avl = xl / 50               # average the best heuristic and get the best move from that
            avu = xu / 50
            avd = xd / 50

            choice_huer = self.largest(avr, avl, avu, avd)

            avr = yr / 50
            avl = yl / 50       # average the moves till
            avu = yu / 50
            avd = yd / 50

            if avr == avl == avu == avd:       # if they are all equal there is no best option so use the heuristic move
                return choice_huer
            else:                                           # returns the one that gets stuck after
                return self.largest(avr, avl, avu, avd)     # the most moves possible

        else:   # all other options

            (xr, yr) = self.till_stuck(puzzle, "right", 50, 50)         # 50 tests with depth of 50 now was to mostly
            (xl, yl) = self.till_stuck(puzzle, "left", 50, 50)          # get stuck or solved after 50 moves
            (xu, yu) = self.till_stuck(puzzle, "up", 50, 50)
            (xd, yd) = self.till_stuck(puzzle, "down", 50, 50)

            avr = xr / 50               # same process as above
            avl = xl / 50
            avu = xu / 50
            avd = xd / 50

            choice_huer = self.largest(avr, avl, avu, avd)

            avr = yr / 50
            avl = yl / 50
            avu = yu / 50
            avd = yd / 50

            if avr == avl == avu == avd:
                return choice_huer
            else:
                return self.largest(avr, avl, avu, avd)

    # run_test: runs however many tests need returns the sum of the heuristics  of each tet
    # puzzle: the puzzle that the test is being done on
    # move: The first move to be made every test
    # test_count: The number of test that are being done
    # cut_off: The number of moves that is looked ahead
    # return: the heuristic sum
    def run_tests(self, puzzle, move, test_count, cut_off):
        sum_heur = 0                   # the heuristic total of boards

        for x in range(test_count):
            puzzle_test = puzzle
            puzzle_test = puzzle_test.neighbor(move)
            w = 0
            while w < cut_off:
                puzzler = puzzle_test                       # must make these copies so you don't change the the puzzle
                puzzlel = puzzle_test                       # each move has their own unique puzzle not effect by each
                puzzleu = puzzle_test                       # other moves
                puzzled = puzzle_test
                prr = puzzler.neighbor("right").heuristic()      # checks all heuristics then uses largest to get the
                prl = puzzlel.neighbor("left").heuristic()       # best move from that
                pru = puzzleu.neighbor("up").heuristic()
                prd = puzzled.neighbor("down").heuristic()

                choice = self.largest(prr, prl, pru, prd)
                puzzle_test = puzzle_test.neighbor(choice)
                sum_heur += puzzle_test.heuristic()
                w += 1

        return sum_heur

    # till_stuck: Similar to run but has some key differences in what is compared and what is returned
    # puzzle: the current puzzle being looked at
    # move: the initial move that was made
    # test_count: the number of test being done to solve the puzzle
    # cut_off: How many moves ahead to look
    # return: the tuple of moves till stuck and the heuristic sum
    def till_stuck(self, puzzle, move, test_count, cut_off):
        sum_heur = 0
        move_till_stuck = 0

        for x in range(test_count):
            puzzle_test = puzzle
            puzzle_test = puzzle_test.neighbor(move)
            w = 1
            while w < cut_off + 1:
                puzzler = puzzle_test
                puzzlel = puzzle_test
                puzzleu = puzzle_test
                puzzled = puzzle_test

                prr = puzzler.neighbor("right").heuristic_stuck()  # checks all heuristics2 then uses largest to get the
                prl = puzzlel.neighbor("left").heuristic_stuck()   # best move from that
                pru = puzzleu.neighbor("up").heuristic_stuck()
                prd = puzzled.neighbor("down").heuristic_stuck()

                choice = self.largest(prr, prl, pru, prd)

                puzzle_test = puzzle_test.neighbor(choice)

                if puzzle_test.stuck():         # if the board becomes stuck increment the w add w to move_till_stuck
                    move_till_stuck += w + 1    # break out of while loop by setting w to max
                    w = cut_off

                if puzzle_test.solved() and not puzzle_test.stuck:  # break if the puzzle is solved and set\increment
                    move_till_stuck = cut_off                       # important values
                    w = cut_off
                    sum_heur += puzzle_test.heuristic_stuck()

                sum_heur += puzzle_test.heuristic_stuck()
                w += 1

        return sum_heur, move_till_stuck

    # avr: Average right value
    # avl: Average left value
    # avu: Average up value
    # avd: Average down value
    # return: the largest value of the four as a string if ties random out of the tie
    def largest(self, avr, avl, avu, avd):
        choice = []

        if avr >= avl and avr >= avu and avr >= avd:
            choice.append("right")

        if avl >= avr and avl >= avu and avl >= avd:
            choice.append("left")

        if avu >= avr and avu >= avl and avu >= avd:
            choice.append("up")

        if avd >= avr and avd >= avl and avd >= avu:
            choice.append("down")

        return random.choice(choice)
