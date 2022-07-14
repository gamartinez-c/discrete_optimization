#!/usr/bin/python
# -*- coding: utf-8 -*-
import itertools
import logging
import os
import sys
import datetime as dt

from node import Node
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
        graph = Graph()
        for node_id in range(node_count):
            possible_colors = [*range(amount_of_colors)]
            node = Node(node_id, possible_colors)
            graph.add_node(node)
        for node_id_1, node_id_2 in edges:
            graph.add_edge(node_id_1, node_id_2)

        color_pallet = ColorPallet(amount_of_colors)

        graph_to_solve = graph

        has_resolved_graph = Graph.solve_graph_for_amount_of_colors(graph_to_solve, color_pallet, 'most_connected', 0)

        result_text = 'SUCCESS' if has_resolved_graph else 'FAIL'

        end_time = dt.datetime.now()
        print_text = result_text + ','
        print_text += ' Count: ' + str(amount_of_colors) + ','
        print_text += ' Max ' + str(current_max) + ','
        print_text += ' Min ' + str(current_min) + ','
        print_text += ' time: ' + end_time.strftime('%H:%M:%S')
        print(print_text)

        if has_resolved_graph:
            best_graph = graph
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

    for node in best_graph.nodes_dict.values():
        if node.color in node.get_colors_of_surrounding_nodes():
            print('Error')

    if '-1' in output_data:
        print('bug')

    return output_data


if __name__ == '__main__':
    file_location = ''
    if len(sys.argv) <= 1:
        case_number = input('Give the case number:')
        file_location = 'data/gc_' + case_number
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
