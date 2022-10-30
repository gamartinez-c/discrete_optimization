#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
import itertools

from solution import Solution
from location import Location

logging.basicConfig(level=logging.INFO, format="%(asctime)s --- %(message)s")
sys.setrecursionlimit(20000)


def solve_it(input_data_list):
    logging.info("#"*60)
    Solution.list_of_solutions = []

    start_time_load_location = time.time()
    logging.info('Start loading Nodes.')

    # parse the input
    lines = input_data_list.split('\n')
    logging.info("Amount of Nodes: " + str(lines[0]))
    location_list = Location.load_locations(lines[1:-1])

    approach_neighbours = 'simple'
    if len(location_list) < 500:
        approach_neighbours = 'simulated_annealing'

    if approach_neighbours in ['simple', 'simulated_annealing']:
        amount_of_random = 1
        amount_of_best_sol_to_imp, amount_of_bad_sol_to_imp = (1, 0)
    else:
        amount_of_random = 100 if len(location_list) < 1000 else 5
        if len(location_list) < 1000:
            amount_of_best_sol_to_imp, amount_of_bad_sol_to_imp = (5, 2)
        elif len(location_list) < 15000:
            amount_of_best_sol_to_imp, amount_of_bad_sol_to_imp = (2, 1)
        else:
            amount_of_best_sol_to_imp, amount_of_bad_sol_to_imp = (1, 1)
    amount_of_solutions_to_improve = amount_of_best_sol_to_imp + amount_of_bad_sol_to_imp
    first_locations_approachs = ['origin'] + ['random']*amount_of_random
    greedy_heuristics_approaches = ['min_distance'] + ['mst']*1 + ['clockwise']*0 + ['cluster_1']*0 + ['cluster_2']*0

    logging.info('Finish loading Nodes.')

    for location in location_list:
        location.sort_location_list_by_distance(location_list)

    logging.info('Finish sorting Nodes.')
    start_time_initial_attribution = time.time()
    logging.info("Time Loading location: " + str(round(start_time_initial_attribution - start_time_load_location, 2)))

    # #################################################################################
    # ############################ Build Initial Solutions ############################
    # #################################################################################
    # visit the nodes in the order they appear in the file
    solution_comb = [*itertools.product(first_locations_approachs, greedy_heuristics_approaches)]
    for first_location_name, heuristic_name in solution_comb:
        solution = Solution(location_list)
        solution.solve_initial_solution_for_route(first_location_name, heuristic_name)

    end_initial_solution = time.time()
    time_in_initial_solution = end_initial_solution - start_time_initial_attribution
    logging.info('Initial Solution Time: ' + str(round(time_in_initial_solution, 2)))

    # ####################################################################
    # ############################ Neighbours ############################
    # ####################################################################

    solutions_to_improve = Solution.get_solutions_to_improve_list(amount_of_best_sol_to_imp, amount_of_bad_sol_to_imp, greedy_heuristics_approaches, amount_of_solutions_to_improve)
    logging.info('Solutions have been picked')

    for solution in solutions_to_improve:
        solution.improve_solution(approach_neighbours)

    end_neighbours = time.time()
    logging.info('Neighbour Time: ' + str(round(end_neighbours - end_initial_solution, 2)))

    best_solution = Solution.get_best_solution()
    best_solution.plot('charts/' + str(lines[0]) + '.png')

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

    # plt.scatter(problem_size, time_list)
    # plt.show()
