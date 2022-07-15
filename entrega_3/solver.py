#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from location import Location
from route import Route


def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


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
    first_location = Location.locations_list[0]
    min_distance = first_location.distance_to()
    for location in Location.locations_list[1:]:
        if location.distance_to() < min_distance:
            first_location = location
            min_distance = location.distance_to()

    location_list = Location.get_locations_ordered_by_distance(first_location)
    route = Route()
    route.plot_route()
    for location in location_list:
        route.add_location(location)
    route.plot_route()

    location_list = Location.get_locations_ordered_by_anti_clockwise(first_location)
    route = Route()
    for location in location_list:
        route.add_location(location)
    route.plot_route()

    # Output sequence
    solution_output = [Location.locations_list.index(location) for location in location_list]

    # calculate the length of the tour
    obj = route.get_total_distance_travel()

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution_output))

    route.plot_route()

    return output_data


import sys

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
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print('#'*60)
        print('Start with: ' + file_location + '.') #, end=' ')
        sys.stdout.flush()
        solution_output = solve_it(input_data)
        print(solution_output)