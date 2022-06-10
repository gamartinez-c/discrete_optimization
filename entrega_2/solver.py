#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import networkx as nx
from graph import Graph
from color_pallet import ColorPallet


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

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

    color_pallet = ColorPallet()
    amount_of_colors = 4

    graph = Graph()
    graph.graph.add_nodes_from([id_node for id_node in range(node_count)], color=-1, assignation_number=-1, possible_color=[*range(amount_of_colors)])
    graph.graph.add_edges_from(edges)

    amount_assign = 0
    nodes_resolved = set()
    node = graph.get_most_connected_node()
    while node is not None:
        color_of_surrounding_nodes = graph.get_colors_of_surrounding_nodes(node)
        color = color_pallet.get_color(color_excluding=color_of_surrounding_nodes)
        resolved = graph.set_color_of_node(node, color, amount_assign)
        if not resolved:
            graph.plot(flag_current=True)
            time.sleep(1.5)
            print('', end='')
            print("Unable to propagate")

        nodes_resolved.add(node)
        node = graph.get_node_with_least_possibilities(exclude=nodes_resolved)
        amount_assign += 1

        if amount_assign < 0:
            graph.plot()
            time.sleep(1.5)
            print('', end='')

    graph.plot()


    # build a trivial solution
    # every node has its own color
    solution = range(0, node_count)

    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 1:
        case_number = '20_9'  # input('Give the case number:')
        file_location = 'data/gc_' + case_number
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    print(solve_it(input_data))
    if True:
        pass
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

