#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import math
import random

from location import Location
from route import Route


def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def get_output_format(best_route):
    solution_output = [Location.locations_list.index(location) for location in best_route.sequence_list]

    # calculate the length of the tour
    obj = best_route.get_total_distance_travel()

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution_output))
    return output_data


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    locations = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        locations.append(Location(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    route_solution_dict = {}
    first_location_dict = {
        'origin': Location.get_nearest_location_to_origin()
    }
    list_from_picking_random = Location.locations_list.copy()
    for i in range(100):
        if len(list_from_picking_random) != 0:
            first_location = random.choice(list_from_picking_random)
            list_from_picking_random.remove(first_location)
            first_location_dict['random_' + str(i)] = first_location

    greedy_heuristics_dict = {
        'min_distance': Location.get_locations_ordered_by_distance,
        # 'clockwise': Location.get_locations_ordered_by_anti_clockwise
    }

    for heuristic_name, heuristic in greedy_heuristics_dict.items():
        for first_location_name, first_location in first_location_dict.items():
            location_list = heuristic(first_location)
            route = Route()
            for location in location_list:
                route.add_location(location)
            route_solution_dict[first_location_name + '-' + heuristic_name] = route

    best_route = random.choice([*route_solution_dict.values()])
    best_distance = best_route.get_total_distance_travel()
    for solution_name, route in route_solution_dict.items():
        # print(solution_name, route.get_total_distance_travel())
        # route.plot_route()
        if route.get_total_distance_travel() < best_distance:
            best_route = route
            best_distance = route.get_total_distance_travel()

    best_route.plot_route()

    # Output sequence
    output_data = get_output_format(best_route)

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
        Location.locations_list = []
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print('#'*60)
        print('Start with: ' + file_location + '.') #, end=' ')
        sys.stdout.flush()
        solution_output = solve_it(input_data)
        print(solution_output)