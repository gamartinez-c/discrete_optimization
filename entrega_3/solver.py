#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import math
import random

from route import Route
from solution import Solution
from location import Location


def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    Location.load_locations(lines[1:])

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    first_locations_approachs = ['origin'] + ['random']
    greedy_heuristics_approachs = ['min_distance'] + ['clockwise']
    for heuristic_name in greedy_heuristics_approachs:
        for first_location_name in first_locations_approachs:
            solution = Solution()
            solution.solve_initial_solution_for_route(first_location_name, heuristic_name)

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
    for file_location in file_locations:
        Solution.list_of_solutions = []
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print('#'*60)
        print('Start with: ' + file_location + '.')  # , end=' ')
        sys.stdout.flush()
        solution_output = solve_it(input_data)
        print(solution_output)
