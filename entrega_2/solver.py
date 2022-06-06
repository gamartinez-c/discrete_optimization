#!/usr/bin/python
# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt


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

    graph = nx.Graph()
    nodes = []
    graph.add_nodes_from([*range(node_count)])
    graph.add_edges_from(edges)

    nx.draw(graph)
    plt.show()
    nx.draw_random(graph)
    plt.show()
    nx.draw_circular(graph)
    plt.show()
    nx.draw_spectral(graph)
    plt.show()

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
        case_number = input('Give the case number:')
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

