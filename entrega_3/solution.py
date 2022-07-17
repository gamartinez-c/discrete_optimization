import random

from route import Route
from location import Location


class Solution:
    list_of_solutions = []

    def __init__(self):
        self.route = Route()
        Solution.list_of_solutions.append(self)

    def solve_initial_solution_for_route(self, approach_for_first_loc, greedy_approach):
        first_location = None
        if approach_for_first_loc == "origin":
            first_location = Location.get_nearest_location_to_origin()
        elif approach_for_first_loc == "random":
            first_location = random.choice([*Location.locations_list])
        else:
            print("The First Location:", approach_for_first_loc, "is not known")
            exit()

        heuristic = None
        if greedy_approach == "min_distance":
            heuristic = Location.get_locations_ordered_by_distance
        elif greedy_approach == "clockwise":
            heuristic = Location.get_locations_ordered_by_anti_clockwise
        else:
            print("The Greedy approach:", greedy_approach, "is not known")
            exit()

        location_list = heuristic(first_location)
        for location in location_list:
            self.route.add_location(location)

    def improve_solution_with_neighbour(self, location_to_improve):
        pass

    def get_obj_value(self):
        return self.route.get_total_distance_travel()

    def plot(self):
        self.route.plot_route()

    def get_output_format(self):
        solution_output = [Location.locations_list.index(location) for location in self.route.sequence_list]

        # calculate the length of the tour
        obj = self.get_obj_value()

        # prepare the solution in the specified output format
        output_data = '%.2f' % obj + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, solution_output))
        return output_data

    @staticmethod
    def get_best_solution():
        best_solution = Solution.list_of_solutions[0]
        best_obj = best_solution.get_obj_value()
        for solution in Solution.list_of_solutions[1:]:
            if solution.get_obj_value() < best_obj:
                best_solution = solution
                best_obj = solution.get_obj_value()
        return best_solution
