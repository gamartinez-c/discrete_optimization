import random
import logging
from multiprocessing import Pool

from improvements.neighbours import Neighbours
from improvements.simulated_annealing import SimulatedAnnealing
from initial_solutions import *

from route import Route
from location import Location


class Solution:
    list_of_solutions = []

    def __init__(self, list_of_locations):
        self.list_of_locations = list_of_locations
        self.route = Route(self.list_of_locations)
        Solution.list_of_solutions.append(self)

        self.initial_node = None
        self.greedy_constructive = None
        self.neighbour_iterations = {}

        self.value_without_neighbours = None

    def solve_initial_solution_for_route(self, approach_for_first_loc, greedy_approach):
        first_location = None
        self.initial_node = approach_for_first_loc
        self.greedy_constructive = greedy_approach
        if approach_for_first_loc == "origin":
            first_location = Location.get_nearest_location_to_location(self.list_of_locations)
        elif approach_for_first_loc == "random":
            first_location = random.choice([*self.list_of_locations])
        else:
            print("The First Location:", approach_for_first_loc, "is not known")
            exit()

        location_list = self.list_of_locations.copy()
        heuristic = None
        if greedy_approach == "min_distance":
            heuristic = Greedy(location_list, first_location)
        elif greedy_approach == "clockwise":
            heuristic = Clock(location_list, first_location)
        elif greedy_approach == 'mst':
            heuristic = MST(location_list, first_location)
        elif greedy_approach == 'cluster_1' or greedy_approach == 'cluster_2':
            if greedy_approach == 'cluster_1':
                type_of_assignation = 1
            else:
                type_of_assignation = 2
            heuristic = Cluster(location_list, first_location, type_of_assignation)
        else:
            print("The Greedy approach:", greedy_approach, "is not known")
            exit()

        location_list = heuristic.solve()
        for location in location_list:
            self.route.add_location(location)

        self.value_without_neighbours = self.get_obj_value()

    def improve_solution(self, approach, plot=False):
        if approach == 'simple':
            neighbour = Neighbours(self.route)
            self.neighbour_iterations = neighbour.improve_by_2_opt()
        elif approach == 'simulated_annealing':
            amount_of_nodes = len(self.route)
            if amount_of_nodes < 100:
                init_temp, cooldown_rate, max_iterations = 25, 0.99998, 400000
            elif amount_of_nodes < 200:
                init_temp, cooldown_rate, max_iterations = 200, 0.99998, 400000
            elif amount_of_nodes < 500:
                init_temp, cooldown_rate, max_iterations = 200, 0.99998, 500000
            elif amount_of_nodes < 1000:
                init_temp, cooldown_rate, max_iterations = 50, 0.999985, 700000
            elif amount_of_nodes < 2000:
                init_temp, cooldown_rate, max_iterations = 25, 0.99999, 1500000
            else:
                init_temp, cooldown_rate, max_iterations = 25, 0.99999, 1500000
            neighbour = SimulatedAnnealing(self.route, 'swap', init_temp, cooldown_rate, max_iterations)
            self.neighbour_iterations = neighbour.improve(True if len(self.route) < 333000 else False)
        else:
            neighbour = Neighbours(self.route)
            self.neighbour_iterations = neighbour.best_improvement()
        self.route = neighbour.route.copy()
        self.print_solution_path()

    def get_obj_value(self):
        return self.route.get_total_distance_travel()

    def plot(self, save_path=None):
        self.route.plot_route(save_path)

    def print_solution_path(self):
        initial_value = self.value_without_neighbours
        final_value = self.get_obj_value()

        message = "initial: " + str(self.initial_node)
        message += "| greedy: " + str(self.greedy_constructive)
        message += "| nghb: " + str(self.neighbour_iterations)
        message += "| Impr: " + str(int(((initial_value - final_value) / final_value) * 10000) / 100) + "%"
        message += "| F Val: " + str(int(final_value))
        logging.info(message)

    def get_output_format(self):
        solution_output = [self.list_of_locations.index(location) for location in self.route.sequence_list]

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

    @staticmethod
    def get_solutions_to_improve_list(amount_of_best_sol_to_imp, amount_of_bad_sol_to_imp, greedy_heuristics_approaches, amount_of_solutions_to_improve):
        solution_list = Solution.list_of_solutions.copy()

        # Pick best solutions to improve.
        solution_list.sort(key=lambda sol: sol.get_obj_value())
        solutions_to_add_set = set(solution_list[:amount_of_best_sol_to_imp] + solution_list[-amount_of_bad_sol_to_imp:])
        sol_dict_by_const_appr = {greedy_approach: set() for greedy_approach in greedy_heuristics_approaches}
        for solution in solutions_to_add_set:
            sol_dict_by_const_appr[solution.greedy_constructive].add(solution)

        i = 0
        solution_group_count = [len(solution_group) for solution_group in sol_dict_by_const_appr.values()]
        while min(solution_group_count) <= amount_of_solutions_to_improve \
                and sum(solution_group_count) < len(solution_list) \
                and amount_of_solutions_to_improve + i < len(solution_list):
            solution = solution_list[amount_of_best_sol_to_imp + i]
            if len(sol_dict_by_const_appr[solution.greedy_constructive]) <= amount_of_best_sol_to_imp:
                sol_dict_by_const_appr[solution.greedy_constructive].add(solution)
            solution_group_count = [len(solution_group) for solution_group in sol_dict_by_const_appr.values()]
            i += 1
        sol_dict_by_const_appr = {initial_sol_name: list(solutions) for initial_sol_name, solutions in sol_dict_by_const_appr.items()}

        solutions_to_improve = []
        for solutions in sol_dict_by_const_appr.values():
            solutions_to_improve.extend(solutions)

        return solutions_to_improve

    @staticmethod
    def improve_for_solution(solution, approach):
        solution.improve_solution(approach)
        return solution

    @staticmethod
    def parallel_improvement_run(solutions_to_improve, approach_neighbours):
        with Pool() as pool:
            results_solutions_list = pool.starmap(Solution.improve_for_solution, [(sol, approach_neighbours) for sol in solutions_to_improve])
        return results_solutions_list
        # for solution in solutions_to_improve:
        #     solution.improve_solution(approach_neighbours)
