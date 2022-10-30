import logging
import time
import math
import random
import matplotlib.pyplot as plt

from improvements.neighbours import Neighbours


class SimulatedAnnealing(Neighbours):

    def __init__(self, route, initial_temperature, type_of_swap, cooldown_factor):
        super().__init__(route)
        self.initial_temperature = initial_temperature
        self.current_temperature = initial_temperature

        self.cooldown_factor = cooldown_factor

        self.type_of_swap = type_of_swap

    def improve(self):
        has_available_time = True
        start_time = time.time()
        best_route = self.route.copy()
        amount_of_iterations = 0
        prev_thousand_iterations = self.route.get_total_distance_travel()
        history_of_obj_value = []
        index_of_iterations = []
        while has_available_time:
            initial_obj_value = self.route.get_total_distance_travel()
            initial_route = self.route.copy()

            random_index_node_1, random_index_node_2 = random.sample(range(0, len(self.route)), 2)
            self.make_2_opt_movement_by_index(random_index_node_1, random_index_node_2)
            final_obj_value = self.route.get_total_distance_travel()
            random_prob_value = random.random()
            prob_of_acceptance = self.calculate_acceptance_prob(initial_obj_value, final_obj_value)
            if random_prob_value > prob_of_acceptance:
                self.route = initial_route

            initial_obj_value = self.route.get_total_distance_travel()
            initial_route = self.route.copy()

            random_index_node_1, random_index_node_2 = random.sample(range(0, len(self.route)), 2)
            self.swap_2_index(random_index_node_1, random_index_node_2)
            final_obj_value = self.route.get_total_distance_travel()
            if final_obj_value > initial_obj_value:
                self.route = initial_route

            if best_route.get_total_distance_travel() > self.route.get_total_distance_travel():
                best_route = self.route.copy()

            if (amount_of_iterations % 1000) == 0:
                curr_obj_val = self.route.get_total_distance_travel()
                improvement = (1 - curr_obj_val/prev_thousand_iterations)
                if 0.001 > improvement > 0:
                    self.increase_temp()
                prev_thousand_iterations = curr_obj_val
                logging.info("Number of iterations: " + str(amount_of_iterations) + ", Obj value: " + str(self.route.get_total_distance_travel()))

            history_of_obj_value.append(self.route.get_total_distance_travel())
            index_of_iterations.append(amount_of_iterations)
            if (amount_of_iterations % 40000) == 0:
                self.route.plot_route()
                plt.show()

                fig, ax = plt.subplots()
                ax.plot(index_of_iterations, history_of_obj_value)
                plt.show()

            self.decrease_temp()
            amount_of_iterations += 1
            running_time = time.time() - start_time
            has_available_time = self.has_available_time(running_time)

        return best_route

    def decrease_temp(self):
        self.current_temperature = self.current_temperature*self.cooldown_factor

    def increase_temp(self):
        self.current_temperature = self.initial_temperature

    def calculate_acceptance_prob(self, initial_obj_value, final_obj_value):
        exponential_value = min(((initial_obj_value - final_obj_value)/self.current_temperature), 0)
        return min(math.exp(exponential_value), 1)
