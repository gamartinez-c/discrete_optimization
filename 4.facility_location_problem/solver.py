#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import time
import logging
from subprocess import Popen, PIPE

def solve_it(input_data):

    os.chdir(os.getcwd() + "/src")

    # Runs the command: java Solver -file=tmp.data
    process = Popen(['javac', 'Solver.java', '-d', '..\\output\\'], shell=True)
    process.communicate()

    os.chdir(os.getcwd() + "\\..\\output\\")

    # Writes the inputData to a temporay file
    tmp_file_name = 'tmp.data'
    tmp_file = open(tmp_file_name, 'w')
    tmp_file.write(input_data)
    tmp_file.close()

    print("Ready")
    process = Popen(['java', 'Solver', '-file=' + tmp_file_name], stdout=PIPE, universal_newlines=True)
    # for stdout_line in iter(popen.stdout.readline, ""):
    #     yield stdout_line
    # process.stdout.close()
    (stdout, stderr) = process.communicate()
    print(stdout)

    # removes the temporay file
    os.remove(tmp_file_name)
    for file in [file for file in os.listdir() if ".class" in file]:
        os.remove(file)
    os.chdir(os.getcwd() + "\\..\\")

    return stdout.strip()


if __name__ == '__main__':
    file_location = ''
    if len(sys.argv) <= 1:
        case_number = input('Give the case number:')
        file_location = 'data/fl_' + case_number
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
        logging.info('#' * 60)
        logging.info('Start with: ' + file_location + '.')  # , end=' ')
        sys.stdout.flush()
        lines = input_data.split('\n')
        solution_output = solve_it(input_data)
        # print(solution_output)
        end = time.time()
        time_list.append(end - start)
        problem_size.append(int(lines[0]))
