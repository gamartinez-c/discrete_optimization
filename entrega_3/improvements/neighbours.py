import time
import itertools
import logging

from route import Route
from location import Location


class Neighbours:

    def __init__(self, route: Route):
        self.route = route

    def get_number_of_iterations(self):
        count_locations = len(self.route.locations_to_consider)
        if count_locations < 1000:
            num_iterations = 4000
        elif count_locations < 15000:
            num_iterations = 800
        else:
            num_iterations = 100

        return num_iterations

    def get_available_time(self):
        count_locations = len(self.route.locations_to_consider)
        if count_locations < 100:
            available_time = 0.25 * 60 * 60
        elif count_locations < 1000:
            available_time = 0.4 * 60 * 60
        elif count_locations < 2000:
            available_time = 0.75 * 60 * 60
        else:
            available_time = 1 * 60 * 60
        return available_time

    def has_available_time(self, current_running_time):
        available_time = self.get_available_time()
        return available_time > current_running_time

    def change_location_position(self, location_to_improve):
        initial_index = self.route.sequence_list.index(location_to_improve)

        best_position = initial_index
        best_obj_value = self.route.get_total_distance_travel()

        for i in range(len(self.route)):
            self.route.remove_location(location_to_improve)
            self.route.add_location(location_to_improve, index=i)
            obj_value = self.route.get_total_distance_travel()
            if obj_value < best_obj_value:
                best_position = i
                best_obj_value = obj_value

        # Set to best solution
        self.route.remove_location(location_to_improve)
        self.route.add_location(location_to_improve, index=best_position)

    def improve_by_2_opt(self, max_number_of_loops=None):
        start_time = time.time()
        available_time = self.get_available_time()
        improve = True
        amount_of_iterations = 0
        time_spent = 0
        while improve:
            original_obj_val = self.route.get_total_distance_travel()
            for start_index in range(len(self.route) - 1):
                for end_index in range(start_index + 1, len(self.route)):
                    if start_index < end_index:
                        self.improve_2_opt_by_index(start_index, end_index)
            final_obj_val = self.route.get_total_distance_travel()
            improve = final_obj_val < original_obj_val

            current_time = time.time()
            time_spent = current_time - start_time

            amount_of_iterations += 1
            if time_spent > available_time:
                break

        return {'2_opt': amount_of_iterations, 'Exit time': (time_spent > available_time)}

    def swap_2_index(self, index_1, index_2):
        loc_1 = self.route.get_location_by_index(index_1)
        loc_2 = self.route.get_location_by_index(index_2)
        self.route.remove_location(loc_2)
        self.route.remove_location(loc_1)
        if index_1 < index_2:
            self.route.add_location(loc_2, index_1)
            self.route.add_location(loc_1, index_2)
        else:
            self.route.add_location(loc_1, index_2)
            self.route.add_location(loc_2, index_1)

    def best_improvement(self):
        num_iterations = self.get_number_of_iterations()

        iterations = 0
        iteration_2_opt = 0
        iterations_changing_locations = 0
        improved = True
        while improved and iterations < num_iterations:
            original_route = self.route.copy()
            initial_obj_value = self.route.get_total_distance_travel()

            route_imp_sol = self.route.copy()
            self.route = route_imp_sol
            location_to_move = self.route.get_loc_with_most_travel_times()
            self.change_location_position(location_to_move)

            nodes_to_exclude = []
            first_worst_connection = self.route.get_locs_of_worst_connection()
            nodes_to_exclude.append(first_worst_connection[1])
            node_to_reconnect = first_worst_connection[0]
            best_route_2_opt = original_route.copy()
            for i in range(10):
                route_2_opt = original_route.copy()
                self.route = route_2_opt
                node_to_connect_to = node_to_reconnect.get_nearest_location(self.route.locations_to_consider, exclude_location_list=nodes_to_exclude)
                self.improve_2_opt(node_to_reconnect, node_to_connect_to)
                nodes_to_exclude.append(node_to_connect_to)
                if best_route_2_opt.get_total_distance_travel() > route_2_opt.get_total_distance_travel():
                    best_route_2_opt = route_2_opt

            best_route_improvement = original_route
            for route in [best_route_2_opt, route_imp_sol]:
                if route.get_total_distance_travel() < best_route_improvement.get_total_distance_travel():
                    best_route_improvement = route
            final_obj_value = best_route_improvement.get_total_distance_travel()
            improved = final_obj_value < initial_obj_value
            if not improved:
                self.route = original_route

            iterations += 1
            if best_route_improvement == route_2_opt:
                iteration_2_opt += 1
            else:
                iterations_changing_locations += 1

        return {'improve_1_link': iterations_changing_locations, '2_opt': iteration_2_opt}

    def improve_2_opt_by_index(self, index_to_start_extraction, index_of_end_extraction):
        original_route = self.route.copy()
        original_obj_value = self.route.get_total_distance_travel()

        self.make_2_opt_movement_by_index(index_to_start_extraction, index_of_end_extraction)

        if self.route.get_total_distance_travel() > original_obj_value:
            self.route = original_route

    def make_2_opt_movement_by_index(self, index_to_start_extraction, index_of_end_extraction):
        if index_to_start_extraction < index_of_end_extraction:
            new_sequence_to_insert = self.route.sequence_list[index_to_start_extraction: index_of_end_extraction + 1]
        else:
            new_sequence_to_insert = []
            new_sequence_to_insert += self.route.sequence_list[index_to_start_extraction:]
            new_sequence_to_insert += self.route.sequence_list[:index_of_end_extraction + 1]

        self.route.remove_multiple_location_sequenced(new_sequence_to_insert)
        # By how we are inserting the sequence is reverse that is what we need
        new_sequence_to_insert.reverse()
        if index_to_start_extraction < index_of_end_extraction:
            index_to_insert_on = index_to_start_extraction
        else:
            index_to_insert_on = len(self.route)
        self.route.add_multiple_locations(new_sequence_to_insert, index_to_insert_on)

    def improve_2_opt(self, src_loc_of_link, dest_loc_of_link):
        index_of_dest = self.route.sequence_list.index(dest_loc_of_link)
        loc_to_exclude_list = [src_loc_of_link, self.route.get_location_by_index(index_of_dest + 1)]
        loc_to_change_src_with = dest_loc_of_link.get_nearest_location(self.route.locations_to_consider, exclude_location_list=loc_to_exclude_list)
        index_loc_to_change_src_with = self.route.sequence_list.index(loc_to_change_src_with)

        index_to_start_extraction = index_of_dest
        index_of_end_extraction = (index_loc_to_change_src_with - 1) % len(self.route)

        self.improve_2_opt_by_index(index_to_start_extraction, index_of_end_extraction)
