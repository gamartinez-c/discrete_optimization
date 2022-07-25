#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import sys
import time
import logging
from multiprocessing import Process, Pool, Manager

import matplotlib.pyplot as plt

from solution import Solution
from location import Location

logging.basicConfig(level=logging.INFO, format="%(asctime)s --- %(message)s")
sys.setrecursionlimit(20000)


def solve_it(input_data_list):
    Solution.list_of_solutions = []

    amount_of_random = 1000 if len(Location.locations_list) < 30000 else 10

    amount_of_best_sol_to_imp, amount_of_bad_sol_to_imp = (1, 1)
    amount_of_solutions_to_improve = amount_of_best_sol_to_imp + amount_of_bad_sol_to_imp

    # Modify this code to run your optimization algorithm

    start_time_load_location = time.time()
    logging.info('Start loading Nodes.')

    # parse the input
    lines = input_data_list.split('\n')
    logging.info("Amount of Nodes: " + str(lines[0]))
    Location.load_locations(lines[1:-1])

    logging.info('Finish loading Nodes.')

    for location in Location.locations_list:
        location.sort_location_list_by_distance()

    logging.info('Finish sorting Nodes.')

    start_time_initial_attribution = time.time()

    logging.info("Time Loading location: " + str(round(start_time_initial_attribution - start_time_load_location, 2)))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    amount_of_random = 1000 if len(Location.locations_list) < 30000 else 10
    first_locations_approachs = ['origin'] + ['random']*amount_of_random
    greedy_heuristics_approachs = ['min_distance'] + ['clockwise']*0
    for heuristic_name in greedy_heuristics_approachs:
        for first_location_name in first_locations_approachs:
            solution = Solution()
            solution.solve_initial_solution_for_route(first_location_name, heuristic_name)

    end_initial_solution = time.time()
    time_in_initial_solution = end_initial_solution - start_time_initial_attribution
    logging.info('Initial Solution Time: ' + str(round(time_in_initial_solution, 2)))

    solution_list = Solution.list_of_solutions.copy()
    solution_list.sort(key=lambda sol: sol.get_obj_value())
    solution_list = solution_list[:3] + solution_list[-1:]
    for solution in solution_list:
        loops_for_swaps, loops_for_breaking_bad_connections = (800, 800) if len(Location.locations_list) < 30000 else (100, 100)
        solution.improve_looking_for_neighbours(loops_for_swaps, loops_for_breaking_bad_connections)

    end_neighbours = time.time()
    logging.info('Neighbour Time: ' + str(round(end_neighbours - end_initial_solution, 2)))

    best_solution = Solution.get_best_solution()
    best_solution.plot()

    # Output sequence
    output_data = best_solution.get_output_format()

    return output_data


if __name__ == '__main__':
    file_location = ''
    if len(sys.argv) <= 1:
        case_number = input('Give the case number:')
        file_location = 'data/tsp_' + case_number
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
    if 'all' in file_location:
        file_locations = ['data/' + path for path in os.listdir('data')]
        file_locations.sort(key=lambda x: len(x))
    else:
        file_locations = [file_location]

    time_list = []
    problem_size = []
    for file_location in file_locations:
        start = time.time()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        logging.info('#'*60)
        logging.info('Start with: ' + file_location + '.')  # , end=' ')
        sys.stdout.flush()
        lines = input_data.split('\n')
        if int(lines[0]) <= 30000:
            solution_output = solve_it(input_data)
            # print(solution_output)
            end = time.time()
            time_list.append(end - start)
            problem_size.append(int(lines[0]))

    plt.scatter(problem_size, time_list)
    plt.show()
