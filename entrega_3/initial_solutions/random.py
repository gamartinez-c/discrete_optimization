import random

from initial_solution import InitialSolution


class Random(InitialSolution):

    def solve(self):
        random.shuffle(self.locations_list)
        return self.locations_list
