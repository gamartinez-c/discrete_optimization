import logging
import time
import math
import random
import matplotlib.pyplot as plt
import numpy as np

from improvements.neighbours import Neighbours


class SimulatedAnnealing(Neighbours):

    def __init__(self, route, type_of_swap, initial_temperature, cooldown_factor, max_iterations):
        super().__init__(route)
        self.initial_temperature = initial_temperature
        self.reheat_temperature = initial_temperature
        self.current_temperature = initial_temperature

        self.cooldown_factor = cooldown_factor

        self.max_iterations = max_iterations
        self.iteration_num = None

        self.index_of_iterations = []
        self.history_of_obj_value = []
        self.history_of_temperature = []
        self.history_of_reheat_temperature = []

        self.type_of_swap = type_of_swap

    def improve(self, plot):
        self.iteration_num = 0
        should_keep_on_looping = True
        start_time = time.time()
        best_route = self.route.copy()
        amount_of_iterations = 0
        while should_keep_on_looping:
            initial_obj_value = self.route.get_total_distance_travel()
            initial_route = self.route.copy()
            random_index_node_1, random_index_node_2 = random.sample(range(0, len(self.route)), 2)
            # FIXME: WHAT IF NODES ARE PREETY NEAR

            swap_benefit = self.calculate_2_opt_movement_benefit(random_index_node_1, random_index_node_2)
            final_obj_value = initial_obj_value - swap_benefit
            random_prob_value = random.random()
            prob_of_acceptance = self.calculate_acceptance_prob(initial_obj_value, final_obj_value)
            if random_prob_value <= prob_of_acceptance:
                self.make_2_opt_movement_by_index(random_index_node_1, random_index_node_2)

            # initial_obj_value = self.route.get_total_distance_travel()
            # initial_route = self.route.copy()
            # random_index_node_1, random_index_node_2 = random.sample(range(0, len(self.route)), 2)
            # # FIXME: Need to precalculate
            # self.swap_2_index(random_index_node_1, random_index_node_2)
            # final_obj_value = self.route.get_total_distance_travel()
            # if final_obj_value > initial_obj_value:
            #     self.route = initial_route

            if best_route.get_total_distance_travel() > self.route.get_total_distance_travel():
                best_route = self.route.copy()

            self.store_records(amount_of_iterations)
            # self.check_for_reheat(amount_of_iterations)
            if (amount_of_iterations % 20000) == 0 and plot:
                logging.info("Number of iterations: " + str(amount_of_iterations) + ", Obj value: " + str(self.route.get_total_distance_travel()))
                # self.plot_data()

            self.decrease_temp()
            self.iteration_num += 1
            amount_of_iterations += 1
            running_time = time.time() - start_time
            should_keep_on_looping = self.should_keep_on_looping(running_time, amount_of_iterations)

        if plot:
            self.plot_data()
        self.route = best_route
        return {'Simulated annealing': amount_of_iterations}

    def check_for_reheat(self, amount_of_iterations):
        time_window = 1000
        window_to_look_for_imprv = 100
        if (amount_of_iterations % time_window) == 0 and amount_of_iterations > time_window * 2:
            curr_obj_val = self.get_obj_value_with_agg(window_to_look_for_imprv, np.mean)
            past_obj_val = self.get_obj_value_with_agg(time_window-window_to_look_for_imprv, np.mean, offset=window_to_look_for_imprv)
            improvement = (1 - curr_obj_val / past_obj_val)
            if 0.001 > improvement >= 0:
                self.increase_temp()

        if self.iteration_num % 4000 == 0 and self.iteration_num > time_window * 4:
            worst_past_records = self.get_obj_value_with_agg(time_window * 2, max, offset=time_window)
            worst_current_records = self.get_obj_value_with_agg(time_window * 2, max)
            best_curr_records = self.get_obj_value_with_agg(time_window * 2, min)
            if worst_past_records < worst_current_records:
                self.reheat_temperature = self.reheat_temperature / 2
            elif worst_current_records/best_curr_records < 1.001:
                self.reheat_temperature = self.reheat_temperature * 2

    def store_records(self, amount_of_iterations):
        self.history_of_obj_value.append(self.route.get_total_distance_travel())
        self.history_of_temperature.append(self.current_temperature)
        self.history_of_reheat_temperature.append(self.reheat_temperature)
        self.index_of_iterations.append(amount_of_iterations)

    def print_progress_logs(self):
        pass

    def get_obj_value_with_agg(self, time_window, agg, offset=0):
        value = agg(self.history_of_obj_value[-time_window-offset:])
        return value

    def plot_data(self, last_n_records=None):
        if last_n_records is None:
            last_n_records = len(self.history_of_obj_value)
        self.route.plot_route()
        plt.show()

        fig, ax = plt.subplots()
        taxis = ax.twinx()
        ax.plot(self.index_of_iterations[-last_n_records:], self.history_of_obj_value[-last_n_records:], color='black', alpha=0.5)
        taxis.plot(self.index_of_iterations[-last_n_records:], self.history_of_temperature[-last_n_records:], color='red', alpha=0.5)
        taxis.plot(self.index_of_iterations[-last_n_records:], self.history_of_reheat_temperature[-last_n_records:], color='green', alpha=0.5)
        plt.show()

    def should_keep_on_looping(self, running_time, amount_of_iterations):
        has_available_time = self.has_available_time(running_time)
        has_remaining_iterations = self.max_iterations > amount_of_iterations
        return has_available_time & has_remaining_iterations

    def decrease_temp(self):
        self.current_temperature = self.current_temperature*self.cooldown_factor

    def increase_temp(self):
        self.current_temperature += self.reheat_temperature

    def calculate_acceptance_prob(self, initial_obj_value, final_obj_value):
        exponential_value = min(((initial_obj_value - final_obj_value)/self.current_temperature), 0)
        return min(math.exp(exponential_value), 1)
