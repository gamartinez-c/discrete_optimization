from location import Location
import matplotlib.pyplot as plt


class Route:
    def __init__(self):
        self.sequence_list = []

    def add_location(self, location, index=None):
        if index is None:
            self.sequence_list.append(location)
        elif index >= len(self.sequence_list):
            self.sequence_list.append(location)
        else:
            self.sequence_list.insert(index, location)

    def get_total_distance_travel(self):
        total_distance = 0
        if len(self.sequence_list) <= 1:
            return total_distance
        else:
            index = 0
            while index != (len(self.sequence_list) - 1):
                location_1 = self.get_sequence_location(index)
                location_2 = self.get_sequence_location(index + 1)
                total_distance += location_1.distance_to(location_2)
                index += 1
            location_1 = self.get_sequence_location(-1)
            location_2 = self.get_sequence_location(0)
            total_distance += location_1.distance_to(location_2)
            return total_distance

    def get_loc_with_most_travel_times(self):

        prev_location = self.get_sequence_location(-1)
        curr_location = self.get_sequence_location(0)
        foll_location = self.get_sequence_location(1)

        distance_to_prev = prev_location.distance_to(curr_location)
        distance_to_foll = foll_location.distance_to(curr_location)
        biggest_distance = distance_to_prev + distance_to_foll
        picked_location = curr_location
        for location_index in range(1, len(self)):
            prev_location = self.get_sequence_location(location_index - 1)
            curr_location = self.get_sequence_location(location_index)
            foll_location = self.get_sequence_location(location_index + 1)

            distance_to_prev = prev_location.distance_to(curr_location)
            distance_to_foll = foll_location.distance_to(curr_location)
            total_distance_for_location = distance_to_prev + distance_to_foll
            if biggest_distance < total_distance_for_location:
                biggest_distance = total_distance_for_location
                picked_location = curr_location

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
        self.sequence_list.remove(location_2)

        self.add_location(location_2, index_of_location_1)
        self.sequence_list.remove(location_1)

    def plot_route(self):
        position_x_in_route = []
        position_y_in_route = []
        for location in self.sequence_list:
            position_x_in_route.append(location.x)
            position_y_in_route.append(location.y)
        plt.plot(position_x_in_route, position_y_in_route, color='black', marker='o')
        if len(self.sequence_list) == len(Location.locations_list):
            position_x_in_route = []
            position_y_in_route = []
            for location in [self.get_sequence_location(0), self.get_sequence_location(-1)]:
                position_x_in_route.append(location.x)
                position_y_in_route.append(location.y)
                plt.plot(position_x_in_route, position_y_in_route, color='red')

        locations_not_in_route = set(Location.locations_list) - set(self.sequence_list)
        position_x_not_in_route = []
        position_y_not_in_route = []
        for location in locations_not_in_route:
            position_x_not_in_route.append(location.x)
            position_y_not_in_route.append(location.y)
        plt.scatter(position_x_not_in_route, position_y_not_in_route, color='black', marker='o')

        for location in Location.locations_list:
            x, y, s = location.x, location.y, location.id
            plt.text(x+1, y+1, s)

        plt.show()

    def __len__(self):
        return len(self.sequence_list)
