#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime as dt
from item import Item
from solution_greedy import SolutionGreedy
from solution_dynamic_programing import SolutionDynamicPrograming


def get_best_solution(solutions):
    best_solution = None
    best_value = 0
    for solution in solutions:
        if solution.value > best_value:
            best_solution = solution
            best_value = best_solution.value
    return best_solution


def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    start = dt.datetime.now()
    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    number_of_items = int(first_line[0])
    capacity_of_knapsack = int(first_line[1])

    print(first_line)

    Item.amount_of_items = 0

    items_list = []
    for i in range(1, number_of_items+1):
        line = lines[i]
        parts = line.split()
        items_list.append(Item(int(parts[0]), int(parts[1]), i - 1))

    try:
        solution_dynamic_programing = SolutionDynamicPrograming(capacity_of_knapsack, items_list)
        solution_dynamic_programing.solve()
        print(solution_dynamic_programing)
        best_solution = solution_dynamic_programing
    except Exception as e:
        print(e)
        solutions = []
        for method in SolutionGreedy.possible_solving_method:
            solver = SolutionGreedy(capacity_of_knapsack, items_list, method)
            solver.solve()
            print(solver)
            solutions.append(solver)
        best_solution = get_best_solution(solutions)

    output_data = best_solution.get_output_format()
    print(best_solution.knapsack)
    print(best_solution.list_of_items[-1])
    print(f'number of items {len(best_solution.list_of_items)}.')
    print('number of booleans ' + str(len(output_data.split("\n")[-1].split(" "))) + '.')

    end_time = dt.datetime.now()
    print('Time', (end_time-start).seconds)

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        number_of_scenario = input('Enter the number of Scenario:')
        file_location = f'data/ks_{number_of_scenario}_0'
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
        #print('This test requires an input file.  Please select one from the data directory. (i.e. python solution_greedy.py ./data/ks_4_0)')

