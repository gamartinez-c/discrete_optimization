#!/usr/bin/python
# -*- coding: utf-8 -*-
import itertools
import logging
import time
import os
import sys

import datetime as dt
from graph import Graph
from color_pallet import ColorPallet


def solve_it(input_data):
    sys.setrecursionlimit(10000)

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    logging.info('Start', dt.datetime.now())
    current_max = node_count
    current_min = 0
    amount_of_colors = current_max - 1
    previous_amount_of_colors = amount_of_colors + 1
    while amount_of_colors != previous_amount_of_colors:
        color_pallet = ColorPallet(amount_of_colors)

        possible_approches = ['most_connected', 'least_possible']
        approach_dict = {}
        graph = None
        for node_selection_criteria in possible_approches:
            graph = Graph()
            graph.graph.add_nodes_from([id_node for id_node in range(node_count)], color=-1, possible_color=[*range(amount_of_colors)])
            graph.graph.add_edges_from(edges)

            has_resolved_graph = graph.solve_graph_for_amount_of_colors(color_pallet, node_selection_criteria)
            approach_dict[node_selection_criteria[:3]] = ('T', graph) if has_resolved_graph else ('F', graph)
        else:
            result = any([result[0] == 'T' for result in approach_dict.values()])
            result_text = 'SUCCESS' if result else 'FAIL'
            print(result_text, ', Count: ' + str(amount_of_colors),
                  ', Max', current_max, ', Min', current_min, ',',
                  {key: val[0] for key, val in approach_dict.items()}, ', time:', str(int(time.time() % 3600)))
            if result:
                success_graph_list = [graph for result, graph in approach_dict.values() if result == 'T']
                best_graph = success_graph_list[0]
                current_max = amount_of_colors
                previous_amount_of_colors = amount_of_colors
                amount_of_colors = int((current_max+current_min)/2)
            else:
                current_min = amount_of_colors + 1
                previous_amount_of_colors = amount_of_colors
                amount_of_colors = int((current_max+current_min)/2)

    print('Amount of colors in solution ' + str(amount_of_colors))
    # graph.plot()

    output_data = best_graph.get_return_format()

    return output_data


if __name__ == '__main__':
    file_location = ''
    if len(sys.argv) <= 1:
        case_number = input('Give the case number:')
        file_location = 'data/gc_' + case_number
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
    if file_location == 'all':
        file_locations = ['data/' + path for path in os.listdir('data')]
        file_locations.sort(reverse=True)
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
