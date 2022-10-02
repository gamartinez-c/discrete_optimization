import random
import logging

from route import Route
from location import Location


class Solution:
    list_of_solutions = []

    def __init__(self, list_of_locations=None):
        if list_of_locations is None:
            self.list_of_locations = Location.locations_list
        else:
            self.list_of_locations = list_of_locations
        self.route = Route(self.list_of_locations)
        Solution.list_of_solutions.append(self)

        self.initial_node = None
        self.greedy_constructive = None

    def solve_initial_solution_for_route(self, approach_for_first_loc, greedy_approach):
        first_location = None
        self.initial_node = approach_for_first_loc
        self.greedy_constructive = greedy_approach
        if approach_for_first_loc == "origin":
            first_location = Location.get_nearest_location_to_location()
        elif approach_for_first_loc == "random":
            first_location = random.choice([*Location.locations_list])
        else:
            print("The First Location:", approach_for_first_loc, "is not known")
            exit()

        location_list = self.list_of_locations.copy()
        heuristic = None
        if greedy_approach == "min_distance":
            heuristic = Location.get_locations_ordered_by_distance
        elif greedy_approach == "clockwise":
            heuristic = Location.get_locations_ordered_by_anti_clockwise
        elif greedy_approach == 'mst':
            heuristic = Location.get_mst
        elif greedy_approach == 'cluster_1' or greedy_approach == 'cluster_2':
            heuristic = Location.get_clustered_locations_solution
            if greedy_approach == 'cluster_1':
                first_location = 1
            if greedy_approach == 'cluster_2':
                first_location = 2
        else:
            print("The Greedy approach:", greedy_approach, "is not known")
            exit()

        location_list = heuristic(location_list, first_location)
        for location in location_list:
            self.route.add_location(location)

    def change_location_position(self, location_to_improve):
        initial_index = self.route.sequence_list.index(location_to_improve)

        best_position = initial_index
        best_obj_value = self.get_obj_value()

        for i in range(len(self.route)):
            self.route.remove_location(location_to_improve)
            self.route.add_location(location_to_improve, index=i)
            obj_value = self.get_obj_value()
            if obj_value < best_obj_value:
                best_position = i
                best_obj_value = obj_value

        # Set to best solution
        self.route.remove_location(location_to_improve)
        self.route.add_location(location_to_improve, index=best_position)

    def improve_looking_for_neighbours(self, loops_for_swaps=300, loops_for_breaking_bad_connections=300):
        initial_value = self.get_obj_value()

        prev_location_moved = None
        location_to_move = self.route.get_loc_with_most_travel_times()

        # self.plot()
        # print(self.get_obj_value())
        i = 0
        exclude_locations = []
        while prev_location_moved != location_to_move and i < loops_for_swaps and i <= len(Location.locations_list) - 2:
            original_sequence = self.route.sequence_list.copy()
            original_obj_value = self.get_obj_value()

            self.change_location_position(location_to_move)
            exclude_locations.append(location_to_move)

            if self.get_obj_value() > original_obj_value:
                self.route.reset_route_with(original_sequence)

            prev_location_moved = location_to_move
            location_to_move = self.route.get_loc_with_most_travel_times(exclude_locations=exclude_locations)
            i += 1
        j = i
        # self.plot()
        # print(self.get_obj_value())

        i = 0
        prev_worst_connection = None
        worst_connection_tuple = self.route.get_locs_of_worst_connection()
        while prev_worst_connection != worst_connection_tuple and i < loops_for_breaking_bad_connections:
            self.improve_just_1_link(worst_connection_tuple[0], worst_connection_tuple[1])

            prev_worst_connection = worst_connection_tuple
            worst_connection_tuple = self.route.get_locs_of_worst_connection(exclude_list=[worst_connection_tuple])
            i += 1
        # self.plot()
        final_value = self.get_obj_value()

        message = "initial: " + str(self.initial_node)
        message += "| greedy: " + str(self.greedy_constructive)
        message += "| nghb 1: " + str(j)
        message += "| nghb 2: " + str(i)
        message += "| Impr: " + str(int(((initial_value - final_value)/final_value)*10000)/100) + "%"
        message += "| F Val: " + str(int(final_value))
        logging.info(message)

    def improve_just_1_link(self, src_loc, dest_loc):
        original_sequence = self.route.sequence_list.copy()
        original_obj_value = self.get_obj_value()

        loc_to_exclude_list = [src_loc, self.route.get_sequence_location(self.route.sequence_list.index(dest_loc)+1)]
        ideal_loc_for_dest = dest_loc.get_nearest_location(exclude_location_list=loc_to_exclude_list)
        index_of_ideal_loc_for_dest = self.route.sequence_list.index(ideal_loc_for_dest)
        index_of_src = self.route.sequence_list.index(src_loc)
        index_of_dest = self.route.sequence_list.index(dest_loc)

        index_to_start_extraction = (index_of_dest + 1) % len(self.route)
        index_of_end_extraction = index_of_ideal_loc_for_dest

        if index_to_start_extraction < index_of_end_extraction:
            sequence_to_extract = self.route.sequence_list[index_to_start_extraction: index_of_ideal_loc_for_dest]
        else:
            sequence_to_extract = []
            sequence_to_extract += self.route.sequence_list[index_to_start_extraction:]
            sequence_to_extract += self.route.sequence_list[:index_to_start_extraction]

        for location in sequence_to_extract:
            self.route.remove_location(location)
        # By how we are inserting the sequence is reverse that is what we need
        for location in sequence_to_extract:
            self.route.add_location(location, index_of_src + 1)

        if self.get_obj_value() > original_obj_value:
            self.route.reset_route_with(original_sequence)

    def get_obj_value(self):
        return self.route.get_total_distance_travel()

    def plot(self, save_path=None):
        self.route.plot_route(save_path)

    def get_output_format(self):
        solution_output = [Location.locations_list.index(location) for location in self.route.sequence_list]

        # calculate the length of the tour
        obj = self.get_obj_value()

        # prepare the solution in the specified output format
        output_data = '%.2f' % obj + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, solution_output))
        return output_data

    @staticmethod
    def get_best_solution():
        best_solution = Solution.list_of_solutions[0]
        best_obj = best_solution.get_obj_value()
        for solution in Solution.list_of_solutions[1:]:
            if solution.get_obj_value() < best_obj:
                best_solution = solution
                best_obj = solution.get_obj_value()
        return best_solution
