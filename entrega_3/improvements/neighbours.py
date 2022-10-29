import time
import itertools
import logging

from route import Route


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
            available_time = 0.4 * 6.4 * 0 * 60
        elif count_locations < 2000:
            available_time = 0.75 * 60 * 60
        else:
            available_time = 1 * 60 * 60
        return available_time

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

    def improve_by_2_opt(self):
        start_time = time.time()
        available_time = self.get_available_time()
        improve = True
        amount_of_iterations = 0
        while improve:
            original_obj_val = self.route.get_total_distance_travel()
            combinations = itertools.combinations(range(len(self.route)), 2)
            for start_index, end_index in combinations:
                self.improve_2_opt_by_index(start_index, end_index)
            final_obj_val = self.route.get_total_distance_travel()
            improve = final_obj_val < original_obj_val

            current_time = time.time()
            time_spent = current_time - start_time

            amount_of_iterations += 1
            if time_spent > available_time:
                break

        return {'2_opt': amount_of_iterations}

    def best_improvement(self):
        num_iterations = self.get_number_of_iterations()

        iterations = 0
        iteration_2_opt = 0
        iterations_changing_locations = 0
        improved = True
        while improved and iterations < num_iterations:
            original_route = self.route.copy()
            route_imp_sol = self.route.copy()
            route_2_opt = self.route.copy()
            initial_obj_value = self.route.get_total_distance_travel()

            self.route = route_imp_sol
            location_to_move = self.route.get_loc_with_most_travel_times()
            self.change_location_position(location_to_move)

            self.route = route_2_opt
            worst_connection_tuple = self.route.get_locs_of_worst_connection()
            self.improve_2_opt(worst_connection_tuple[0], worst_connection_tuple[1])

            best_route_improvement = original_route
            for route in [route_2_opt, route_imp_sol]:
                if route.get_total_distance_travel() < best_route_improvement:
                    best_route_improvement = route
            final_obj_value = best_route_improvement.get_total_distance_travel()
            improved = final_obj_value < initial_obj_value
            if not improved:
                self.route = original_route

            iterations += 1
            iteration_2_opt += 1
            iterations_changing_locations += 1

        return {'improve_1_link': iterations_changing_locations, '2_opt': iteration_2_opt}

    def improve_2_opt_by_index(self, index_to_start_extraction, index_of_end_extraction):
        original_sequence = self.route.sequence_list.copy()
        original_obj_value = self.route.get_total_distance_travel()

        self.make_2_opt_movement_by_index(index_to_start_extraction, index_of_end_extraction)

        if self.route.get_total_distance_travel() > original_obj_value:
            self.route.reset_route_with(original_sequence)

    def make_2_opt_movement_by_index(self, index_to_start_extraction, index_of_end_extraction):
        if index_to_start_extraction < index_of_end_extraction:
            new_sequence_to_insert = self.route.sequence_list[index_to_start_extraction: index_of_end_extraction + 1]
        else:
            new_sequence_to_insert = []
            new_sequence_to_insert += self.route.sequence_list[index_to_start_extraction:]
            new_sequence_to_insert += self.route.sequence_list[:index_of_end_extraction + 1]

        for location in new_sequence_to_insert:
            self.route.remove_location(location)
        # By how we are inserting the sequence is reverse that is what we need
        for location in new_sequence_to_insert:
            if index_to_start_extraction < index_of_end_extraction:
                index_to_insert_on = index_to_start_extraction
            else:
                index_to_insert_on = len(self.route)
            self.route.add_location(location, index_to_insert_on)

    def improve_2_opt(self, src_loc_of_link, dest_loc_of_link):
        index_of_dest = self.route.sequence_list.index(dest_loc_of_link)
        loc_to_exclude_list = [src_loc_of_link, self.route.get_location_by_index(index_of_dest + 1)]
        loc_to_change_src_with = dest_loc_of_link.get_nearest_location(self.route.locations_to_consider, exclude_location_list=loc_to_exclude_list)
        index_loc_to_change_src_with = self.route.sequence_list.index(loc_to_change_src_with)

        index_to_start_extraction = index_of_dest
        index_of_end_extraction = (index_loc_to_change_src_with - 1) % len(self.route)

        self.improve_2_opt_by_index(index_to_start_extraction, index_of_end_extraction)
