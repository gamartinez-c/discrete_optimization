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
    logging.info("#"*60)
    Solution.list_of_solutions = []

    start_time_load_location = time.time()
    logging.info('Start loading Nodes.')

    # parse the input
    lines = input_data_list.split('\n')
    logging.info("Amount of Nodes: " + str(lines[0]))
    Location.load_locations(lines[1:-1])

    amount_of_random = 100 if len(Location.locations_list) < 1000 else 5

    if len(Location.locations_list) < 1000:
        loops_for_swaps, loops_for_2_opt = (1600, 1600)
        amount_of_best_sol_to_imp, amount_of_bad_sol_to_imp = (3, 1)
    elif len(Location.locations_list) < 30000:
        loops_for_swaps, loops_for_2_opt = (800, 800)
        amount_of_best_sol_to_imp, amount_of_bad_sol_to_imp = (2, 1)
    else:
        loops_for_swaps, loops_for_2_opt = (100, 100)
        amount_of_best_sol_to_imp, amount_of_bad_sol_to_imp = (1, 1)

    amount_of_solutions_to_improve = amount_of_best_sol_to_imp + amount_of_bad_sol_to_imp
    logging.info('Finish loading Nodes.')

    for location in Location.locations_list:
        location.sort_location_list_by_distance()

    logging.info('Finish sorting Nodes.')
    start_time_initial_attribution = time.time()
    logging.info("Time Loading location: " + str(round(start_time_initial_attribution - start_time_load_location, 2)))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    first_locations_approachs = ['origin'] + ['random']*amount_of_random
    greedy_heuristics_approaches = ['min_distance'] + ['mst'] + ['clockwise']*0 + ['cluster_1'] + ['cluster_2']
    for heuristic_name in greedy_heuristics_approaches:
        for first_location_name in first_locations_approachs:
            solution = Solution()
            solution.solve_initial_solution_for_route(first_location_name, heuristic_name)

    end_initial_solution = time.time()
    time_in_initial_solution = end_initial_solution - start_time_initial_attribution
    logging.info('Initial Solution Time: ' + str(round(time_in_initial_solution, 2)))

    solution_list = Solution.list_of_solutions.copy()
    solution_list.sort(key=lambda sol: sol.get_obj_value())
    solutions_to_add_set = set(solution_list[:amount_of_best_sol_to_imp] + solution_list[-amount_of_bad_sol_to_imp:])
    sol_dict_by_const_appr = {greedy_approach: set() for greedy_approach in greedy_heuristics_approaches}
    for solution in solutions_to_add_set:
        sol_dict_by_const_appr[solution.greedy_constructive].add(solution)

    i = 0
    solution_group_count = [len(solution_group) for solution_group in sol_dict_by_const_appr.values()]
    while min(solution_group_count) <= amount_of_best_sol_to_imp and sum(solution_group_count) < len(solution_list):
        solution = solution_list[amount_of_best_sol_to_imp + i]
        if len(sol_dict_by_const_appr[solution.greedy_constructive]) <= amount_of_best_sol_to_imp:
            sol_dict_by_const_appr[solution.greedy_constructive].add(solution)
        solution_group_count = [len(solution_group) for solution_group in sol_dict_by_const_appr.values()]
        i += 1
    sol_dict_by_const_appr = {sol_greedy_name: list(solutions) for sol_greedy_name, solutions in sol_dict_by_const_appr.items()}

    for greedy_approach in sol_dict_by_const_appr:
        for solution in sol_dict_by_const_appr[greedy_approach]:
            solution.improve_looking_for_neighbours(loops_for_swaps, loops_for_2_opt)

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
