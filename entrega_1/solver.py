#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime as dt
import sys
import threading

from item import Item
from solution_greedy import SolutionGreedy
from solution_dynamic_programing import SolutionDynamicPrograming
from solution_branch_and_bound import SolutionBranchAndBound


def get_best_solution(solutions):
    best_solution = None
    best_value = 0
    for solution in solutions:
        if solution.value > best_value:
            best_solution = solution
            best_value = best_solution.value
    return best_solution


def solve_it(input_data):
    print('\n', '-'*60)

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

    approach = 'branch and bound'

    if approach == 'branch and bound':
        sys.setrecursionlimit(100000)
        threading.stack_size(200000000)

        solution_branch_and_bound = SolutionBranchAndBound(capacity_of_knapsack, items_list)

        thread_1 = threading.Thread(target=solution_branch_and_bound.solve)
        thread_1.start()
        thread_1.join()
        best_solution = solution_branch_and_bound
        print('Solved Branch and Bound')

    elif approach == 'dynamic':
        solution_dynamic_programing = SolutionDynamicPrograming(capacity_of_knapsack, items_list)
        solution_dynamic_programing.solve()
        print(solution_dynamic_programing)
        best_solution = solution_dynamic_programing
        print('Solved with Dynamic')
    else:
        solutions = []
        for method in SolutionGreedy.possible_solving_method:
            solver = SolutionGreedy(capacity_of_knapsack, items_list, method)
            solver.solve()
            print(solver)
            solutions.append(solver)
        best_solution = get_best_solution(solutions)
        print('Solved with greedy')

    output_data = best_solution.get_output_format()
    print(best_solution.knapsack)

    end_time = dt.datetime.now()
    print('Time', (end_time-start).seconds)

    return output_data


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
            print(solve_it(input_data))
    else:
        print('Arranca')
        number_of_scenario = input('Enter the number of Scenario:')
        file_location = f'data/ks_{number_of_scenario}_0'
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
            print(solve_it(input_data))
