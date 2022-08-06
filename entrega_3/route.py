import logging
import random
import matplotlib.pyplot as plt


class Route:
    def __init__(self, locations_to_consider):
        self.locations_to_consider = locations_to_consider
        self.sequence_list = []
        self.total_distance = 0

    def add_location(self, location, index=None):
        if index is None or index >= len(self):
            index = len(self) - 1

        if len(self) != 0:
            self.total_distance -= self.get_distance_to_location(index)

        self.sequence_list.insert(index, location)
        self.total_distance += self.get_total_distance_of_location(index)

    def remove_location(self, location):
        index_of_location = self.sequence_list.index(location)

        self.total_distance -= self.get_total_distance_of_location(index_of_location)
        self.sequence_list.remove(location)

        if len(self) != 0:
            self.total_distance += self.get_distance_to_location(index_of_location)

    def get_total_distance_travel(self):
        return self.total_distance

    def get_distance_to_location(self, location_index):
        prev_location = self.get_sequence_location(location_index - 1)
        curr_location = self.get_sequence_location(location_index)
        return prev_location.distance_to(curr_location)

    def get_distance_from_location(self, location_index):
        curr_location = self.get_sequence_location(location_index)
        foll_location = self.get_sequence_location(location_index + 1)
        return foll_location.distance_to(curr_location)

    def get_total_distance_of_location(self, location_index):
        total_distance = 0
        total_distance += self.get_distance_to_location(location_index)
        total_distance += self.get_distance_from_location(location_index)
        return total_distance

    def get_loc_with_most_travel_times(self, exclude_locations=None):
        exclude_locations = exclude_locations if exclude_locations is not None else []
        picked_location = random.choice([*{*self.locations_to_consider} - {*exclude_locations}])
        picked_location_index = self.sequence_list.index(picked_location)
        biggest_distance = self.get_total_distance_of_location(picked_location_index)
        for location_index in range(0, len(self)):
            current_location = self.get_sequence_location(location_index)
            if current_location not in exclude_locations:
                total_distance_for_location = self.get_total_distance_of_location(location_index)
                if biggest_distance < total_distance_for_location:
                    biggest_distance = total_distance_for_location
                    picked_location = current_location

        return picked_location

    def get_sequence_location(self, index):
        index = index % len(self)
        return self.sequence_list[index]

    def get_locs_of_worst_connection(self, exclude_list=None):
        exclude_list = [] if exclude_list is None else exclude_list
        exclude_list_index = [(self.sequence_list.index(src), self.sequence_list.index(dest)) for src, dest in exclude_list]

        src_loc_index = 0
        dest_loc_index = 1
        if (src_loc_index, dest_loc_index) in exclude_list_index:
            src_loc_index += 1
            dest_loc_index += 1
        src_loc = self.get_sequence_location(src_loc_index)
        dest_loc = self.get_sequence_location(dest_loc_index)
        worst_src_and_dest = (src_loc, dest_loc)
        worst_distance = src_loc.distance_to(dest_loc)

        src_loc_index += 1
        dest_loc_index += 1
        src_loc_index = src_loc_index % len(self)
        dest_loc_index = dest_loc_index % len(self)

        while src_loc_index != 0:
            src_loc = self.get_sequence_location(src_loc_index)
            dest_loc = self.get_sequence_location(dest_loc_index)
            distance_between_src_and_dest = src_loc.distance_to(dest_loc)
            if worst_distance < distance_between_src_and_dest:
                worst_src_and_dest = (src_loc, dest_loc)
                worst_distance = distance_between_src_and_dest

            src_loc_index += 1
            dest_loc_index += 1
            if (src_loc_index, dest_loc_index) in exclude_list_index:
                src_loc_index += 1
                dest_loc_index += 1
            src_loc_index = src_loc_index % len(self)
            dest_loc_index = dest_loc_index % len(self)
        return worst_src_and_dest

    def swap_locations(self, location_1, location_2):
        index_of_location_1 = self.sequence_list.index(location_1)
        index_of_location_2 = self.sequence_list.index(location_2)

        self.add_location(location_1, index_of_location_2)
        self.remove_location(location_2)

        self.add_location(location_2, index_of_location_1)
        self.remove_location(location_1)

    def reset_route_with(self, sequence_list):
        self.sequence_list = []
        self.total_distance = 0
        for location in sequence_list:
            self.add_location(location)

    def plot_route(self, save_path):
        position_x_in_route = []
        position_y_in_route = []
        for location in self.sequence_list:
            position_x_in_route.append(location.x)
            position_y_in_route.append(location.y)
        plt.plot(position_x_in_route, position_y_in_route, color='black', marker='o')
        if len(self) == len(self.locations_to_consider):
            position_x_in_route = []
            position_y_in_route = []
            for location in [self.get_sequence_location(0), self.get_sequence_location(-1)]:
                position_x_in_route.append(location.x)
                position_y_in_route.append(location.y)
                plt.plot(position_x_in_route, position_y_in_route, color='red')

        locations_not_in_route = set(self.locations_to_consider) - set(self.sequence_list)
        position_x_not_in_route = []
        position_y_not_in_route = []
        for location in locations_not_in_route:
            position_x_not_in_route.append(location.x)
            position_y_not_in_route.append(location.y)
        plt.scatter(position_x_not_in_route, position_y_not_in_route, color='black', marker='o')

        if len(self.locations_to_consider) < 100:
            for location in self.locations_to_consider:
                x, y, s = location.x, location.y, location.id
                plt.text(x+1, y+1, s)

        if save_path is not None:
            try:
                plt.savefig(save_path)
            except:
                logging.info('Wrong path to save.')
        else:
            plt.show()

    def __hash__(self):
        return '-'.join([str(location.id) for location in self.sequence_list])

    def __eq__(self, other):
        same_route = self.sequence_list == other.sequence_list
        same_obj_value = self.total_distance == self.total_distance
        return same_route and same_obj_value

    def __len__(self):
        return len(self.sequence_list)
